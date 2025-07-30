"""
Simple opinionated defaults for Python logging, with minimalist formatting,
anti-logspam measures and other minor tweaks.

Activated with ok_logging_setup.install().
"""

import datetime
import io
import logging
import os
import re
import signal
import sys
import threading
import typing
import unicodedata
import zoneinfo

ENV_LEVEL_RE = re.compile(r"(?i)\s*((?P<module>[\w.]+)\s*=)?\s*(?P<level>\w+)")
TASK_IGNORE_RE = re.compile(r"(|Task-\d+)")
THREAD_IGNORE_RE = re.compile(r"(|MainThread|Thread-\d+)")

_logger = logging.getLogger(__name__)  # very meta
_repeat_per_minute = 10  # max per message 'signature' (format minus digits)
_skip_traceback_for: tuple[typing.Type[BaseException], ...] = ()
_time_format = ""
_timezone = None


def install(*, env_defaults: typing.Dict[str, str]={}):
    """
    Sets up Python logging the ok_logging_setup way. Must be called without
    any other logging handlers added. See README.md for full documentation.

    :param env_defaults: Default environment variables for configuration.
    """

    if logging.root.handlers:
        raise RuntimeError("ok_logging_setup install after logging configured")

    signal.signal(signal.SIGINT, signal.SIG_DFL)  # sane ^C handling by default

    log_handler = logging.StreamHandler(stream=sys.stderr)
    log_handler.setFormatter(_LogFormatter())
    log_handler.addFilter(_LogFilter())
    logging.basicConfig(level=logging.INFO, handlers=[log_handler])

    sys.excepthook = _sys_exception_hook
    sys.unraisablehook = _sys_unraisable_hook
    threading.excepthook = _thread_exception_hook
    if isinstance(sys.stdout, io.TextIOWrapper):
        sys.stdout.reconfigure(line_buffering=True)  # log prints immediately
    _configure({**env_defaults, **os.environ})


def exit(msg: str, *args, code: int=1, **kw):
    """
    Log a critical error (no stack) with the root logger, then exit the process.
    Typically used as a convenient error-and-exit for CLI utilities.
    """

    logging.critical(msg, *args, **kw)
    raise SystemExit(code)


def skip_traceback_for(klass: typing.Type[BaseException]):
    """
    Add to the list of exception classes where tracebacks are suppressed
    in regular logging or when handling uncaught exceptions. Good for
    exceptions with self-evident causes where stack traces are noise.
    """

    if not issubclass(klass, BaseException):
        raise TypeError(f"Bad skip_traceback_for value {klass!r}")

    global _skip_traceback_for
    if not issubclass(klass, _skip_traceback_for):
        _skip_traceback_for += (klass,)


class _LogFormatter(logging.Formatter):
    def format(self, rec: logging.LogRecord):
        m = rec.getMessage()
        ml = m.lstrip()
        out = ml.rstrip()
        pre, post = m[: len(m) - len(ml)], ml[len(out) :]
        if not THREAD_IGNORE_RE.fullmatch(rec.threadName or ""):
            out = f"<{rec.threadName}> {out}"
        if not TASK_IGNORE_RE.fullmatch(getattr(rec, "taskName", "") or ""):
            out = f"[{getattr(rec, 'taskName')}] {out}"
        if rec.name != "root":
            out = f"{rec.name}: {out}"
        if rec.levelno < logging.INFO:
            out = f"🕸  {out}"  # skip _starts_with_emoji for performance?
        elif rec.levelno >= logging.CRITICAL:
            if not _starts_with_emoji(out):
                out = f"💥 {out}"
        elif rec.levelno >= logging.ERROR:
            if not _starts_with_emoji(out):
                out = f"🔥 {out}"
        elif rec.levelno >= logging.WARNING:
            if not _starts_with_emoji(out):
                out = f"⚠️ {out}"
        if _time_format:
            dt = datetime.datetime.fromtimestamp(rec.created, _timezone)
            out = f"{dt.strftime(_time_format)} {out}"
        exc, stack = rec.exc_info, rec.stack_info
        if exc and exc[0] and issubclass(exc[0], _skip_traceback_for):
            exc = (exc[0], exc[1], None)
            stack = None
        if exc:
            out = f"{out.rstrip()}\n{self.formatException(exc)}"
        if stack:
            out = f"{out.rstrip()}\nStack:\n{stack}"
        return pre + out.strip() + post


