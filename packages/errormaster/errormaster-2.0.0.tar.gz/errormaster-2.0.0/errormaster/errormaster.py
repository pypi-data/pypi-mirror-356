import threading
import sys
import traceback
import types

_error_type = None
_original_trace = None
_original_excepthook = None


def _trace_calls(frame, event, arg):
    if event == 'exception':
        exc_type, exc_value, exc_traceback = arg
        global _error_type
        if _error_type is None or (
            isinstance(_error_type, tuple) and issubclass(exc_type, _error_type)
        ) or (_error_type is not None and issubclass(exc_type, _error_type)):
            tb = traceback.extract_tb(exc_traceback)
            if tb:
                last = tb[-1]
                location = f"line {last.lineno}"
                if last.name != '<module>':
                    location = f"function {last.name}"
            else:
                location = "unknown"
            print("Error occured!")
            print(f"Type : {exc_type.__name__}")
            print(f"Location : {location}")
            print(f"Description : {exc_value}")
            return None  # 예외를 무시하고 계속 진행
    return _trace_calls


def _custom_excepthook(exc_type, exc_value, exc_traceback):
    global _error_type, _original_excepthook
    if _error_type is None or (
        isinstance(_error_type, tuple) and issubclass(exc_type, _error_type)
    ) or (_error_type is not None and issubclass(exc_type, _error_type)):
        tb = traceback.extract_tb(exc_traceback)
        if tb:
            last = tb[-1]
            location = f"line {last.lineno}"
            if last.name != '<module>':
                location = f"function {last.name}"
        else:
            location = "unknown"
        print("Error occured!")
        print(f"Type : {exc_type.__name__}")
        print(f"Location : {location}")
        print(f"Description : {exc_value}")
        # 프로그램 종료하지 않음
    else:
        _original_excepthook(exc_type, exc_value, exc_traceback)


def start(error_type=None):
    """
    감지할 에러 타입을 지정하여 예외 감지 트레이스와 excepthook을 시작합니다.
    error_type이 None이면 모든 에러를 감지합니다.
    """
    global _error_type, _original_trace, _original_excepthook
    _error_type = error_type
    if _original_trace is None:
        _original_trace = sys.gettrace()
        sys.settrace(_trace_calls)
    if _original_excepthook is None:
        _original_excepthook = sys.excepthook
        sys.excepthook = _custom_excepthook


def stop():
    """
    예외 감지 트레이스와 excepthook을 종료합니다.
    """
    global _original_trace, _original_excepthook
    if _original_trace is not None:
        sys.settrace(_original_trace)
        _original_trace = None
    if _original_excepthook is not None:
        sys.excepthook = _original_excepthook
        _original_excepthook = None


class DoThis:
    def __enter__(self):
        pass
    def __exit__(self, exc_type, exc_value, exc_traceback):
        if exc_type is not None:
            tb = traceback.extract_tb(exc_traceback)
            if tb:
                last = tb[-1]
                location = f"line {last.lineno}"
                if last.name != '<module>':
                    location = f"function {last.name}"
            else:
                location = "unknown"
            print("Error occured!")
            print(f"Type : {exc_type.__name__}")
            print(f"Location : {location}")
            print(f"Description : {exc_value}")
            return True  # 예외 무시
        return False

do_this = DoThis()
