from enum import IntEnum
from functools import lru_cache

from typing_extensions import Self

from lexorank import decimal
from lexorank.base import Base, Base36
from lexorank.decimal import DECIMAL_POINT, Decimal

BUCKET_SEPARATOR = "|"
WHOLE_NUMBER_SIZE = 6


class Bucket(IntEnum):
    BUCEKT_0 = 0
    BUCKET_1 = 1
    BUCKET_2 = 2

    def next(self) -> Self:
        return self.__class__((self.value + 1) % 3)


class LexoRank:
    def __init__(
        self,
        bucekt: Bucket,
        rank: Decimal,
        *,
        bucket_separator: str = BUCKET_SEPARATOR,
        whole_number_size: int = WHOLE_NUMBER_SIZE,
    ) -> None:
        self._bucket = bucekt
        self._rank = rank
        self._bucket_separator = bucket_separator
        self._whole_number_size = whole_number_size

    @property
    def bucket(self) -> Bucket:
        return self._bucket

    @property
    def rank(self) -> Decimal:
        return self._rank

    def prev(self, step: int = 16) -> Self:
        return self.next(-step)

    def next(self, step: int = 16) -> Self:
        return self.__class__(self._bucket, self._rank + step)

    def __str__(self) -> str:
        rank = str(self._rank)
        index = rank.index(self._rank.decimal_point)

        whole = rank[:index].zfill(self._whole_number_size)
        rank = rank[index + 1 :]

        return (
            f"{self._bucket.value}{self._bucket_separator}{whole}{self._rank.decimal_point}{rank}"
        )

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} value={self} base={self._rank.base.base()}>"


def parse(
    value: str,
    base: Base = Base36,
    *,
    decimal_point: str = DECIMAL_POINT,
    bucket_separator: str = BUCKET_SEPARATOR,
    whole_number_size: int = WHOLE_NUMBER_SIZE,
) -> LexoRank:
    if value[1] != bucket_separator or value[2 + whole_number_size] != decimal_point:
        raise ValueError(f"invalid lexorank format: {value}")

    bucket = Bucket(int(value[0]))
    decimal_ = decimal.parse(value[2:], base, decimal_point=decimal_point)
    return LexoRank(
        bucket, decimal_, bucket_separator=bucket_separator, whole_number_size=whole_number_size
    )


@lru_cache()
def middle(
    bucket: Bucket,
    base: Base = Base36,
    *,
    decimal_point: str = DECIMAL_POINT,
    bucket_separator: str = BUCKET_SEPARATOR,
    whole_number_size: int = WHOLE_NUMBER_SIZE,
) -> LexoRank:
    max_decimal = decimal.parse("1" + "0" * whole_number_size, base, decimal_point=decimal_point)
    return LexoRank(
        bucket,
        max_decimal * 0.5,
        bucket_separator=bucket_separator,
        whole_number_size=whole_number_size,
    )
