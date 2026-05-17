"""1c-batch — кроссплатформенный инструмент для пакетных операций с 1С:Предприятие 8."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("1c-batch")
except PackageNotFoundError:
    __version__ = "0.0.0+unknown"
