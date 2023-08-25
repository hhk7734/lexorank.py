from typing_extensions import Self

from lexorank import integer
from lexorank.base import Base, Base36
from lexorank.integer import Integer, Sign

DECIMAL_POINT = ":"


class Decimal:
    def __init__(
        self, significant_figures: Integer, exponent: int, *, decimal_point: str = DECIMAL_POINT
    ) -> None:
        self._integer, self._exponent = self._rstrip(significant_figures, exponent)
        self._decimal_point = decimal_point

    @staticmethod
    def parse(value: str, base: Base = Base36, *, decimal_point: str = DECIMAL_POINT) -> "Decimal":
        try:
            index = value.index(decimal_point)
        except ValueError:
            return Decimal(integer.parse(value, base), 0, decimal_point=decimal_point)

        integer_str = value[:index] + value[index + 1 :]
        exponent = index - len(value) + 1
        return Decimal(integer.parse(integer_str, base), exponent, decimal_point=decimal_point)

    @property
    def base(self) -> Base:
        return self._integer.base

    @property
    def decimal_point(self) -> str:
        return self._decimal_point

    def __neg__(self) -> Self:
        return self.__class__(-self._integer, self._exponent)

    def __add__(self, other: Self) -> Self:
        if self._exponent == other._exponent:
            return self.__class__(self._integer + other._integer, self._exponent)

        lv = self
        rv = other
        if self._exponent < other._exponent:
            lv, rv = rv, lv

        diff = lv._exponent - rv._exponent
        lv._integer <<= diff
        lv._exponent -= diff

        return self.__class__(lv._integer + rv._integer, lv._exponent)

    def __sub__(self, other: Self) -> Self:
        return self + (-other)

    def __mul__(self, other: Self) -> Self:
        return self.__class__(self._integer * other._integer, self._exponent + other._exponent)

    def whole(self) -> Integer:
        if self._exponent < 0:
            return self._integer >> abs(self._exponent)
        return self._integer << self._exponent

    def to_base10(self) -> float:
        return int(self._integer) * (self.base.base() ** self._exponent)

    def __str__(self) -> str:
        sign = "" if self._integer.sign == Sign.POSITIVE else "-"
        intger_str = str(abs(self._integer))
        if self._exponent < 0:
            if len(intger_str) <= abs(self._exponent):
                intger_str = "0" * (abs(self._exponent) - len(intger_str) + 1) + intger_str
            return (
                sign
                + intger_str[: self._exponent]
                + self._decimal_point
                + intger_str[self._exponent :]
            )
        if self._exponent > 0:
            return sign + intger_str + "0" * self._exponent + self._decimal_point
        return sign + intger_str + self._decimal_point

    @staticmethod
    def _rstrip(value: Integer, exponent: int) -> tuple[Integer, int]:
        index = 0
        for digit in reversed(value.digits):
            if digit != 0:
                break
            index += 1

        return value >> index, exponent + index
