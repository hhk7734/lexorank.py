from typing import Protocol


class Base(Protocol):
    @staticmethod
    def to_base10(digit: str) -> int:
        ...

    @staticmethod
    def from_base10(digit: int) -> str:
        ...

    @staticmethod
    def base() -> int:
        ...


class Base10:
    @staticmethod
    def to_base10(digit: str) -> int:
        return int(digit)

    @staticmethod
    def from_base10(digit: int) -> str:
        return str(digit)

    @staticmethod
    def base() -> int:
        return 10


class Base36:
    @staticmethod
    def to_base10(digit: str) -> int:
        return base36ToBase10[digit]

    @staticmethod
    def from_base10(digit: int) -> str:
        return base10ToBase36[digit]

    @staticmethod
    def base() -> int:
        return 36


class Base64:
    @staticmethod
    def to_base10(digit: str) -> int:
        return base64ToBase10[digit]

    @staticmethod
    def from_base10(digit: int) -> str:
        return base10ToBase64[digit]

    @staticmethod
    def base() -> int:
        return 64


base36ToBase10 = {
    "0": 0,
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "a": 10,
    "b": 11,
    "c": 12,
    "d": 13,
    "e": 14,
    "f": 15,
    "g": 16,
    "h": 17,
    "i": 18,
    "j": 19,
    "k": 20,
    "l": 21,
    "m": 22,
    "n": 23,
    "o": 24,
    "p": 25,
    "q": 26,
    "r": 27,
    "s": 28,
    "t": 29,
    "u": 30,
    "v": 31,
    "w": 32,
    "x": 33,
    "y": 34,
    "z": 35,
}

base10ToBase36 = {v: k for k, v in base36ToBase10.items()}

base64ToBase10 = {
    "0": 0,
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "A": 10,
    "B": 11,
    "C": 12,
    "D": 13,
    "E": 14,
    "F": 15,
    "G": 16,
    "H": 17,
    "I": 18,
    "J": 19,
    "K": 20,
    "L": 21,
    "M": 22,
    "N": 23,
    "O": 24,
    "P": 25,
    "Q": 26,
    "R": 27,
    "S": 28,
    "T": 29,
    "U": 30,
    "V": 31,
    "W": 32,
    "X": 33,
    "Y": 34,
    "Z": 35,
    "^": 36,
    "_": 37,
    "a": 38,
    "b": 39,
    "c": 40,
    "d": 41,
    "e": 42,
    "f": 43,
    "g": 44,
    "h": 45,
    "i": 46,
    "j": 47,
    "k": 48,
    "l": 49,
    "m": 50,
    "n": 51,
    "o": 52,
    "p": 53,
    "q": 54,
    "r": 55,
    "s": 56,
    "t": 57,
    "u": 58,
    "v": 59,
    "w": 60,
    "x": 61,
    "y": 62,
    "z": 63,
}

base10ToBase64 = {v: k for k, v in base64ToBase10.items()}
