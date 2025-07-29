"""MCP 설정 로더 클래스"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Union

from .config_loader import load_mcp_config
from .configs import McpConfig, create_mcp_config


class MCPConfigLoader:
    """MCP 설정을 로드하고 관리하는 클래스"""

    DEFAULT_CONFIG_PATHS = [
        Path.home() / ".config" / "pyhub" / "mcp.json",
        Path.home() / ".config" / "pyhub" / "mcp.yaml",
        Path.home() / ".config" / "pyhub" / "mcp.yml",
        Path.home() / ".pyhub" / "mcp.json",
        Path.home() / ".pyhub" / "mcp.yaml",
        Path.home() / ".pyhub" / "mcp.yml",
    ]

    @staticmethod
    def is_default_config_disabled() -> bool:
        """환경변수로 기본 설정이 비활성화되었는지 확인"""
        return os.environ.get("PYHUB_MCP_NO_DEFAULT", "").lower() in ("true", "1", "yes")

    @staticmethod
    def get_environment_config_path() -> Optional[Path]:
        """환경변수에서 설정 파일 경로 가져오기"""
        env_path = os.environ.get("PYHUB_MCP_CONFIG")
        if env_path:
            return Path(env_path)
        return None

    @staticmethod
    def load_from_default_file() -> List[McpConfig]:
        """기본 설정 파일에서 로드"""
        for config_path in MCPConfigLoader.DEFAULT_CONFIG_PATHS:
            if config_path.exists():
                try:
                    return load_mcp_config(config_path)
                except Exception:
                    continue
        return []

    @staticmethod
    def load_from_file(file_path: Union[str, Path]) -> List[McpConfig]:
        """지정된 파일에서 로드"""
        return load_mcp_config(file_path)

    @staticmethod
    def load_from_json(json_str: str) -> List[McpConfig]:
        """JSON 문자열에서 로드"""
        try:
            data = json.loads(json_str)
            if isinstance(data, dict) and "mcpServers" not in data:
                # mcpServers 키가 없으면 추가
                data = {"mcpServers": data}
            return load_mcp_config(data)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {e}")

    @staticmethod
    def load_from_environment() -> List[McpConfig]:
        """환경변수에서 MCP 설정 로드"""
        configs = []

        # PYHUB_MCP_SERVERS 환경변수 (JSON 형식)
        servers_json = os.environ.get("PYHUB_MCP_SERVERS")
        if servers_json:
            try:
                servers_data = json.loads(servers_json)
                if isinstance(servers_data, list):
                    configs.extend(load_mcp_config(servers_data))
                elif isinstance(servers_data, dict):
                    configs.extend(load_mcp_config(servers_data))
            except Exception:
                pass

        # 개별 서버 환경변수 (PYHUB_MCP_SERVER_0, PYHUB_MCP_SERVER_1, ...)
        idx = 0
        while True:
            server_json = os.environ.get(f"PYHUB_MCP_SERVER_{idx}")
            if not server_json:
                break
            try:
                server_data = json.loads(server_json)
                # 단일 서버 설정을 리스트로 변환
                server_configs = load_mcp_config([server_data])
                configs.extend(server_configs)
            except Exception:
                pass
            idx += 1

        return configs

    @staticmethod
    def load_from_cli_args(
        mcp_stdio: Optional[List[str]] = None, mcp_sse: Optional[List[str]] = None, mcp_http: Optional[List[str]] = None
    ) -> List[McpConfig]:
        """CLI 인자에서 MCP 설정 생성"""
        configs = []

        # stdio 타입 서버
        if mcp_stdio:
            for idx, cmd in enumerate(mcp_stdio):
                try:
                    config = create_mcp_config({"transport": "stdio", "name": f"stdio-{idx}", "cmd": cmd})
                    configs.append(config)
                except Exception:
                    pass

        # sse 타입 서버
        if mcp_sse:
            for idx, url in enumerate(mcp_sse):
                try:
                    config = create_mcp_config({"transport": "sse", "name": f"sse-{idx}", "url": url})
                    configs.append(config)
                except Exception:
                    pass

        # streamable_http 타입 서버 (--mcp-http)
        if mcp_http:
            for idx, url in enumerate(mcp_http):
                try:
                    config = create_mcp_config({"transport": "streamable_http", "name": f"http-{idx}", "url": url})
                    configs.append(config)
                except Exception:
                    pass

        return configs

    @staticmethod
    def merge_configs(*config_lists: List[McpConfig]) -> Dict[str, McpConfig]:
        """여러 설정 리스트를 병합 (나중 것이 우선)"""
        merged = {}

        for config_list in config_lists:
            for config in config_list:
                # 서버 이름을 키로 사용하여 병합 (이름이 없으면 transport_index 형태로 생성)
                if config.name:
                    key = config.name
                else:
                    # 이름이 없는 경우 transport와 인덱스로 키 생성
                    base_key = f"{config.transport}"
                    key = base_key
                    idx = 1
                    while key in merged:
                        key = f"{base_key}_{idx}"
                        idx += 1
                merged[key] = config

        return merged
