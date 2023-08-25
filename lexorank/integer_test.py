from lexorank.base import Base10, Base36, Base64
from lexorank.integer import parse


def test_parse():
    cases = [
        {"in": ("123", Base10), "want": [1, 2, 3]},
        {"in": ("ri", Base36), "want": [27, 18]},
        {"in": ("r^i", Base64), "want": [55, 36, 46]},
        {"in": (123, Base10), "want": [1, 2, 3]},
        {"in": (3 * 36 + 4, Base36), "want": [3, 4]},
        {"in": (20 * 64**2 + 1, Base64), "want": [20, 0, 1]},
    ]

    for c in cases:
        got = parse(*c["in"]).digits
        assert got == c["want"]


def test_add():
    cases = [
        {"in": (123, 356), "want": 479},
        {
            "in": (-11230124540123123124, -12315810924310958102938109238190284),
            "want": -12315810924310969333062649361313408,
        },
    ]

    for c in cases:
        a = parse(c["in"][0])
        b = parse(c["in"][1])
        got = (a + b).to_base10()
        assert got == c["want"]


def test_mul():
    cases = [
        {"in": (123, 356), "want": 43788},
        {"in": (-157564, 123), "want": -19380372},
        {
            "in": (-11230124540123123124, -12315810924310958102938109238190284),
            "want": 138308090492620934298311599366068267126028607872527216,
        },
        {"in": (0, -123), "want": 0},
    ]

    for c in cases:
        a = parse(c["in"][0])
        b = parse(c["in"][1])
        got = (a * b).to_base10()
        assert got == c["want"]


def test_lshift():
    cases = [
        {"in": (123, 1), "want": 123 * 36},
        {"in": (123, 123), "want": 123 * 36**123},
    ]

    for c in cases:
        a = parse(c["in"][0])
        got = (a << c["in"][1]).to_base10()
        assert got == c["want"]


def test_rshift():
    cases = [
        {"in": (123, 1), "want": 123 // 36},
        {"in": (123, 11), "want": 0},
    ]

    for c in cases:
        a = parse(c["in"][0])
        got = (a >> c["in"][1]).to_base10()
        assert got == c["want"]


def test_str():
    cases = [
        {"in": (123, Base10), "want": "123"},
        {"in": (123123541345346245634523463456456, Base36), "want": "97l0vq9nx1bzufjaqp4ug"},
        {"in": (123, Base64), "want": "1v"},
        {"in": (-123, Base64), "want": "-1v"},
    ]

    for c in cases:
        got = str(parse(*c["in"]))
        assert got == c["want"]
