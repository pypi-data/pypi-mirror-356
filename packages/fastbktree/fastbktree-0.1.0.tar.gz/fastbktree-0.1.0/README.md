# fastbktree :deciduous_tree:

A Rust implementation of [BK-trees](https://en.wikipedia.org/wiki/BK-tree) for fast fuzzy string matching in Python.


## Installation

```bash
uv add fastbktree
# pip install fastbktree
```

## Quickstart
```python
from fastbktree import BKTree

# Create a BK-tree from a list of strings
tree = BKTree(["hello", "help", "hell", "shell", "helper"])

# Search for similar strings within a maximum distance
results = tree.search("helo", max_distance=2)
# Returns: [("hello", 1), ("hell", 1), ("help", 1)]

# Get the size of the corpus
print(len(tree))  # 5
```

## Reference

### `BKTree(iterable)`
Creates a new BK-tree from an iterable of strings.

```python
tree = BKTree(["word1", "word2", "word3"])
```

### `tree.search(query: str, max_distance: int) -> List[Tuple[str, int]]`
Searches for strings similar to `query` within `max_distance` Levenshtein distance.
Returns a list of `(string, distance)` tuples.

```python
results = tree.search("query", max_distance=2)
```

### `len(tree) -> int`
Returns the number of strings in the tree.

```python
size = len(tree)
```

### `levenshtein_distance(a: str, b: str) -> int`
Pure Rust implementation of Levenshtein distance between two strings.

```python
from fastbktree import levenshtein_distance

distance = levenshtein_distance("kitten", "sitting")  # 3
```


## License
MIT
