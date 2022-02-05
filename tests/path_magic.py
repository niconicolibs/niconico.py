
from sys import stdout, stderr, path
import logging


path.insert(0, __file__[:-20])


def setStdoutLogger(name=None):
    "標準出力をするように指定された名前のLoggerを設定する。"
    # FROM: https://techblog.sasashima.works/archives/229
    stdout_handler = logging.StreamHandler(stream=stdout)
    stdout_handler.setFormatter(fmt:=logging.Formatter("[%(levelname)s] %(message)s"))
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.addFilter(lambda record: record.levelno <= logging.INFO)
    stderr_handler = logging.StreamHandler(stream=stderr)
    stderr_handler.setFormatter(fmt)
    stderr_handler.setLevel(logging.WARNING)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(stdout_handler)
    logger.addHandler(stderr_handler)


setStdoutLogger("niconico.py")