from lexorank import lexorank
from lexorank.base import Base10, Base36, Base64
from lexorank.lexorank import Bucket


def test_parse():
    cases = [
        {"in": ("0|000012:3", Base10), "want": (Bucket.BUCKET_0, "12:3", "0|000012:3")},
        {"in": ("0|00ri01:000000", Base36), "want": (Bucket.BUCKET_0, "ri01:", "0|00ri01:")},
        {"in": ("1|000r^i:1", Base64), "want": (Bucket.BUCKET_1, "r^i:1", "1|000r^i:1")},
    ]

    for c in cases:
        got = lexorank.parse(*c["in"])
        assert got.bucket == c["want"][0]
        assert str(got.rank) == c["want"][1]
        assert str(got) == c["want"][2]


def test_middle():
    cases = [
        {"in": (Bucket.BUCKET_0, Base10), "want": "0|500000:"},
        {"in": (Bucket.BUCKET_0, Base36), "want": "0|i00000:"},
        {"in": (Bucket.BUCKET_0, Base64), "want": "0|W00000:"},
    ]

    for c in cases:
        got = lexorank.middle(*c["in"])
        assert str(got) == c["want"]


def test_next():
    cases = [
        {"in": lexorank.middle(Bucket.BUCKET_0, Base10), "want": "0|500016:"},
        {"in": lexorank.middle(Bucket.BUCKET_0, Base36), "want": "0|i0000g:"},
        {"in": lexorank.middle(Bucket.BUCKET_0, Base64), "want": "0|W0000G:"},
    ]

    for c in cases:
        got = c["in"].next()
        assert str(got) == c["want"]


def test_add():
    cases = [
        {"in": ("0|000001:", "0|000002:", Base36), "want": "0|000003:"},
    ]

    for c in cases:
        got = lexorank.parse(c["in"][0], c["in"][2])
        other = lexorank.parse(c["in"][1], c["in"][2])
        assert (got + other) == c["want"]


def test_eq():
    cases = [
        {"in": ("0|000001:", "0|000002:", Base36), "want": False},
        {"in": ("0|000001:", "0|000001:", Base36), "want": True},
        {"in": ("0|000002:", "0|000001:", Base36), "want": False},
    ]

    for c in cases:
        got = lexorank.parse(c["in"][0], c["in"][2])
        other = lexorank.parse(c["in"][1], c["in"][2])
        assert (got == other) == c["want"]


def test_gt():
    cases = [
        {"in": ("0|000001:", "0|000002:", Base36), "want": False},
        {"in": ("0|000001:", "0|000001:", Base36), "want": False},
        {"in": ("0|000002:", "0|000001:", Base36), "want": True},
        {"in": ("1|000001:", "0|000001:", Base36), "want": True},
    ]

    for c in cases:
        got = lexorank.parse(c["in"][0], c["in"][2])
        other = lexorank.parse(c["in"][1], c["in"][2])
        assert (got > other) == c["want"]
