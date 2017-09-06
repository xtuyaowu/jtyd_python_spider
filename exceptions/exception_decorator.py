import traceback
from functools import wraps

from logger.log import other as logger

def try_except_to_error(e, platform):
    def try_except(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                return result
            except:
                logger.error(traceback.format_exc())
                raise e(traceback.format_exc(), platform)
        return wrapper
    return try_except