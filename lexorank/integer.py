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
    def __init__(
        self, reversed_digits: list[int], sign: Sign = Sign.POSITIVE, base: Base = Base36
    ) -> None:
        self._rdigits = self._rstrip(reversed_digits)
        self._sign = sign
        self._base = base

    @staticmethod
    def parse(value: str, base: Base = Base36) -> "Integer":
        sign = Sign.POSITIVE if value[0] != "-" else Sign.NEGATIVE
        if value[0] in ("+", "-"):
            value = value[1:]

        digits = [base.to_base10(digit) for digit in reversed(value)]
        return Integer(digits, sign, base)

    @property
    def digits(self) -> list[int]:
        return list(reversed(self._rdigits))

    @property
    def sign(self) -> Sign:
        return self._sign

    @property
    def base(self) -> Base:
        return self._base

    @staticmethod
    def from_base10(value: int, base: Base = Base36) -> "Integer":
        sign = Sign.POSITIVE if value >= 0 else Sign.NEGATIVE
        value = abs(value)

        digits = []
        while value > 0:
            digits.append(value % base.base())
            value //= base.base()

        return Integer(digits, sign, base)

    def __neg__(self) -> Self:
        return self.__class__(self._rdigits.copy(), -self._sign, self._base)

    def __abs__(self) -> Self:
        return self.__class__(self._rdigits.copy(), Sign.POSITIVE, self._base)

    def __add__(self, other: Self) -> Self:
        if self._sign != other._sign:
            return self - (-other)

        rdigits = []
        carry = 0

        for i in range(max(len(self), len(other))):
            a = self._rdigits[i] if i < len(self) else 0
            b = other._rdigits[i] if i < len(other) else 0

            result = a + b + carry
            carry = result // self._base.base()
            rdigits.append(result % self._base.base())

        if carry:
            rdigits.append(carry)

        return self.__class__(rdigits, self._sign, self._base)

    def __sub__(self, other: Self) -> Self:
        raise NotImplementedError

    def __mul__(self, other: Self) -> Self:
        rdigits = [0] * (len(self) + len(other))

        for i in range(len(self)):
            for j in range(len(other)):
                index = i + j
                ret = rdigits[index] + self._rdigits[i] * other._rdigits[j]
                rdigits[index] = ret % self._base.base()
                rdigits[index + 1] += ret // self._base.base()

        return self.__class__(rdigits, self._sign * other._sign, self._base)

    def __lshift__(self, other: int) -> Self:
        if other < 0:
            raise ValueError("shift count must be non-negative")
        rdigits = [0] * other + self._rdigits
        return self.__class__(rdigits, self._sign, self._base)

    def __rshift__(self, other: int) -> Self:
        if other < 0:
            raise ValueError("shift count must be non-negative")
        return self.__class__(self._rdigits[other:], self._sign, self._base)

    def to_base10(self) -> int:
        value = 0
        for i, digit in enumerate(self._rdigits):
            value += digit * self._base.base() ** i
        return self._sign.value * value

    def __str__(self) -> str:
        if len(self) == 0:
            return "0"

        num = "".join([self._base.from_base10(digit) for digit in reversed(self._rdigits)])
        return f"{'-' if self._sign == Sign.NEGATIVE else ''}{num}"

    def __len__(self) -> int:
        return len(self._rdigits)

    @staticmethod
    def _rstrip(reversed_digits: list[int]) -> list[int]:
        index = len(reversed_digits)
        for i in reversed(range(index)):
            if reversed_digits[i] != 0:
                index = i + 1
                break
        return reversed_digits[:index]
