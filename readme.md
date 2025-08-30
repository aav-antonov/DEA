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

Complexety of the problem
Given matrices $X$ and $Y$ the above formulated linear problem must be solved for each DMU, and the time required to do this scales faster then quadratic (somewhere between quadratic and cubic), because more DMUs also increase size of matrices $X$ and $Y$ and time to solve each individual linear problem (so the number of linear prolems increases and size of each problem increases). Given that solving DEA instances (computing efficiency for each DMU) for cases > 1000 even for moderate size of input $x$ and outputs $y$ like 5 and 3 lead to hours of computations even using parralel code on several CPU cores.

**Complexity of the Problem**

Given input and output matrices $X$ and $Y$, the above linear program must be solved separately for each DMU. The computational cost of solving these problems grows super-quadratically with the number of DMUs ($n$), because both the number of linear programs and the size of each program (determined by the number of DMUs and variables) increase as $n$ increases. Specifically, the size of each individual linear program grows with $n$ (the number of DMUs appears in both constraints and variables), so total computational effort increases faster than $O(n^2)$—often approaching cubic complexity for large datasets.

As a result, evaluating DEA efficiency for datasets with more than 1,000 DMUs, even with a moderate number of inputs (e.g., $m = 5$) and outputs (e.g., $s = 3$), can require hours of computation—even when using parallel processing on multiple CPU cores.

**Improving Computational Performance**

A standard way to reduce computational time in DEA is to exploit the fact that the efficiency of each DMU can be determined using only the set of efficient DMUs, rather than the full matrices $X$ and $Y$. In practice, for fixed input and output dimensions, the number of efficient DMUs tends to saturate as the dataset grows—adding more DMUs usually results in only a few additional efficient units. Therefore, a common strategy is to first identify the efficient set (referred to as the `full_base`), which is typically much smaller than the total number of DMUs, and then compute the efficiency of all other DMUs using only this set. The `DeaLargeScale` class implements this strategy to achieve significant computational improvements.      

**Steps in DeaLargeScale**

***Base Candidate Selection via Ratios***
Calculate efficiency-related ratios for each column (DMU) and select pleminary candidates.
Let denote candidate set to be $B_0$.

***Base Extension (Addbase)***
For candidates in $B_0$, solve the DEA model (e.g., linear programming) for each DMU in  matrixes $X$ and $Y$ (using as reference matrixes $X[B_0]$ and $Y[B_0]$ ) and retain those DMUs whose computed efficiency scores are greater than or equal to a 1:  
Let denote candidate set to be  $B_1$

***Base Refinement (Rebase)***
For each DMU in $B_1$ solve DEA using as reference $X[B_1]$ and $Y[B_1]$ and retain only efficient (set $B_2$). At this stage set $B_2$ should have complete subset of  efficient  DMU from original matrices $X$ and $Y$. This step is just to remove ineffient DMUs from $B_1$ set. 

***Final Compute*** 
For each DMU in  matrixes $X$ and $Y$ (using as reference matrixes $X[B_2]$ and $Y[B_2]$). We still solve ($n$) linear problems (the total number of DMUs) but the size of problems itselfs is significantly reduced.





**The Cauchy-Schwarz Inequality**\
$$\left( \sum_{k=1}^n a_k b_k \right)^2 \leq \left( \sum_{k=1}^n a_k^2 \right) \left( \sum_{k=1}^n b_k^2 \right)$$