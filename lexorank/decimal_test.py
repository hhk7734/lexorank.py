from lexorank import decimal, integer
from lexorank.base import Base10, Base36, Base64
from lexorank.decimal import Decimal


def test_parse():
    cases = [
        {"in": ("12:3", Base10), "want": "12:3"},
        {"in": (0.5, Base36), "want": "0:i"},
        {"in": (-0.5, Base36), "want": "-0:i"},
        {"in": (10, Base36), "want": "a:"},
        {"in": ("0000:00ri", Base36), "want": "0:00ri"},
        {"in": ("-0000:00ri", Base36), "want": "-0:00ri"},
        {"in": ("r^i", Base64), "want": "r^i:"},
    ]

    for c in cases:
        got = str(decimal.parse(*c["in"]))
        assert got == c["want"]


def test_add():
    cases = [
        {"in": (("12345", Base10, -3), ("55", Base10, -1)), "want": 17.845},
        {"in": (("12345", Base10, 1), ("55", Base10, -1)), "want": 123455.5},
        {"in": (("12345", Base10, 1), ("55", Base10, 1)), "want": 124000},
    ]

    for c in cases:
        a = Decimal(integer.parse(c["in"][0][0], c["in"][0][1]), c["in"][0][2])
        b = Decimal(integer.parse(c["in"][1][0], c["in"][1][1]), c["in"][1][2])
        assert float(a + b) == c["want"]


def test_mul():
    cases = [
        {"in": (("12345", Base10, -3), ("55", Base10, -1)), "want": "67:8975"},
        {"in": (("12345", Base10, 1), ("5", Base10, -1)), "want": "61725:"},
        {"in": (("12as5", Base36, 0), ("i", Base36, -1)), "want": "j5e2:i"},
    ]

    for c in cases:
        a = Decimal(integer.parse(c["in"][0][0], c["in"][0][1]), c["in"][0][2])
        b = Decimal(integer.parse(c["in"][1][0], c["in"][1][1]), c["in"][1][2])
        got = str(a * b)
        assert got == c["want"]


def test_whole():
    cases = [
        {"in": ("12345", Base10, -3), "want": "12"},
        {"in": ("21i3v9", Base36, -4), "want": "21"},
    ]

    for c in cases:
        got = str(Decimal(integer.parse(c["in"][0], c["in"][1]), c["in"][2]).whole())
        assert got == c["want"]


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
