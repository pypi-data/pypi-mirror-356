#!/usr/bin/env python
import argparse
import logging
import os
import shutil
import subprocess
import sys
import threading
from pathlib import Path
from typing import Union

from ltpylib import opts

LOG_FORMAT_PART_LEVEL = "{levelname:<8}"
LOG_FORMAT_PART_MESSAGE = "{message}"
LOG_FORMAT_PART_TIMESTAMP = "{asctime}"

DEFAULT_LOG_LEVEL = logging.INFO
DEFAULT_LOG_FORMAT = f"{LOG_FORMAT_PART_MESSAGE}"
DEFAULT_LOG_STYLE = "{"
LOG_SEP = "----------------------------------------------------------------------------------------------------------------------------------"

LOG_FORMAT_WITH_LEVEL = f"{LOG_FORMAT_PART_LEVEL} {LOG_FORMAT_PART_MESSAGE}"
LOG_FORMAT_WITH_TIMESTAMP = f"[{LOG_FORMAT_PART_TIMESTAMP}] {LOG_FORMAT_PART_MESSAGE}"


# see https://stackoverflow.com/questions/21953835/run-subprocess-and-print-output-to-logging
class LogPipe(threading.Thread):

  def __init__(self, level: int = logging.INFO):
    threading.Thread.__init__(self)
    self.daemon = False
    self.level = level
    self.fd_read, self.fd_write = os.pipe()
    self.pipe_reader = os.fdopen(self.fd_read)
    self.start()

  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_value, exc_tb):
    self.close()

  def fileno(self):
    return self.fd_write

  def run(self):
    for line in iter(self.pipe_reader.readline, ''):
      logging.log(self.level, line.strip('\n'))

    self.pipe_reader.close()

  def close(self):
    os.close(self.fd_write)

  def write(self, message):
    logging.log(self.level, message)

  def flush(self):
    pass


class StderrStreamHandler(logging.StreamHandler):

  def __init__(self):
    super().__init__(stream=sys.stderr)

  def handleError(self, record):
    err_type, err_value, traceback = sys.exc_info()
    if err_type == BrokenPipeError:
      exit(0)

    super().handleError(record)


class StdoutStreamHandler(logging.StreamHandler):

  def __init__(self):
    super().__init__(stream=sys.stdout)

  def handleError(self, record):
    err_type, err_value, traceback = sys.exc_info()
    if err_type == BrokenPipeError:
      exit(0)

    super().handleError(record)


def init_logging(
  verbose: bool = None,
  quiet: bool = None,
  log_level: Union[int, str] = None,
  log_format: str = None,
  args: Union[argparse.Namespace, opts.BaseArgs] = None,
  use_stderr: bool = False,
):
  if args:
    if verbose is None and hasattr(args, "verbose"):
      verbose = args.verbose
    if log_level is None and hasattr(args, "log_level"):
      log_level = args.log_level
    if log_format is None and hasattr(args, "log_format"):
      log_format = args.log_format
    if quiet is None and hasattr(args, "quiet"):
      quiet = args.quiet

  if verbose:
    log_level = logging.DEBUG
  elif quiet:
    log_level = logging.WARNING
  elif log_level is not None:
    log_level = log_level
  elif os.environ.get("log_level") is not None:
    log_level = os.environ.get("log_level")
  else:
    log_level = DEFAULT_LOG_LEVEL

  log_config_kwargs = {
    "style": DEFAULT_LOG_STYLE,
    "handlers": [StderrStreamHandler() if use_stderr else StdoutStreamHandler()],
  }
  logging.basicConfig(
    level=log_level,
    format=log_format if log_format else DEFAULT_LOG_FORMAT,
    **log_config_kwargs,
  )


def add_file_logging(log_file: Path):
  if not log_file.parent.exists():
    log_file.parent.mkdir(parents=True)

  root_logger = logging.getLogger()

  file_handler = logging.FileHandler(log_file.as_posix())
  file_handler.setFormatter(root_logger.handlers[0].formatter)

  root_logger.addHandler(file_handler)


def is_debug_enabled():
  return logging.root.isEnabledFor(logging.DEBUG)


def log_sep(debug_only=False):
  if debug_only:
    logging.debug(LOG_SEP)
  else:
    logging.info(LOG_SEP)


def create_path_log_info(path: Path, replace_home_dir: bool = True) -> str:
  output = path.as_posix()

  if replace_home_dir:
    output = output.replace(os.getenv('HOME'), '~', 1)

  return output


def log_with_sep(msg, *args, level: int = logging.INFO, **kwargs):
  logging.log(level, LOG_SEP)
  logging.log(level, msg, *args, **kwargs)
  logging.log(level, LOG_SEP)


def log_with_title_sep(title, *args, msg=None, level: int = logging.INFO, **kwargs):
  logging.log(level, title)
  logging.log(level, LOG_SEP)
  if msg is not None:
    logging.log(level, msg, *args, **kwargs)
    logging.log(level, '')


def log_title_with_sep(title, level: int = logging.INFO):
  logging.log(level, title)
  logging.log(level, LOG_SEP)


def ltlogs_dir() -> Path:
  return Path(os.getenv("LTLOGS_DIR", os.path.expanduser("~/Library/Logs/lt_logs")))


def tail_log_file(file: str, *func_args):
  if shutil.which('multitail'):
    log_cmd = ['multitail']
    mt_conf = Path(os.getenv('DOTFILES') + '/multitail.conf')
    if '-F' not in func_args and mt_conf.is_file():
      log_cmd.extend(['-F', mt_conf.as_posix()])

    if '-CS' not in func_args:
      log_cmd.extend(['-CS', 'l4j'])

    if '-n' not in func_args:
      log_cmd.extend(['-n', '1500'])

  else:
    log_cmd = ['tail', '-1500f']

  if func_args:
    log_cmd.extend(func_args)

  log_cmd.append(file)

  subprocess.check_call(log_cmd, universal_newlines=True)


def _main():
  import sys

  result = globals()[sys.argv[1]](*sys.argv[2:])
  if result is not None:
    print(result)


if __name__ == "__main__":
  try:
    _main()
  except KeyboardInterrupt:
    exit(130)
