from enum import IntEnum

from typing_extensions import Self

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
        decimal: Decimal,
        *,
        bucket_separator: str = BUCKET_SEPARATOR,
        whole_number_size: int = WHOLE_NUMBER_SIZE,
    ) -> None:
        self._bucket = bucekt
        self._decimal = decimal
        self._bucket_separator = bucket_separator
        self._whole_number_size = whole_number_size

    @staticmethod
    def parse(
        value: str,
        base: Base = Base36,
        *,
        decimal_point: str = DECIMAL_POINT,
        bucket_separator: str = BUCKET_SEPARATOR,
        whole_number_size: int = WHOLE_NUMBER_SIZE,
    ) -> "LexoRank":
        if value[1] != bucket_separator or value[2 + whole_number_size] != decimal_point:
            raise ValueError(f"invalid lexorank format: {value}")

        bucket = Bucket(int(value[0]))
        decimal = Decimal.parse(value[2:], base, decimal_point=decimal_point)
        return LexoRank(
            bucket, decimal, bucket_separator=bucket_separator, whole_number_size=whole_number_size
        )

    @property
    def bucket(self) -> Bucket:
        return self._bucket

    @property
    def decimal(self) -> Decimal:
        return self._decimal

    def __str__(self) -> str:
        decimal = str(self._decimal)
        index = decimal.index(self._decimal.decimal_point)

        whole = decimal[:index].zfill(self._whole_number_size)
        decimal = decimal[index + 1 :]

        return f"{self._bucket.value}{self._bucket_separator}{whole}{self._decimal.decimal_point}{decimal}"
