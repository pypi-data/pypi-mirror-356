import traceback
import sys
from functools import wraps
import inspect


def log_on_exception(logger=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                stack_lines = traceback.format_exc().splitlines(keepends=True)
                if len(stack_lines) > 40:
                    stack_summary = ''.join(stack_lines[:20]) + '\n...\n' + ''.join(stack_lines[-20:])
                else:
                    stack_summary = ''.join(stack_lines)
                error_info = {
                    '函数': func.__name__,
                    '模块': func.__module__,
                    '类型': type(e).__name__,
                    '消息': str(e),
                    '签名': str(inspect.signature(func)),
                    'args': [str(arg) for arg in args] if args else [],
                    'kwargs': {k: str(v) for k, v in kwargs.items()} if kwargs else {},
                    '函数文件': func.__code__.co_filename,
                    '函数行号': func.__code__.co_firstlineno,
                    '异常行号': traceback.extract_tb(sys.exc_info()[2])[-1].lineno if sys.exc_info()[2] else None,
                    '异常文件': traceback.extract_tb(sys.exc_info()[2])[-1].filename if sys.exc_info()[2] else None,
                    '堆栈': stack_summary,
                }
                if logger:
                    logger.error(f"执行失败", {'details': error_info})

                # print(error_info)
                # raise  # 重新抛出异常
                
                return None  # 或者返回其他默认值
        
        return wrapper
    return decorator


def log_on_exception_with_retry(max_retries=3, delay=1, logger=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    import time
                    last_exception = e
                    error_info = {
                        '函数': func.__name__,
                        '重试': attempt + 1,
                        '最大重试': max_retries,
                        '类型': type(e).__name__,
                        '消息': str(e),
                    }
                    
                    if logger:
                        logger.warning(f"函数 {func.__name__} 第 {attempt + 1} 次尝试失败", {'details': error_info})
                    
                    if attempt < max_retries - 1:
                        time.sleep(delay)
                        if logger:
                            logger.info(f"⏳ 第 {attempt + 1} 次尝试失败，{delay}秒后重试...")
                    else:
                        if logger:
                            logger.error(f"❌ 函数 {func.__name__} 在 {max_retries} 次尝试后仍然失败")
            
            final_error_info = {
                '函数': func.__name__,
                '最终错误类型': type(last_exception).__name__,
                '最终错误消息': str(last_exception),
                '总尝试次数': max_retries,
                '堆栈跟踪': traceback.format_exc(),
            }
            
            if logger:
                logger.error(f"函数 {func.__name__} 最终执行失败", {'details': final_error_info})
            
            return None
            
        return wrapper
    return decorator


if __name__ == "__main__":
    import logging
    test_logger = logging.getLogger(__name__)
    test_logger.setLevel(logging.INFO)
    
    @log_on_exception(logger=test_logger)
    def divide_numbers(a, b):
        """测试函数：除法运算"""
        return a / b
    
    @log_on_exception_with_retry(max_retries=2, delay=0.5, logger=test_logger)
    def fetch_data(url):
        import random
        """测试函数：模拟数据获取"""
        if random.random() < 0.7:  # 70% 概率失败
            raise ConnectionError("网络连接失败")
        return "数据获取成功"
    
    # 测试基本错误处理
    print("=== 测试基本错误处理 ===")
    result1 = divide_numbers(10, 0)
    result2 = divide_numbers(10, 2)
    print(f"结果: {result2}")
    
    print("\n=== 测试重试机制 ===")
    result3 = fetch_data("http://example.com")
    print(f"最终结果: {result3}") 