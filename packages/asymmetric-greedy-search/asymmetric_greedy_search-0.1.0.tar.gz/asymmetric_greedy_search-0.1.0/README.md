# Asymmetric Greedy Search

A Python implementation of the **Asymmetric Greedy Search (AGS)** algorithm, a fast heuristic for solving the **Linear Sum Assignment Problem**, based on the work of Brown et al. (2017).

## Features
This package provides an efficient alternative to exact methods like the [Hungarian algorithm](https://en.wikipedia.org/wiki/Hungarian_algorithm), particularly for large, rectangular (asymmetric) matrices where exact solutions may be computationally expensive. It includes both **NumPy** and **Numba** backends and extends the original algorithm with features such as: 
* Optional **randomized greedy initialization**
* Support for both **cost minimization** and **benefit maximization**
* Optional **batched row updates** between global swap benefit recalculations

## Installation

```bash
pip install git+https://github.com/kaboroevich/asymmetric-greedy-search.git
```
## Usage Example

```python
from asymmetric_greedy_search import AsymmetricGreedySearch
import numpy as np

# Create a random benefit matrix (maximize benefit)
np.random.seed(57)
benefit = np.random.rand(100, 120)

ags = AsymmetricGreedySearch(backend='numba')
row_ind, assignment = ags.optimize(benefit)
score = benefit[row_ind, assignment].sum()

print(f"Total benefit: {score}")
```

## Parameters

### `AsymmetricGreedySearch(backend = "numpy")`

* **backend** (`str`, optional): Specifies the computational backend to use for the algorithm.  
  Options are:
  * `"numpy"` (default): Uses a NumPy-based implementation, suitable for general use.
  * `"numba"`: Uses a Numba-accelerated implementation for improved performance on large problems.

---

### `AsymmetricGreedySearch.optimize(benefit, minimize=False, shuffle=False, maximum_iterations=0, stagnation_limit=0, stagnation_tolerance=1e-3, row_batch_size=1)`

Runs the Asymmetric Greedy Search optimization on the provided benefit matrix.

* **benefit** (`numpy.ndarray`): A 2D array representing the benefit or cost matrix for row-column assignments.
* **minimize** (`bool`): If `True`, the algorithm minimizes the assignment costs instead of maximizing the benefit. Defaults to `False`.
* **shuffle** (`bool`): If `True`, rows are shuffled before the greedy initialization to potentially improve solution diversity. Defaults to `False`.
* **maximum_iterations** (`int`): The maximum number of optimization iterations to perform. If set to `0`, no limit is applied. Defaults to `0`.
* **stagnation_limit** (`int`): The number of consecutive iterations allowed where the maximum improvement remains below a specified tolerance before terminating early. A value of `0` disables stagnation detection. Defaults to `0`.
* **stagnation_tolerance** (`float`): The relative improvement threshold used to detect stagnation. Stagnation is triggered if the maximum benefit improvement stays below `initial_max_delta * stagnation_tolerance` for `stagnation_limit` consecutive iterations. Defaults to `1e-3`.
* **row_batch_size** (`int`): The number of rows to swap in each iteration, allowing batched updates to improve efficiency. Defaults to `1` (no batching).

**Returns:**  
A tuple containing two NumPy arrays:  
- The first array contains row indices.  
- The second array contains the assigned column indices corresponding to each row.

## Benchmarking
The [examples/lsa_benchmark.ipynb](examples/lsa_benchmark.ipynb) notebook benchmarks AGS against [SciPy's `linear_sum_assignment`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linear_sum_assignment.html), comparing runtime and assignment quality on synthetic distance matrices of increasing size.

AGS achieves solutions **within a few percent of optimal** (LSA) while offering orders-of-magnitude faster runtime on certain large matrices.

## References
Brown, Peter, Yuedong Yang, Yaoqi Zhou, and Wayne Pullan. "A heuristic for the time constrained asymmetric linear sum assignment problem." *Journal of Combinatorial Optimization* 33 (2017): 551-566.    
https://doi.org/10.1007/s10878-015-9979-2