from enum import IntEnum

from typing_extensions import Self

from lexorank.base import Base, Base36


class Sign(IntEnum):
    POSITIVE = 1
    NEGATIVE = -1

    def __neg__(self) -> Self:
        return self.__class__(-self.value)

    def __mul__(self, other: Self) -> Self:  # type: ignore[override]
        return self.__class__(self.value * other.value)


class Integer:
    def __init__(self, digits: list[int], sign: Sign = Sign.POSITIVE, base: Base = Base36) -> None:
        self._digits = self._lstrip(digits)
        self._sign = sign
        self._base = base

    @property
    def digits(self) -> list[int]:
        return self._digits.copy()

    @property
    def sign(self) -> Sign:
        return self._sign

    @property
    def base(self) -> Base:
        return self._base

    def __neg__(self) -> Self:
        return self.__class__(self._digits.copy(), -self._sign, self._base)

    def __abs__(self) -> Self:
        return self.__class__(self._digits.copy(), Sign.POSITIVE, self._base)

    def __add__(self, other: object) -> Self:
        other = self._type_guard(other)

        if self._sign != other._sign:
            return self - (-other)

        rdigits = []
        carry = 0

        for i in range(max(len(self), len(other))):
            a = self._digits[-i - 1] if i < len(self) else 0
            b = other._digits[-i - 1] if i < len(other) else 0

            result = a + b + carry
            carry = result // self._base.base()
            rdigits.append(result % self._base.base())

        if carry:
            rdigits.append(carry)

        return self.__class__(list(reversed(rdigits)), self._sign, self._base)

    def __sub__(self, other: object) -> Self:
        other = self._type_guard(other)

        if self._sign != other._sign:
            return self + (-other)

        a: Integer = self
        b = other
        sign = self._sign
        if len(a) < len(b):
            a, b = b, a
            sign = -sign

        complement = [35] * len(a)
        for i in range(len(b)):
            complement[-i - 1] = 35 - b._digits[-i - 1]

        rdigits = []
        carry = 1
        base = self._base.base()

        for i in range(len(a)):
            ad = a._digits[-i - 1]
            bd = complement[-i - 1]

            result = ad + bd + carry
            carry = result // base
            rdigits.append(result % base)

        return self.__class__(list(reversed(rdigits)), sign)

    def __mul__(self, other: object) -> Self:
        other = self._type_guard(other)

        rdigits = [0] * (len(self) + len(other))

        for i in range(len(self)):
            for j in range(len(other)):
                index = i + j
                ret = rdigits[index] + self._digits[-i - 1] * other._digits[-j - 1]
                rdigits[index] = ret % self._base.base()
                rdigits[index + 1] += ret // self._base.base()

        return self.__class__(list(reversed(rdigits)), self._sign * other._sign, self._base)

    def __lshift__(self, other: int) -> Self:
        if other < 0:
            raise ValueError("shift count must be non-negative")
        digits = self._digits + [0] * other
        return self.__class__(digits, self._sign, self._base)

    def __rshift__(self, other: int) -> Self:
        if other < 0:
            raise ValueError("shift count must be non-negative")
        return self.__class__(self._digits[: len(self) - other], self._sign, self._base)

    def __eq__(self, other: object):
        other = self._type_guard(other)

        if len(self) != len(other):
            return False
        if len(self) == 0:
            return True
        if self._sign != other._sign:
            return False
        for a, b in zip(self._digits, other._digits):
            if a != b:
                return False
        return True

    def __gt__(self, other: object):
        other = self._type_guard(other)

        if len(self) == 0 and len(other) == 0:
            return False
        if self._sign > other._sign:
            return True
        if self._sign < other._sign:
            return False
        if len(self) > len(other):
            return self._sign == Sign.POSITIVE
        if len(self) < len(other):
            return self._sign == Sign.NEGATIVE
        for a, b in zip(self._digits, other._digits):
            if a > b:
                return self._sign == Sign.POSITIVE
            if a < b:
                return self._sign == Sign.NEGATIVE
        return False

    def __ge__(self, other: object):
        return self.__gt__(other) or self.__eq__(other)

    def __lt__(self, other: object):
        return not self.__ge__(other)

    def __le__(self, other: object):
        return not self.__gt__(other)

    def __str__(self) -> str:
        if len(self) == 0:
            return "0"

        num = "".join([self._base.from_base10(digit) for digit in self._digits])
        return f"{'-' if self._sign == Sign.NEGATIVE else ''}{num}"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} value={self.__str__()}, base={self._base.base()}>"

    def __int__(self) -> int:
        value = 0
        for digit in self._digits:
            value = value * self._base.base() + digit
        return self._sign.value * value

    def __len__(self) -> int:
        return len(self._digits)

    @staticmethod
    def _lstrip(digits: list[int]) -> list[int]:
        for i, digit in enumerate(digits):
            if digit != 0:
                return digits[i:]

        return []

    def _type_guard(self, other: object) -> "Integer":  # type: ignore[return-value]
        if isinstance(other, (int, str)):
            return parse(other, self._base)
        if isinstance(other, Integer):
            return other
        raise ValueError(f"unsupported operand type(s) {type(other)}")


def parse(value: str | int, base: Base = Base36) -> Integer:
    if isinstance(value, int):
        sign = Sign.POSITIVE if value >= 0 else Sign.NEGATIVE
        value = abs(value)

        rdigits = []
        while value > 0:
            rdigits.append(value % base.base())
            value //= base.base()

        return Integer(list(reversed(rdigits)), sign, base)

    sign = Sign.POSITIVE if value[0] != "-" else Sign.NEGATIVE
    if value[0] in ("+", "-"):
        value = value[1:]

    digits = [base.to_base10(digit) for digit in value]
    return Integer(digits, sign, base)
