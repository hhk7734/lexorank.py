from lexorank import decimal, integer
from lexorank.base import Base10, Base36, Base64
from lexorank.decimal import Decimal


def test_parse():
    cases = [
        {"in": ("12:3", Base10), "want": "12:3"},
        {"in": (0.5, Base36), "want": "0:i"},
        {"in": (-0.5, Base36), "want": "-0:i"},
        {"in": (10, Base36), "want": "a:"},
        {"in": (integer.parse(10), Base36), "want": "a:"},
        {"in": ("0000:00ri", Base36), "want": "0:00ri"},
        {"in": ("-0000:00ri", Base36), "want": "-0:00ri"},
        {"in": ("r^i", Base64), "want": "r^i:"},
    ]

    for c in cases:
        got = str(decimal.parse(*c["in"]))
        assert got == c["want"]


def test_add():
    cases = [
        {"in": (("12:345", Base10), ("5:5", Base10)), "want": ("17:845", Base10)},
        {"in": (("123450", Base10), ("5:5", Base10)), "want": ("123455:5", Base10)},
        {"in": (("123450", Base10), ("550", Base10)), "want": ("124000", Base10)},
        {"in": (("123450", Base10), ("-550", Base10)), "want": ("122900", Base10)},
        {"in": (("-123450", Base10), ("-550", Base10)), "want": ("-124000", Base10)},
        {"in": (("-123450", Base10), ("550", Base10)), "want": ("-122900", Base10)},
    ]

    for c in cases:
        a = decimal.parse(*c["in"][0])
        b = decimal.parse(*c["in"][1])
        assert a + b == decimal.parse(*c["want"])


def test_mul():
    cases = [
        {"in": (("12:345", Base10), ("55", Base10)), "want": ("678:975", Base10)},
        {"in": (("12:345", Base10), ("0:5", Base10)), "want": ("6:1725", Base10)},
        {"in": (("12as5", Base36), ("0:i", Base36)), "want": ("j5e2:i", Base36)},
        {"in": (("12as5", Base36), ("-0:i", Base36)), "want": ("-j5e2:i", Base36)},
        {"in": (("-12as5", Base36), ("0:i", Base36)), "want": ("-j5e2:i", Base36)},
        {"in": (("-12as5", Base36), ("-0:i", Base36)), "want": ("j5e2:i", Base36)},
    ]

    for c in cases:
        a = decimal.parse(*c["in"][0])
        b = decimal.parse(*c["in"][1])
        assert a * b == decimal.parse(*c["want"])


def test_eq():
    cases = [
        {"in": (0, 0)},
        {"in": (12.3, 12.3)},
        {"in": (-12.3, 12.3)},
        {"in": (12.3, -12.3)},
        {"in": (-12.3, -12.3)},
        {"in": (12.3, 123.4)},
        {"in": (12.3, -123.4)},
        {"in": (-12.3, 123.4)},
        {"in": (-12.3, -123.4)},
        {"in": (123.4, 12.3)},
        {"in": (123.4, -12.3)},
        {"in": (-123.4, 12.3)},
        {"in": (-123.4, -12.3)},
    ]

    for c in cases:
        a = decimal.parse(c["in"][0])
        b = decimal.parse(c["in"][1])
        assert (a == b) == (c["in"][0] == c["in"][1])


def test_gt():
    cases = [
        {"in": (0, 0)},
        {"in": (12.3, 12.3)},
        {"in": (-12.3, 12.3)},
        {"in": (12.3, -12.3)},
        {"in": (-12.3, -12.3)},
        {"in": (12.3, 123.4)},
        {"in": (12.3, -123.4)},
        {"in": (-12.3, 123.4)},
        {"in": (-12.3, -123.4)},
        {"in": (123.4, 12.3)},
        {"in": (123.4, -12.3)},
        {"in": (-123.4, 12.3)},
        {"in": (-123.4, -12.3)},
    ]

    for c in cases:
        a = decimal.parse(c["in"][0])
        b = decimal.parse(c["in"][1])
        assert (a > b) == (c["in"][0] > c["in"][1])


def test_whole_number():
    cases = [
        {"in": ("12345", Base10, -3), "want": "12"},
        {"in": ("21i3v9", Base36, -4), "want": "21"},
    ]

    for c in cases:
        got = str(Decimal(integer.parse(c["in"][0], c["in"][1]), c["in"][2]).whole_number())
        assert got == c["want"]


def test_decimal():
    cases = [
        {"in": ("12:345", Base10), "want": ("0:345", Base10)},
        {"in": ("21:i3v9", Base36), "want": ("0:i3v9", Base36)},
    ]

    for c in cases:
        got = decimal.parse(*c["in"]).decimal()
        assert got == decimal.parse(*c["want"])


def test_str():
    cases = [
        {"in": ("12345", Base10, -3), "want": "12:345"},
        {"in": ("21i3v9", Base36, 1), "want": "21i3v90:"},
        {"in": ("21i3v9", Base36, -6), "want": "0:21i3v9"},
        {"in": ("21i3v9", Base36, -10), "want": "0:000021i3v9"},
        {"in": ("21i3v9^", Base64, 2), "want": "21i3v9^00:"},
    ]

    for c in cases:
        got = str(Decimal(integer.parse(c["in"][0], c["in"][1]), c["in"][2]))
        assert got == c["want"]
