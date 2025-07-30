#-*- coding: utf-8 -*-

import asyncio
import logging
import os
from contextlib import AsyncExitStack
from typing import Optional, Any

import chromadb
import mcp.types
from chromadb import Metadata
from chromadb.config import Settings
from chromadb.api.types import OneOrMany, ID, Document, GetResult, QueryResult
from mcp import ClientSession
from mcp.client.sse import sse_client
from mcp.client.stdio import StdioServerParameters, stdio_client
from .logger import NacosMcpRouteLogger
from .nacos_mcp_server_config import NacosMcpServerConfig
from mcp.client.streamable_http import streamablehttp_client


def _stdio_transport_context(config: dict[str, Any]):
  server_params = StdioServerParameters(command=config['command'], args=config['args'], env=config['env'])
  return stdio_client(server_params)

def _sse_transport_context(config: dict[str, Any]):
  return sse_client(url=config['url'], headers=config['headers'] if 'headers' in config else {}, timeout=10)

def _streamable_http_transport_context(config: dict[str, Any]):
  return streamablehttp_client(url=config["url"], headers=config['headers'] if 'headers' in config else {})

class CustomServer:
  def __init__(self, name: str, config: dict[str, Any]) -> None:
    self.name: str = name
    self.config: dict[str, Any] = config
    self.stdio_context: Any | None = None
    self.session: ClientSession | None = None
    self._cleanup_lock: asyncio.Lock = asyncio.Lock()
    self.exit_stack: AsyncExitStack = AsyncExitStack()
    self._initialized_event = asyncio.Event()
    self._shutdown_event = asyncio.Event()
    if 'protocol' in config['mcpServers'][name] and  "mcp-sse" == config['mcpServers'][name]['protocol']:
      self._transport_context_factory = _sse_transport_context
      self._protocol = 'mcp-sse'
    elif 'protocol' in config['mcpServers'][name] and "mcp-streamable" == config['mcpServers'][name]['protocol']:
      self._transport_context_factory = _streamable_http_transport_context
      self._protocol = 'mcp-streamable'
    else:
      self._transport_context_factory = _stdio_transport_context
      self._protocol = 'stdio'

    self._server_task = asyncio.create_task(self._server_lifespan_cycle())


  async def _server_lifespan_cycle(self):
    try:
      server_config = self.config
      if "mcpServers" in self.config:
        mcp_servers = self.config["mcpServers"]
        for key, value in mcp_servers.items():
          server_config = value
      if self._protocol == 'mcp-streamable':
        async with _streamable_http_transport_context(server_config) as (read, write, _):
          async with ClientSession(read, write) as session:
            self.session_initialized_response = await session.initialize()
            self.session = session
            self._initialized = True
            self._initialized_event.set()
            await self.wait_for_shutdown_request()
      elif self._protocol == 'mcp-sse':
        async with _sse_transport_context(server_config) as (read, write):
          async with ClientSession(read, write) as session:
            self.session_initialized_response = await session.initialize()
            self.session = session
            self._initialized = True
            self._initialized_event.set()
            await self.wait_for_shutdown_request()
      else:
        async with _stdio_transport_context(server_config) as (read, write):
          async with ClientSession(read, write) as session:
            self.session_initialized_response = await session.initialize()
            self.session = session
            self._initialized = True
            self._initialized_event.set()
            await self.wait_for_shutdown_request()
    except Exception as e:
      NacosMcpRouteLogger.get_logger().warning("failed to init mcp server " + self.name + ", config: " + str(self.config), exc_info=e)
      self._initialized_event.set()
      self._shutdown_event.set()
  def get_initialized_response(self) -> mcp.types.InitializeResult:
    return self.session_initialized_response

  def healthy(self) -> bool:
    return self.session is not None and self._initialized

  async def wait_for_initialization(self):
    await self._initialized_event.wait()

  async def request_for_shutdown(self):
    self._shutdown_event.set()

  async def wait_for_shutdown_request(self):
    await self._shutdown_event.wait()

  async def list_tools(self) -> list[Any]:
    if not self.session:
      raise RuntimeError(f"Server {self.name} is not initialized")

    tools_response = await self.session.list_tools()

    return tools_response.tools

  async def execute_tool(
          self,
          tool_name: str,
          arguments: dict[str, Any],
          retries: int = 2,
          delay: float = 1.0,
  ) -> Any:
    if not self.session:
      raise RuntimeError(f"Server {self.name} not initialized")

    attempt = 0
    while attempt < retries:
      try:
        result = await self.session.call_tool(tool_name, arguments)

        return result

      except Exception as e:
        attempt += 1
        if attempt < retries:
          await asyncio.sleep(delay)
          await self.session.initialize()
          try:
            result = await self.session.call_tool(tool_name, arguments)
            return result
          except Exception as e:
            raise e
        else:
          raise



  async def cleanup(self) -> None:
    """Clean up server resources."""
    async with self._cleanup_lock:
      try:
        await self.exit_stack.aclose()
        self.session = None
        self.stdio_context = None
      except Exception as e:
        logging.error(f"Error during cleanup of server {self.name}: {e}")

class McpServer:
  name: str
  description: str
  client: ClientSession
  session: ClientSession
  mcp_config_detail: NacosMcpServerConfig
  agentConfig: dict[str, Any]
  mcp_config_detail: NacosMcpServerConfig
  version: str
  def __init__(self, name: str, description: str, agentConfig: dict, id: str, version: str):
    self.name = name
    self.description = description
    self.agentConfig = agentConfig
    self.id = id
    self.version = version
  def get_name(self) -> str:
    return self.name
  def get_description(self) -> str:
    return self.description
  def agent_config(self) -> dict:
    return self.agentConfig
  def to_dict(self):
    return {
      "name": self.name,
      "description": self.description,
      "agentConfig": self.agent_config(),
    }

class ChromaDb:
  def __init__(self) -> None:
    self.dbClient = chromadb.PersistentClient(path=os.path.expanduser("~") + "/.nacos_mcp_router/chroma_db",
                settings=Settings(
                    anonymized_telemetry=False,
                ))
    self._collectionId = "nacos_mcp_router-collection"
    self._collection = self.dbClient.get_or_create_collection(name=self._collectionId)
    self.preIds = []

  def update_data(self, ids: OneOrMany[ID],
        metadatas: Optional[OneOrMany[Metadata]] = None,
        documents: Optional[OneOrMany[Document]] = None,) -> None:
    self._collection.upsert(documents=documents, metadatas=metadatas, ids=ids)

  def get_all_ids(self) -> list[ID]:
    return self._collection.get().get('ids')
  def delete_data(self, ids: list[ID]) -> None:
    self._collection.delete(ids=ids)

  def query(self, query: str, count: int) -> QueryResult:
    NacosMcpRouteLogger.get_logger().info(f"Querying chroma {query}")
    return self._collection.query(
      query_texts=[query],
      n_results=count
    )

  def get(self, id: list[str]) -> GetResult:
    return self._collection.get(ids=id)