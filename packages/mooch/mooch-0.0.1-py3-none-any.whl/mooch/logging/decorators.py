import asyncio
import functools
import logging

logger = logging.getLogger(__name__)


def log_begin_and_end(func: callable):  # noqa: ANN201
    @functools.wraps(func)
    def run_func(*args, **kwargs):  # noqa: ANN002, ANN003, ANN202
        logger.log(msg=f"BEGIN: {func.__qualname__}()", level=5)
        logger.log(msg=f"Args: {args + tuple(f'{key} = {val}' for key, val in kwargs.items())}", level=5)
        result = func(*args, **kwargs)
        logger.log(msg=f"END: {func.__qualname__}()", level=5)
        return result

    async def async_run_func(*args, **kwargs):  # noqa: ANN002, ANN003, ANN202
        logger.log(msg=f"BEGIN: {func.__qualname__}()", level=5)
        logger.log(msg=f"Args: {args + tuple(f'{key} = {val}' for key, val in kwargs.items())}", level=5)
        result = await func(*args, **kwargs)
        logger.log(msg=f"END: {func.__qualname__}", level=5)
        return result

    return async_run_func if asyncio.iscoroutinefunction(func) else run_func
