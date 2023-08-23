from typing_extensions import Self

from lexorank.integer import Integer

DECIMAL_POINT = ":"


class Decimal:
    def __init__(self, integer: Integer, exponent: int, decimal_point=DECIMAL_POINT) -> None:
        self._integer = integer
        self._exponent = exponent
        self._decimal_point = decimal_point

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
        return self._integer.to_base10() * (self._integer.base**self._exponent)

    def __str__(self) -> str:
        integer = str(self._integer)
        if self._exponent < 0:
            if len(integer) < abs(self._exponent):
                integer = "0" * (abs(self._exponent) - len(integer) + 1) + integer
            return integer[: self._exponent] + self._decimal_point + integer[self._exponent :]
        if self._exponent > 0:
            return integer + "0" * self._exponent
        return integer
