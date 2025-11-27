from enum import IntEnum
from functools import lru_cache

from typing_extensions import Self

from lexorank import decimal
from lexorank.base import Base, Base36
from lexorank.decimal import DECIMAL_POINT, Decimal
from lexorank.integer import Integer

BUCKET_SEPARATOR = "|"
WHOLE_NUMBER_SIZE = 6


class Bucket(IntEnum):
    BUCKET_0 = 0
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
        return self.__class__(
            self._bucket,
            Decimal(self._rank.whole_number(), 0, decimal_point=self._rank.decimal_point) + step,
            bucket_separator=self._bucket_separator,
            whole_number_size=self._whole_number_size,
        )

    def __add__(self, other: object) -> Self:
        other = self._type_guard(other)

        return self.__class__(
            self._bucket,
            self._rank + other._rank,
            bucket_separator=self._bucket_separator,
            whole_number_size=self._whole_number_size,
        )

    def __sub__(self, other: object) -> Self:
        other = self._type_guard(other)

        return self.__class__(
            self._bucket,
            self._rank - other._rank,
            bucket_separator=self._bucket_separator,
            whole_number_size=self._whole_number_size,
        )

    def __mul__(self, other: object) -> Self:
        other = self._type_guard(other)

        return self.__class__(
            self._bucket,
            self._rank * other._rank,
            bucket_separator=self._bucket_separator,
            whole_number_size=self._whole_number_size,
        )

    def __eq__(self, other: object) -> bool:
        other = self._type_guard(other)

        return self._bucket == other._bucket and self._rank == other._rank

    def __gt__(self, other: object) -> bool:
        other = self._type_guard(other)

        if self._bucket.value > other._bucket.value:
            return True
        if self._bucket.value < other._bucket.value:
            return False
        return self._rank > other._rank

    def __ge__(self, other: object):
        return self.__gt__(other) or self.__eq__(other)

    def __lt__(self, other: object):
        return not self.__ge__(other)

    def __le__(self, other: object):
        return not self.__gt__(other)

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

    def __float__(self) -> float:
        return float(self._rank)

    def __int__(self) -> int:
        return int(self._rank)

    def _type_guard(self, other: object) -> "LexoRank":
        if isinstance(other, LexoRank):
            return other
        if isinstance(other, str):
            return parse(
                other,
                self._rank.base,
                decimal_point=self._rank.decimal_point,
                bucket_separator=self._bucket_separator,
                whole_number_size=self._whole_number_size,
            )
        if isinstance(other, (int, float, Integer)):
            return LexoRank(self._bucket, decimal.parse(other, self._rank.base))
        if isinstance(other, Decimal):
            return LexoRank(self._bucket, other)
        raise ValueError(f"unsupported operand type(s) {type(other)}")


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


def between(a: LexoRank | None, b: LexoRank | None) -> LexoRank:
    if a is None:
        if b is None:
            raise ValueError("a and b cannot be None at the same time")
        return b.prev()
    if b is None:
        return a.next()

    if a > b:
        a, b = b, a
    mid = (a + b) * 0.5
    if int(a) < int(mid) < int(b):
        return LexoRank(a.bucket, decimal.parse(mid.rank.whole_number()))

    # TODO: shorten the length of the decimal part
    return mid
