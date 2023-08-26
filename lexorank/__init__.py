from importlib.metadata import PackageNotFoundError, version

from lexorank.lexorank import (
    BUCKET_SEPARATOR,
    DECIMAL_POINT,
    WHOLE_NUMBER_SIZE,
    Bucket,
    LexoRank,
    middle,
    parse,
)

try:
    __version__ = version("loggingx-py")

except PackageNotFoundError:
    pass
