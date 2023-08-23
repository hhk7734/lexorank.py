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
        assert str(got.decimal) == c["want"][1]
        assert str(got) == c["want"][2]
