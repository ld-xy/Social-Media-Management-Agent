"""

    日志配置:
        根据不同日志文件name，区分不同日志模块信息，同时还可以根据env区分环境信息，根据service区分模块服务信息

"""


import os
import sys
from loguru import logger
from typing import Dict, List


_global_logger = None


def setup_multi_module_logging(
    log_dir: str,
    modules_config: List[Dict[str, Any]],
    env: str = "dev",
    service: str = "excel_agent",
    level_console: str = "INFO",
    rotation: str = "50 MB",
    retention: str = "7 days",
    compression: str = "zip",
    use_json_file: bool = True  # 方便代码查看
):
    """
    为多个模块配置日志（service 和 env 全局共用）
    
    Args:
        log_dir: 日志目录
        modules_config: 模块配置列表，每项包含 {
            'name': 模块名（必填）,
            'log_name': 日志文件名（可选，默认使用name）,
            'level': 日志级别（可选，默认DEBUG）
        }
        env: 运行环境（dev/test/prod），全局共用
        service: 服务名称，全局共用
        level_console: 控制台日志级别
        rotation: 日志轮转规则（50 MB 或 00:00）
        retention: 日志保留期限（7 days）
        compression: 压缩格式（zip）
        use_json_file: 是否生成JSON格式日志
    
    示例:
        modules_config = [
            {'name': 'main', 'log_name': 'main', 'level': 'INFO'},
            {'name': 'data_processor', 'log_name': 'data', 'level': 'DEBUG'},
            {'name': 'api_client', 'log_name': 'api', 'level': 'WARNING'},
        ]
    
    返回:
        配置好的全局 logger，需要配合 get_module_logger 使用
    """

    global _global_logger

    os.makedirs(log_dir, exist_ok=True)
    logger.remove()

    # 日志格式：包含 service、env、module 三层标识
    human_format = (
        "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | "
        "pid={process.id} tid={thread.id} | {name}:{function}:{line} | "
        "service={extra[service]} env={extra[env]} module={extra[module]} | {message}"
    )

    # 添加控制台输出（全局共用，显示所有模块日志）
    logger.add(
        sys.stderr, 
        level=level_console,
        format=human_format,
        enqueue=True,
        backtrace=(env == "dev"),
        diagnose=(env == "dev"),
    )

    # 为每个模块添加独立的文件处理器
    for module_cfg in modules_config:
        module_name = module_cfg['name']
        log_name = module_cfg.get('log_name', module_name)
        level = module_cfg.get('level', 'DEBUG')
        
        # 创建过滤器：只记录属于该模块的日志
        def make_filter(mod_name):
            return lambda record: record["extra"].get("module") == mod_name
        
        # 文本格式日志文件
        file_path = os.path.join(log_dir, f"{log_name}.log")
        logger.add(
            file_path,
            level=level,
            format=human_format,
            rotation=rotation,
            retention=retention,
            compression=compression,
            enqueue=True,
            backtrace=False,
            diagnose=False,
            filter=make_filter(module_name)
        )

        # JSON格式日志文件（便于程序解析和监控）
        if use_json_file:
            json_path = os.path.join(log_dir, f"{log_name}.jsonl")
            logger.add(
                json_path,
                level=level,
                serialize=True,
                rotation=rotation,
                retention=retention,
                compression=compression,
                enqueue=True,
                filter=make_filter(module_name)
            )

    _global_logger = logger.bind(service=service, env=env, module="default")

    # 返回全局logger，默认绑定 service 和 env（全局共用）
    return _global_logger


def get_module_logger(module_name: str):
    """
    获取指定模块的logger（继承全局的 service 和 env）
    
    Args:
        module_name: 模块名称，必须与 setup_multi_module_logging 中配置的模块名匹配
    
    返回:
        绑定了 module 字段的 logger 实例
    
    注意:
        - service 和 env 已在初始化时全局绑定，这里只需指定 module
        - 如果需要覆盖 service 或 env，使用 get_custom_module_logger
    """

    if _global_logger is None:
        raise ValueError("请先调用 setup_multi_module_logging 初始化全局 logger")
    return _global_logger.bind(module=module_name)