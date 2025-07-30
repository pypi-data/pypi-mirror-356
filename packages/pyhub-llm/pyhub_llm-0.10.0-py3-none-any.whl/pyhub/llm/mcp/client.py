"""MCP client implementation for pyhub."""

import logging
from contextlib import asynccontextmanager
from typing import Any, Dict, List, Optional, Union

from .configs import McpConfig
from .transports import create_transport

logger = logging.getLogger(__name__)


class MCPClient:
    """MCP 서버와 통신하는 클라이언트 래퍼

    Attributes:
        _server_info: 서버가 제공하는 정보 (name, version)
    """

    def __init__(self, server_params_or_config: Union[Any, Dict[str, Any], McpConfig]):
        """
        Args:
            server_params_or_config: MCP 서버 연결 설정
                - McpConfig: 새로운 dataclass 방식 (권장)
                - Dict[str, Any]: 기존 dict 방식
                - StdioServerParameters: 레거시 방식
        """
        # McpConfig 처리
        if isinstance(server_params_or_config, McpConfig):
            config_dict = server_params_or_config.to_dict()
            self.server_params = None
            self.transport = create_transport(config_dict)
        # 기존 dict 방식
        elif isinstance(server_params_or_config, dict):
            self.server_params = None
            self.transport = create_transport(server_params_or_config)
        # 레거시 StdioServerParameters
        else:
            self.server_params = server_params_or_config
            self.transport = None

        self._session = None
        self._read = None
        self._write = None
        self._server_info = None  # 서버 정보 저장용

    @asynccontextmanager
    async def connect(self):
        """MCP 서버에 연결"""
        try:
            from mcp import ClientSession
        except ImportError:
            raise ImportError("MCP support requires 'mcp' package. " "Install it with: pip install mcp")

        # Transport 사용 (새로운 방식)
        if self.transport:
            async with self.transport.connect() as (read, write):
                self._read = read
                self._write = write

                async with ClientSession(read, write) as session:
                    self._session = session

                    # 연결 초기화 및 서버 정보 저장
                    init_result = await session.initialize()
                    if hasattr(init_result, "serverInfo"):
                        self._server_info = {
                            "name": init_result.serverInfo.name,
                            "version": init_result.serverInfo.version,
                        }
                        logger.info(
                            f"MCP session initialized with server '{self._server_info['name']}' v{self._server_info['version']}"
                        )
                    else:
                        logger.info("MCP session initialized successfully")

                    try:
                        yield self
                    finally:
                        self._session = None
                        logger.info("MCP session closed")

        # 레거시 방식 (StdioServerParameters 직접 사용)
        else:
            from mcp.client.stdio import stdio_client

            async with stdio_client(self.server_params) as (read, write):
                self._read = read
                self._write = write

                async with ClientSession(read, write) as session:
                    self._session = session

                    # 연결 초기화 및 서버 정보 저장
                    init_result = await session.initialize()
                    if hasattr(init_result, "serverInfo"):
                        self._server_info = {
                            "name": init_result.serverInfo.name,
                            "version": init_result.serverInfo.version,
                        }
                        logger.info(
                            f"MCP session initialized with server '{self._server_info['name']}' v{self._server_info['version']}"
                        )
                    else:
                        logger.info("MCP session initialized successfully")

                    try:
                        yield self
                    finally:
                        self._session = None
                        logger.info("MCP session closed")

    async def list_tools(self) -> List[Dict[str, Any]]:
        """MCP 서버에서 사용 가능한 도구 목록 가져오기"""
        if not self._session:
            raise RuntimeError("MCP session not initialized. Use 'async with client.connect():'")

        # MCP 프로토콜에 따라 도구 목록 요청
        result = await self._session.list_tools()

        tools = []
        for tool in result.tools:
            tools.append(
                {
                    "name": tool.name,
                    "description": tool.description or "",
                    "parameters": tool.inputSchema if hasattr(tool, "inputSchema") else {},
                }
            )

        logger.info(f"Found {len(tools)} tools from MCP server")
        return tools

    async def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """MCP 도구 실행"""
        if not self._session:
            raise RuntimeError("MCP session not initialized. Use 'async with client.connect():'")

        logger.debug(f"Executing MCP tool '{tool_name}' with arguments: {arguments}")

        try:
            # MCP 도구 호출
            result = await self._session.call_tool(tool_name, arguments)

            # 결과를 문자열로 변환
            if hasattr(result, "content"):
                # 텍스트 콘텐츠가 있는 경우
                if isinstance(result.content, list):
                    # 여러 콘텐츠가 있는 경우 결합
                    text_parts = []
                    for content in result.content:
                        if hasattr(content, "text"):
                            text_parts.append(content.text)
                        else:
                            text_parts.append(str(content))
                    return "\n".join(text_parts)
                else:
                    return str(result.content)
            else:
                return str(result)

        except Exception as e:
            logger.error(f"Error executing MCP tool '{tool_name}': {e}")
            return f"Error: Failed to execute tool '{tool_name}': {str(e)}"

    async def get_prompts(self) -> List[Dict[str, Any]]:
        """MCP 서버에서 프롬프트 목록 가져오기 (선택적)"""
        if not self._session:
            raise RuntimeError("MCP session not initialized")

        try:
            result = await self._session.list_prompts()
            prompts = []
            for prompt in result.prompts:
                prompts.append(
                    {
                        "name": prompt.name,
                        "description": prompt.description or "",
                        "arguments": prompt.arguments if hasattr(prompt, "arguments") else [],
                    }
                )
            return prompts
        except Exception as e:
            logger.warning(f"Failed to get prompts: {e}")
            return []

    def get_server_info(self) -> Optional[Dict[str, str]]:
        """연결된 서버의 정보 반환"""
        return self._server_info.copy() if self._server_info else None
