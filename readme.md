**Data Envelopment Analysis (DEA)**

DEA evaluates the relative efficiency of a set of decision-making units (DMUs) by analyzing their input/output combinations. Each DMU is represented by a vector of inputs $x$ and outputs $y$. For multiple DMUs, inputs and outputs are organized into matrices $X$ and $Y$. See more details in my PhD related paper [Open DEA.pdf](DEA.pdf) 

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
Calculate efficiency-related ratios for each column (DMU) and select preliminary candidates.  
Let the candidate set be denoted as $B_0$.

***Base Extension (Addbase)***  
For each DMU in $B_0$, solve the DEA model (e.g., linear programming) using the reference sets $X[B_0]$ and $Y[B_0]$. Retain those DMUs whose computed efficiency scores are greater than or equal to $1$.  
Let this refined set be denoted as $B_1$.

***Base Refinement (Rebase)***  
For each DMU in $B_1$, solve DEA using $X[B_1]$ and $Y[B_1]$ as reference sets, and retain only the efficient DMUs, yielding set $B_2$. At this stage, $B_2$ should contain the complete subset of efficient DMUs from the original $X$ and $Y$. This step ensures removal of any inefficient DMUs from $B_1$.

***Final Compute***  
For each DMU in the original matrices $X$ and $Y$, solve DEA using the reference sets $X[B_2]$ and $Y[B_2]$. Thus, we still solve $n$ linear programs (one per DMU), but the size of each problem is significantly reduced compared to using the full set.





