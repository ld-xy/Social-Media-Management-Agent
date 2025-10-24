"""

程序启动主入口：负责整个社交媒体管理agent的启动和初始化

"""

import os
from contextlib import asynccontextmanager


from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests


from src.logger import setup_multi_module_logging, get_module_logger


# 初始化全局日志
_ = setup_multi_module_logging(
    log_dir="logs",
    modules_config=[
        {"name": "agent", "log_name": "agent", "level": "INFO"},
        {"name": "social_media_tool", "log_name": "social_media_tool", "level": "INFO"},
        {"name": "api", "log_name": "api", "level": "INFO"},
    ],
    env="prod",
    service="excel_agent_api",
    level_console="INFO",
)
logger = get_module_logger("api")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时执行
    os.makedirs(os.path.join(BASE_DIR, "config"), exist_ok=True)
    logger.info("应用启动，目录初始化完成")
    yield
    # 关闭时执行
    logger.info("应用关闭")


# 创建 FastAPI 应用
app = FastAPI(
    title="小红书内容自动生成与发布系统",
    description="智能生成高质量小红书内容，一键发布",
    version="1.0.0",
    lifespan=lifespan,
)


# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
