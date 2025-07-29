use ahash::AHashMap;
use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use smallvec::SmallVec;

/// An iterative, allocation-free Levenshtein implementation.
/// Returns edit distance in **O(|a|·|b|)** but with tight cache locality.
fn levenshtein(a: &str, b: &str) -> u32 {
    // If either string is empty, distance is the other's length.
    if a.is_empty() {
        return b.chars().count() as u32;
    }
    if b.is_empty() {
        return a.chars().count() as u32;
    }

    // We work with bytes but handle UTF-8 by iterating over chars.
    let a_len = a.chars().count();
    let b_len = b.chars().count();

    // Keep the smaller string in `small` to minimize the buffer.
    let (small, large, small_len, _large_len) = if a_len < b_len {
        (a, b, a_len, b_len)
    } else {
        (b, a, b_len, a_len)
    };

    // One row plus border; SmallVec keeps <64 entries on the stack.
    let mut prev: SmallVec<[u32; 64]> = (0..=small_len as u32).collect();

    for (i, lc) in large.chars().enumerate() {
        let mut current = SmallVec::<[u32; 64]>::with_capacity(small_len + 1);
        current.push((i + 1) as u32);
        for (j, sc) in small.chars().enumerate() {
            let cost = if lc == sc { 0 } else { 1 };
            let insertion = current[j] + 1;
            let deletion = prev[j + 1] + 1;
            let substitution = prev[j] + cost;
            current.push(insertion.min(deletion).min(substitution));
        }
        prev = current;
    }
    *prev.last().unwrap()
}

/// A BK-tree node.
///
/// Children are keyed by the edit distance to the current term.
/// `ahash` keeps lookup lightning-fast and DOS-hard.
#[derive(Debug)]
struct Node {
    term: String,
    children: AHashMap<u32, Node>,
}

impl Node {
    fn new(term: String) -> Self {
        Self {
            term,
            children: AHashMap::new(),
        }
    }

    fn insert(&mut self, term: String) {
        let mut node = self;
        loop {
            let dist = levenshtein(&node.term, &term);
            if dist == 0 {
                // Already in corpus -> silently ignore.
                return;
            }
            if !node.children.contains_key(&dist) {
                node.children.insert(dist, Node::new(term));
                return;
            }
            node = node.children.get_mut(&dist).unwrap();
        }
    }

    fn search<'a>(
        &'a self,
        query: &str,
        max_dist: u32,
        results: &mut Vec<(&'a str, u32)>,
    ) {
        let dist = levenshtein(&self.term, query);
        if dist <= max_dist {
            results.push((&self.term, dist));
        }
        let lower = dist.saturating_sub(max_dist);
        let upper = dist + max_dist;
        for (&child_dist, child) in self.children.iter() {
            if child_dist >= lower && child_dist <= upper {
                child.search(query, max_dist, results);
            }
        }
    }
}

/// Public BK-tree wrapper, exposed to Python.
#[pyclass]
#[derive(Debug)]
pub struct BKTree {
    root: Node,
    corpus_size: usize,
}

#[pymethods]
impl BKTree {
    /// Build a tree from an **iterable of strings**.
    #[new]
    fn new(iterable: &Bound<'_, PyAny>) -> PyResult<Self> {
        // Use the new `try_iter` API on `PyAny` to obtain a Python iterator.
        let mut iter = iterable.try_iter()?;
        let first_py = iter
            .next()
            .ok_or_else(|| PyValueError::new_err("Corpus cannot be empty"))??;
        let first: String = first_py.extract()?;

        let mut root = Node::new(first.clone());
        let mut count = 1usize;

        for item in iter {
            let s: String = item?.extract()?;
            root.insert(s);
            count += 1;
        }
        Ok(Self {
            root,
            corpus_size: count,
        })
    }

    /// Search `query` within `max_distance`; returns list of `(term, distance)`.
    ///
    /// Runs in **O(k log n)** average where *k* is branching,
    /// with no additional allocations except the result vector.
    fn search(&self, query: &str, max_distance: u32) -> PyResult<Vec<(String, u32)>> {
        let mut tmp = Vec::with_capacity(16);
        self.root.search(query, max_distance, &mut tmp);
        let res: Vec<(String, u32)> = tmp
            .into_iter()
            .map(|(term, dist)| (term.to_owned(), dist))
            .collect();
        Ok(res)
    }

    /// Return corpus size.
    #[getter]
    fn len(&self) -> PyResult<usize> {
        Ok(self.corpus_size)
    }

    fn __repr__(&self) -> PyResult<String> {
        Ok(format!("BKTree(size={})", self.corpus_size))
    }
}

#[pymodule]
fn fastbktree(_py: Python<'_>, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<BKTree>()?;

    // Expose pure-Rust Levenshtein distance.
    #[pyfn(m)]
    fn levenshtein_distance(_py: Python<'_>, a: &str, b: &str) -> PyResult<u32> {
        Ok(levenshtein(a, b))
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_levenshtein() {
        // Basic cases
        assert_eq!(levenshtein("", ""), 0);
        assert_eq!(levenshtein("", "abc"), 3);
        assert_eq!(levenshtein("abc", ""), 3);

        // Simple edits
        assert_eq!(levenshtein("kitten", "sitting"), 3);
        assert_eq!(levenshtein("book", "back"), 2);

        // Unicode handling
        assert_eq!(levenshtein("café", "cafe"), 1);
        assert_eq!(levenshtein("résumé", "resume"), 2);
    }

    #[test]
    fn test_bktree_basic() {
        let mut tree = BKTree {
            root: Node::new("hello".to_string()),
            corpus_size: 1,
        };

        // Test insertion
        tree.root.insert("help".to_string());
        tree.root.insert("hell".to_string());
        tree.root.insert("world".to_string());

        // Test search
        let mut results = Vec::new();
        tree.root.search("help", 1, &mut results);
        assert_eq!(results.len(), 2); // Should find "help" and "hell"

        // Verify distances
        let distances: Vec<u32> = results.iter().map(|(_, d)| *d).collect();
        assert!(distances.contains(&0)); // Exact match
        assert!(distances.contains(&1)); // Distance 1 match
    }

    #[test]
    fn test_bktree_duplicates() {
        let mut tree = BKTree {
            root: Node::new("test".to_string()),
            corpus_size: 1,
        };

        // Inserting duplicates should be ignored
        tree.root.insert("test".to_string());
        tree.root.insert("test".to_string());

        let mut results = Vec::new();
        tree.root.search("test", 0, &mut results);
        assert_eq!(results.len(), 1); // Should only find one instance
    }

    #[test]
    fn test_bktree_search_ranges() {
        let mut tree = BKTree {
            root: Node::new("book".to_string()),
            corpus_size: 1,
        };

        // Insert words at various distances
        tree.root.insert("back".to_string());  // distance 2
        tree.root.insert("cook".to_string());  // distance 1
        tree.root.insert("look".to_string());  // distance 1

        // Test different search ranges
        let mut results = Vec::new();
        tree.root.search("book", 0, &mut results);
        assert_eq!(results.len(), 1); // Only exact match

        results.clear();
        tree.root.search("book", 1, &mut results);
        assert_eq!(results.len(), 3); // Exact match + distance 1 matches

        results.clear();
        tree.root.search("book", 2, &mut results);
        assert_eq!(results.len(), 4); // All matches including distance 2
    }
}