class _LogFilter(logging.Filter):
    DIGITS = re.compile("[0-9]+")

    def __init__(self):
        super().__init__()
        self._last_minute = 0
        self._recently_seen = {}

    def filter(self, record: logging.LogRecord):
        minute = record.created // 60
        if minute != self._last_minute:
            self._recently_seen.clear()
            self._last_minute = minute

        if _repeat_per_minute <= 0:
            return True  # suppression disabled

        sig = _LogFilter.DIGITS.sub("#", str(record.msg))
        count = self._recently_seen.get(sig, 0)
        if count < 0:
            return False  # already suppressed
        elif count < _repeat_per_minute:
            self._recently_seen[sig] = count + 1
            return True
        else:
            self._recently_seen[sig] = -1  # suppressed until minute tick
            until_sec = (minute + 1) * 60
            until_dt = datetime.datetime.fromtimestamp(until_sec, _timezone)
            old_message = record.getMessage()
            record.msg = "%s [suppressing until %02d:%02d]"
            record.args = (old_message, until_dt.hour, until_dt.minute)
            return True


def _configure(env):
    for env_level in env.pop("OK_LOGGING_LEVEL", "").split(","):
        if env_match := ENV_LEVEL_RE.fullmatch(env_level):
            module = env_match.group("module")
            level = env_match.group("level").upper()
            logger = logging.getLogger(module) if module else logging.root
            try:
                logger.setLevel(level)
            except ValueError:
                _logger.warning(f'Bad $OK_LOGGING_LEVEL level "{level}"')
        elif env_level.strip():
            _logger.warning(f'Bad $OK_LOGGING_LEVEL entry "{env_level}"')

    if env_repeat := env.pop("OK_LOGGING_REPEAT_PER_MINUTE", ""):
        try:
            _repeat_per_minute = int(env_repeat)
        except ValueError:
            _logger.warning(f'Bad $OK_LOGGING_REPEAT_PER_MINUTE "{env_repeat}"')

    global _time_format, _timezone
    if _time_format := env.pop("OK_LOGGING_TIME_FORMAT", ""):
        if env_timezone := env.pop("OK_LOGGING_TIMEZONE", ""):
            try:
                _timezone = zoneinfo.ZoneInfo(env_timezone)
            except zoneinfo.ZoneInfoNotFoundError:
                _logger.warning(f'Bad $OK_LOGGING_TIMEZONE "{env_timezone}"')

    for key, value in env.items():
        if key.upper().startswith("OK_LOGGING") and value:
            _logger.warning("Unknown variable $%s=%s", key, value)


def _starts_with_emoji(str):
    return unicodedata.category(str[:1]) == "So"


def _sys_exception_hook(exc_type, exc_value, exc_tb):
    if issubclass(exc_type, KeyboardInterrupt):
        logging.critical("\n❌ KeyboardInterrupt (^C)! ❌")
    else:
        exc_info = (exc_type, exc_value, exc_tb)
        logging.critical("Uncaught exception", exc_info=exc_info)

    # after return, the python runtime will execute atexit handlers and exit


def _sys_unraisable_hook(unr):
    if unr.err_msg:
        logging.critical("%s: %s", unr.err_msg, repr(unr.object))
    else:
        exc_info = (unr.exc_type, unr.exc_value, unr.exc_traceback)
        logging.critical("Uncatchable exception", exc_info=exc_info)

    # the python runtime would continue, instead exit the program by policy
    # (this does unfortunately bypass atexit handlers)
    os._exit(1)  # pylint: disable=protected-access


def _thread_exception_hook(args):
    exc_info = (args.exc_type, args.exc_value, args.exc_traceback)
    logging.critical("Uncaught exception in thread", exc_info=exc_info)

    # otehr threads would continue, instead exit the whole program by policy
    # (this does unfortunately bypass atexit handlers)
    os._exit(1)  # pylint: disable=protected-access
