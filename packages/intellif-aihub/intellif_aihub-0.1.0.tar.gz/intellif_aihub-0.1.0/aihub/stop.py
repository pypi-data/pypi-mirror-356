import os
import time
from pathlib import Path
from typing import Callable, List

_SENTINEL = Path(os.getenv("PRE_STOP_FILE", "/tmp/pre_stop"))
_flag = False  # 缓存，防止反复读取 I/O
_callbacks: List[Callable[[], None]] = []


def _check_file() -> bool:
    global _flag
    if not _flag and _SENTINEL.exists():
        _flag = True
        for cb in _callbacks:
            try:
                cb()
            except Exception as e:
                print(f"[aihub] callback error: {e}", flush=True)
    return _flag


def receive_stop_command() -> bool:
    return _check_file()


def register_callback(func: Callable[[], None]) -> None:
    _callbacks.append(func)
    import threading
    def _watch():
        while True:
            if _check_file():
                break
            time.sleep(1)

    threading.Thread(target=_watch, daemon=True).start()
