# encoding:utf-8
import functools
import logging
import asyncio
from typing import Callable, Optional, Any, Union
import math

# 配置日志记录
logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def decorate(
        log_message: str = "函数 {func_name} 出错: {error}",
        log_level: int = logging.ERROR,
        suppress_exception: bool = False,
        default_return: Any = math.nan,
        custom_logger: Optional[logging.Logger] = None
) -> Callable:
    """
    功能强大的异常处理装饰器，支持同步和异步函数
    
    参数:
        log_message: 自定义日志消息模板，可包含{func_name}和{error}占位符
        log_level: 日志级别，默认ERROR
        suppress_exception: 是否抑制异常并返回默认值
        default_return: 异常发生时的默认返回值
        custom_logger: 自定义logger实例，默认使用函数名作为logger名称
    
    使用示例:
        @decorate("计算失败: {error}")
        def calculate(a, b):
            return a / b
            
        @decorate(suppress_exception=True, default_return=[])
        async def fetch_data():
            return await api.get()
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def Except_Error(*args, **kwargs) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                # 获取或创建logger
                logger = custom_logger or logging.getLogger(func.__name__)

                # 格式化日志消息
                if log_message:
                    msg = log_message.format(func_name=func.__name__, error=str(e))
                else:
                    msg = f"函数 {func.__name__} 执行失败: {str(e)}"

                # 记录日志
                logger.log(log_level, msg, exc_info=True)

                # 根据配置决定是否重新抛出异常
                if not suppress_exception:
                    raise

                return default_return

        @functools.wraps(func)
        async def Async_Except_Error(*args, **kwargs) -> Any:
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                logger = custom_logger or logging.getLogger(func.__name__)

                if log_message:
                    msg = log_message.format(func_name=func.__name__, error=str(e))
                else:
                    msg = f"异步函数 {func.__name__} 执行失败: {str(e)}"

                logger.log(log_level, msg, exc_info=True)

                if not suppress_exception:
                    raise

                return default_return

        # 根据函数类型返回对应包装器
        if asyncio.iscoroutinefunction(func):
            return Async_Except_Error
        else:
            return Except_Error

    return decorator
