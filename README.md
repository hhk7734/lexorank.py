## lexorank.py

```shell
python3 -m pip install lexorank-py
```

### New Rank

```python
from pprint import pprint

from lexorank import Bucket, middle

prev = middle(Bucket.BUCEKT_0)
ranks = [prev]
for _ in range(9):
    ranks.append(prev.next())
    prev = ranks[-1]

pprint(ranks)
```

```shell
[<LexoRank value=0|i00000: base=36>,
 <LexoRank value=0|i0000g: base=36>,
 <LexoRank value=0|i0000w: base=36>,
 <LexoRank value=0|i0001c: base=36>,
 <LexoRank value=0|i0001s: base=36>,
 <LexoRank value=0|i00028: base=36>,
 <LexoRank value=0|i0002o: base=36>,
 <LexoRank value=0|i00034: base=36>,
 <LexoRank value=0|i0003k: base=36>,
 <LexoRank value=0|i00040: base=36>]
```

### Between

```python
from lexorank import between, parse

a = parse("0|i00000:")
b = parse("0|i00001:")

mid = between(a, b)
# <LexoRank value=0|i00000:i base=36>

a = parse("0|i00000:")
b = None

mid = between(a, b)  # = a.next()
# <LexoRank value=0|i0000g: base=36>

a = None
b = parse("0|i00000:")

mid = between(a, b)  # = b.prev()
# <LexoRank value=0|hzzzzk: base=36>
```