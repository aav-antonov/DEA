**Data Envelopment Analysis (DEA)**

DEA evaluates the relative efficiency of a set of decision-making units (DMUs) by analyzing their input/output combinations. Each DMU is represented by a vector of inputs $x$ and outputs $y$. For multiple DMUs, inputs and outputs are organized into matrices $X$ and $Y$.

The classical input-oriented DEA efficiency score for a DMU $o$ (where $o = 1, \ldots, n$) is computed by solving the following linear program:

$$
\begin{align*}
\text{Minimize}\quad & \theta \\\\
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
- $\theta$: efficiency score for DMU $o$ ($\theta \leq 1$; $\theta = 1$ means efficient).

The solution $\theta^*$ is the efficiency of DMU $o$. A DMU is considered efficient if $\theta^* = 1$, and inefficient if $\theta^* < 1$ compared to the rest of the dataset.

**Steps in DeaLargeScale**

Base Candidate Selection via Ratios

Calculate efficiency-related ratios for each column (DMU) of the 
Use a partitioning (intervals) heuristic, such as quantiles of these ratios, to select candidate base columns.
Let the indices of these candidates be $C_0 \subseteq {1, \ldots, n}$.
Base Refinement (Rebase)

For candidates in $C_0$, solve the DEA model (e.g., linear programming) for each DMU and retain those whose computed efficiency scores are greater than or equal to a threshold (e.g., $\theta \geq 0.99$).
Define the refined base set:
$$ B_1 = { j \in C_0 : \operatorname{DEA}(X_j, Y_j) \geq 0.99 } $$
Base Extension (Addbase)

For remaining DMUs not in the base ($Q = {1, \ldots, n} \setminus B_1$), run DEA and include in base those with efficiency scores above the threshold: $$ B_2 = B_1 \cup { j \in Q : \operatorname{DEA}(X_j, Y_j) \geq 0.99 } $$
Final Base Refinement

Repeat the base refinement on the extended set $B2$ to ensure only highly efficient units are included: $$ B{\text{final}} = { j \in B_2 : \operatorname{DEA}(X_j, Y_j) \geq 0.99 } $$
Efficiency Score Calculation

Using the final base set $B{\text{final}}$, compute the DEA efficiency scores for all DMUs in the dataset: $$ qX_i = \operatorname{DEA}(X_i, Y_i \mid \text{reference set } B{\text{final}}), \quad \forall i $$
Mathematical DEA Model
For each DMU $i$, the input-oriented DEA efficiency score $\theta_i$ is typically computed by solving:

$$ \begin{align} \text{Minimize} \quad & \thetai \\ \text{Subject to} \quad & \sum{j \in B{\text{final}}} \lambda_j X_j \leq \theta_i X_i \\ & \sum{j \in B{\text{final}}} \lambda_j Y_j \geq Y_i \\ & \sum{j \in B_{\text{final}}} \lambda_j = 1 \\ & \lambda_j \geq 0,\quad \forall j \end{align} $$

where $\lambda_j$ are the weights for constructing a "reference" DMU.


**The Cauchy-Schwarz Inequality**\
$$\left( \sum_{k=1}^n a_k b_k \right)^2 \leq \left( \sum_{k=1}^n a_k^2 \right) \left( \sum_{k=1}^n b_k^2 \right)$$