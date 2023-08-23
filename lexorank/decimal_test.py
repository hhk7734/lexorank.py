from lexorank.base import Base10, Base36, Base64
from lexorank.decimal import Decimal
from lexorank.integer import Integer


def test_add():
    cases = [
        {"in": (("12345", Base10, -3), ("55", Base10, -1)), "want": 17.845},
        {"in": (("12345", Base10, 1), ("55", Base10, -1)), "want": 123455.5},
        {"in": (("12345", Base10, 1), ("55", Base10, 1)), "want": 124000},
    ]

    for c in cases:
        a = Decimal(Integer.from_base(c["in"][0][0], c["in"][0][1]), c["in"][0][2])
        b = Decimal(Integer.from_base(c["in"][1][0], c["in"][1][1]), c["in"][1][2])
        got = (a + b).to_base10()
        assert got == c["want"]


def test_mul():
    cases = [
        {"in": (("12345", Base10, -3), ("55", Base10, -1)), "want": "67:8975"},
        {"in": (("12345", Base10, 1), ("5", Base10, -1)), "want": "61725"},
        {"in": (("12as5", Base36, 0), ("i", Base36, -1)), "want": "j5e2:i"},
    ]

    for c in cases:
        a = Decimal(Integer.from_base(c["in"][0][0], c["in"][0][1]), c["in"][0][2])
        b = Decimal(Integer.from_base(c["in"][1][0], c["in"][1][1]), c["in"][1][2])
        got = str(a * b)
        assert got == c["want"]


def test_whole():
    cases = [
        {"in": ("12345", Base10, -3), "want": "12"},
        {"in": ("21i3v9", Base36, -4), "want": "21"},
    ]

    for c in cases:
        got = str(Decimal(Integer.from_base(c["in"][0], c["in"][1]), c["in"][2]).whole())
        assert got == c["want"]


def test_str():
    cases = [
        {"in": ("12345", Base10, -3), "want": "12:345"},
        {"in": ("21i3v9", Base36, -4), "want": "21:i3v9"},
        {"in": ("21i3v9", Base36, -10), "want": "0:000021i3v9"},
        {"in": ("21i3v9^", Base64, 2), "want": "21i3v9^00"},
    ]

    for c in cases:
        got = str(Decimal(Integer.from_base(c["in"][0], c["in"][1]), c["in"][2]))
        assert got == c["want"]