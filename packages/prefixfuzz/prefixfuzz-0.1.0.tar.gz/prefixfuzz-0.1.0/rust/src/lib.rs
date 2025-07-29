use pyo3::prelude::*;

pub mod prefix;

use crate::prefix::matcher::Matcher;
use crate::prefix::trie::Trie;

#[pyclass]
pub struct PrefixSearch {
    trie: Trie,
}

#[pymethods]
impl PrefixSearch {
    pub fn fuzzy_search(
        &self,
        prefix: String,
        max_dist: usize,
        limit: Option<usize>,
    ) -> Vec<(String, Option<u32>, usize)> {
        let mut matcher = Matcher::new(prefix, max_dist, limit);
        self.trie.dfs(&mut matcher);

        matcher
            .get_results()
            .iter()
            .map(|(prefix, node_id, dist)| {
                (prefix.clone(), self.get_payload(*node_id), *dist)
            })
            .collect()
    }

    pub fn get_children(&self, node_id: u32) -> Vec<(char, u32)> {
        self.trie.get_children(node_id)
    }

    pub fn get_payload(&self, node_id: u32) -> Option<u32> {
        self.trie.get_payload(node_id)
    }
}

#[pyfunction]
fn from_internal_data(
    node_shifts: Vec<u32>,
    node_strings: Vec<String>,
    node_payloads: Vec<Option<u32>>,
    child_indices: Vec<u32>,
) -> PyResult<PrefixSearch> {
    let node_chars: Vec<Option<char>> =
        node_strings.into_iter().map(|s| s.chars().next()).collect();

    Ok(PrefixSearch {
        trie: Trie::from_internal_data(node_shifts, node_chars, node_payloads, child_indices),
    })
}

#[pymodule]
fn _prefixfuzz(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(from_internal_data, m)?)?;
    m.add_class::<PrefixSearch>()?;
    Ok(())
}
