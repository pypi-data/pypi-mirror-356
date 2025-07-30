import logging
import os
import threading
import time
from pathlib import Path
from typing import Callable, List

_LOGGER = logging.getLogger("aihub.stop")

_ENV_KEY = "PRE_STOP_SENTINEL_FILE"
_DEFAULT_SENTINEL = "/tmp/pre_stop_sentinel_file"

_sentinel_path = Path(os.getenv(_ENV_KEY, _DEFAULT_SENTINEL))
_flag: bool = False  # cached result
_callbacks: List[Callable[[], None]] = []
_watch_started: bool = False  # ensure single watcher


def _check() -> bool:
    global _flag
    if not _flag and _sentinel_path.exists():
        _flag = True
        _trigger_callbacks()
    return _flag


def _trigger_callbacks() -> None:
    for cb in _callbacks:
        try:
            cb()
        except Exception as exc:
            _LOGGER.exception("aihub callback raised: %s", exc, exc_info=exc)


def is_pre_stopped() -> bool:
    return _check()


def on_pre_stop(func: Callable[[], None], *, poll_interval: float = 1.0) -> None:
    global _watch_started
    _callbacks.append(func)
    if _watch_started:
        return

    def _watch() -> None:
        while not _check():
            time.sleep(poll_interval)

    threading.Thread(target=_watch, daemon=True, name="aihub-stop-watcher").start()
    _watch_started = True
