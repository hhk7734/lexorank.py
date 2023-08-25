from lexorank.base import Base10, Base36, Base64
from lexorank.lexorank import Bucket, LexoRank


def test_parse():
    cases = [
        {"in": ("0|000012:3", Base10), "want": (Bucket.BUCEKT_0, "12:3", "0|000012:3")},
        {"in": ("0|00ri01:000000", Base36), "want": (Bucket.BUCEKT_0, "ri01:", "0|00ri01:")},
        {"in": ("1|000r^i:1", Base64), "want": (Bucket.BUCKET_1, "r^i:1", "1|000r^i:1")},
    ]

    for c in cases:
        got = LexoRank.parse(*c["in"])
        assert got.bucket == c["want"][0]
        assert str(got.rank) == c["want"][1]
        assert str(got) == c["want"][2]


def test_middle():
    cases = [
        {"in": (Bucket.BUCEKT_0, Base10), "want": "0|500000:"},
        {"in": (Bucket.BUCEKT_0, Base36), "want": "0|i00000:"},
        {"in": (Bucket.BUCEKT_0, Base64), "want": "0|W00000:"},
    ]

    for c in cases:
        got = LexoRank.middle(*c["in"])
        assert str(got) == c["want"]


def test_next():
    cases = [
        {"in": LexoRank.middle(Bucket.BUCEKT_0, Base10), "want": "0|500016:"},
        {"in": LexoRank.middle(Bucket.BUCEKT_0, Base36), "want": "0|i0000g:"},
        {"in": LexoRank.middle(Bucket.BUCEKT_0, Base64), "want": "0|W0000G:"},
    ]

    for c in cases:
        got = c["in"].next()
        assert str(got) == c["want"]
