# Data Envelopment Analysis ([DEA](DEA.pdf)) Computational Library 

This repository provides a Python library for applying Data Envelopment Analysis (DEA) to real-world data. It includes several classes to compute various tasks related to DEA:

1. **`Dea()`**  
   _File:_ `libDEA/dea_instance.py`  
   Solves a standard single DEA instance.

2. **`DeaMultiprocessing()`**  
   _File:_ `libDEA/dea_multiprocessing.py`  
   Solves multiple DEA instances in parallel using multiprocessing.

3. **`DeaLargeScale()`**  
   _File:_ `libDEA/dea_largescale.py`  
   Optimizes performance for large-scale cases.

4. **`DeaProfile()`**  
   _File:_ `libDEA/dea_profile.py`  
   Visualizes the efficiency surface.

The package uses the linear solver from the [`ortools`](https://developers.google.com/optimization) library. It is free to use, provided you comply with the terms and conditions of `ortools`.

For more details, see my PhD-related paper: [DEA.pdf](DEA.pdf)


**Installation**
```
git clone --branch  main https://github.com/aav-antonov/DEA.git
cd DEA
pip install . e
```


**Test**

In the `DEA` folder, you can benchmark and test the performance and correctness of the two DEA implementations by running:

python test_benchmark.py

This script benchmarks and tests both accuracy and computational efficiency for:

- **DeaMultiprocessing:** Base method that computes efficiency for each unit directly using multiprocessing.
- **DeaLargeScale:** Optimized version designed for large-scale data and improved performance.

Random datasets of varying sizes are generated. Both methods are executed, results are compared for accuracy, and computation time is measured.

**All tests were run on a machine with 4 CPU cores.**

### Execution Time Summary

| m    | fX_k | fY_k | DeaMultiprocessing (s) | DeaLargeScale (s) |
|------|------|------|------------------------|-------------------|
| 250  | 5    | 3    | 5.6306                 | 5.8992            |
| 500  | 5    | 3    | 21.8980                | 14.5271           |
| 1000 | 5    | 3    | 86.2211                | 37.7303           |
| 2000 | 5    | 3    | 351.1777                 | 105.9509          |
| 4000 | 5    | 3    | 1500.0*                | 240.7928          |
| 8000 | 5    | 3    | 6200.0*                | 607.6985          |

- \* Extrapolated values for DeaMultiprocessing (based on observed scaling from smaller dataset runs).
  


**Data Envelopment Analysis (DEA)**

DEA evaluates the relative efficiency of a set of decision-making units (DMUs) by analyzing their input/output combinations. Each DMU is represented by a vector of inputs $x$ and outputs $y$. For multiple DMUs, inputs and outputs are organized into matrices $X$ and $Y$. 

The classical input-oriented DEA efficiency score for a DMU $o$ (where $o = 1, \ldots, n$) is computed by solving the following linear program:

$$
\begin{align*}
\text{Minimize}\quad & \theta_o \\\\
\text{Subject to}\quad
    & \sum_{j=1}^n \lambda_j x_{ij} \leq \theta x_{io},\quad \forall i = 1, \ldots, m \\\\
    & \sum_{j=1}^n \lambda_j y_{rj} \geq y_{ro},\quad \forall r = 1, \ldots, s \\\\
    & \lambda_j \geq 0, \quad \forall j = 1, \ldots, n
\end{align*}
$$

where:

- $x_{ij}$: the $i$-th input for DMU $j$,
- $y_{rj}$: the $r$-th output for DMU $j$,
- $m$: number of input variables,
- $s$: number of output variables,
- $n$: number of DMUs,
- $\lambda_j$: weights for constructing a reference DMU,
- $\theta_o$: efficiency score for DMU $o$ ($\theta \leq 1$; $\theta = 1$ means efficient).

The solution $\theta_o$ is the efficiency of DMU $o$. A DMU is considered efficient if $\theta_o = 1$, and inefficient if $\theta_o < 1$ compared to the rest of the dataset.



**Complexity of the Problem**

Given input and output matrices $X$ and $Y$, the above linear program must be solved separately for each DMU. The computational time required to solve these problems commonly grows super-quadratically with the number of DMUs ($n$), because both the number of linear programs and the size of each program (determined by the number of DMUs and variables) increase as $n$ increases. Specifically, the size of each individual linear program grows with $n$ (the number of DMUs appears in both constraints and variables), so the total computational time in average case increases faster than $O(n^2)$—often approaching cubic growth for large datasets.

As a result, evaluating DEA efficiency for datasets with more than 1,000 DMUs, even with a moderate number of inputs (e.g., $m = 5$) and outputs (e.g., $s = 3$), can require hours of computation—even when using parallel processing on multiple CPU cores.

**Improving Computational Performance**

A standard way to reduce computational time in DEA is to exploit the fact that the efficiency of each DMU can be determined using only the set of efficient DMUs, rather than the full matrices $X$ and $Y$. In practice, for fixed input and output dimensions, the number of efficient DMUs tends to saturate as the dataset grows—adding more DMUs usually results in only a few additional efficient units. Therefore, a common strategy is to first identify the efficient set (referred to as the `full_base`), which is typically much smaller than the total number of DMUs, and then compute the efficiency of all other DMUs using only this set. The `DeaLargeScale` class implements this strategy to achieve significant computational improvements.      

**Steps in DeaLargeScale**

***Base Candidate Selection via Ratios***  
Calculate efficiency-related ratios for each column (DMU) and select preliminary candidates.  
Let the candidate set be denoted as $B_0$.

***Base Extension (Addbase)***  
For each DMU in $B_0$, solve the DEA model (e.g., linear programming) using the reference sets $X[B_0]$ and $Y[B_0]$. Retain those DMUs whose computed efficiency scores are greater than or equal to $1$.  
Let this refined set be denoted as $B_1$.

***Base Refinement (Rebase)***  
For each DMU in $B_1$, solve DEA using $X[B_1]$ and $Y[B_1]$ as reference sets, and retain only the efficient DMUs, yielding set $B_2$. At this stage, $B_2$ should contain the complete subset of efficient DMUs from the original $X$ and $Y$. This step ensures removal of any inefficient DMUs from $B_1$.

***Final Compute***  
For each DMU in the original matrices $X$ and $Y$, solve DEA using the reference sets $X[B_2]$ and $Y[B_2]$. Thus, we still solve $n$ linear programs (one per DMU), but the size of each problem is significantly reduced compared to using the full set.





