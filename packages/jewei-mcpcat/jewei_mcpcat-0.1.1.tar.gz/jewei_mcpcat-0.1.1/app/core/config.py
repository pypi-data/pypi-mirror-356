"""应用配置管理"""

import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """应用设置"""
    
    # 应用基础配置
    app_name: str = "MCPCat"
    app_version: str = "0.1.1"
    description: str = "MCP聚合平台 - 支持多种MCP协议的统一管理平台"
    
    # 服务器配置
    host: str = "0.0.0.0"
    port: int = 8000
    
    # MCP配置文件路径
    mcpcat_config_path: str = "config.json"
    
    # 日志配置（如果以后需要）
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# 全局设置实例
settings = Settings()