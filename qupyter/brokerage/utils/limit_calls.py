import time


_MAX_CALLS = 5
_PERIOD = 1
_SCOPE = 'default'


class CallLimiter:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CallLimiter, cls).__new__(cls)
            cls._instance.windows = {'default': []}

        return cls._instance


    def wait_limit_rate(self, max_calls: int = _MAX_CALLS, period: float = _PERIOD, scope: str = _SCOPE):
        if scope not in self.windows:
            self.windows[scope] = []

        now = time.time()
        window = list(filter(lambda x: now - x < period, self.windows[scope]))
        window_size = len(window)

        if window_size >= max_calls:
            time.sleep(period)
        elif window_size > 0:
            time.sleep(period / max_calls)

        window.append(time.time())
        self.windows[scope] = window


def limit_calls(max_calls: int = _MAX_CALLS, period: float = _PERIOD, scope: str = _SCOPE):
    """
    여러 함수에 대한 호출을 제한하는 데코레이터입니다.

    Args:
        max_calls (int): 최대 호출 횟수
        period (float): 기간(초) 동안의 호출 횟수를 제한합니다.
        scope (str): 호출 제한을 적용할 스코프 이름입니다.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            CallLimiter().wait_limit_rate(max_calls=max_calls, period=period, scope=scope)
            result = func(*args, **kwargs)
            return result

        return wrapper

    return decorator
