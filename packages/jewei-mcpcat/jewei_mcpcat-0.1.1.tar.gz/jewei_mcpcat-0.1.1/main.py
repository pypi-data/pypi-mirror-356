"""
MCPCat主应用 - 重构版本
保持与原有逻辑完全一致，但使用模块化的服务类
"""

import logging
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
from typing import Dict, Callable
import os

# 导入新的服务类
from app.core.config import settings
from app.services.server_manager import MCPServerManager
from app.api import health, servers

# 创建全局服务器管理器
server_manager = MCPServerManager()

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(settings.app_name)

# 增加更详细的MCP相关日志
logging.getLogger("mcp").setLevel(logging.DEBUG)
logging.getLogger("fastmcp").setLevel(logging.DEBUG)
logging.getLogger("uvicorn.error").setLevel(logging.DEBUG)


# 保持向后兼容的函数
def load_config():
    """保持向后兼容的配置加载函数"""
    from app.services.config_service import ConfigService
    return ConfigService.load_config()


def add_mcp_server(key, value):
    """保持向后兼容的服务器添加函数"""
    return server_manager.add_mcp_server(key, value)


@asynccontextmanager
async def lifespan_manager(app: FastAPI):
    """
    应用生命周期管理器 - 使用服务器管理器的统一生命周期管理
    """
    async with server_manager.create_unified_lifespan(app):
        yield


# 加载配置和创建服务器
print("Loading MCP server list...")
mcpServerList = load_config()
print("MCP server list loaded.")
print(mcpServerList)

# 创建服务器管理器并加载服务器
server_manager.load_servers_from_config()

# 创建 FastAPI 应用
app = FastAPI(
    title=settings.app_name,
    description=settings.description,
    version=settings.app_version,
    lifespan=lifespan_manager
)

# 存储服务器管理器到应用状态，供API使用
app.state.server_manager = server_manager

# 挂载所有服务器
server_manager.mount_all_servers(app)

# 注册API路由
app.include_router(health.router, prefix="/api", tags=["健康检查"])
app.include_router(servers.router, prefix="/api", tags=["服务器管理"])


# 挂载静态文件
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
async def root():
    """根路径 - 返回前端页面"""
    static_file = os.path.join(os.path.dirname(__file__), "static", "index.html")
    if os.path.exists(static_file):
        return FileResponse(static_file)
    return {"message": f"Welcome to {settings.app_name} - {settings.description}"}


def main():
    """主入口点函数"""
    import uvicorn
    uvicorn.run(
        app, 
        host=settings.host, 
        port=settings.port,
        # 优化关闭行为，减少 ASGI 错误
        timeout_graceful_shutdown=10,  # 优雅关闭超时时间
        timeout_keep_alive=5,         # 保持连接超时时间
        log_level="info"
    )


if __name__ == "__main__":
    main()