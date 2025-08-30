DeaLargeScale: Mathematical Method Description
Data Envelopment Analysis (DEA):
DEA evaluates the relative efficiency of a set of decision-making units (DMUs) by analyzing their input/output combinations. Each DMU is represented by a vector of inputs ( X ) and outputs ( Y ).

Steps in DeaLargeScale
Base Candidate Selection via Ratios

Calculate efficiency-related ratios for each column (DMU) of the input/output matrices ( X, Y ).
Use a partitioning (intervals) heuristic, such as quantiles of these ratios, to select candidate base columns.
Let the indices of these candidates be ( C_0 \subseteq {1,\ldots,n} ).
Base Refinement (Rebase)

For candidates in ( C_0 ), solve the DEA model (e.g., linear programming) for each DMU and retain those whose computed efficiency scores are greater than or equal to a threshold (e.g., ( \theta \geq 0.99 )).
Define the refined base set:
[ B_1 = { j \in C_0 : \text{DEA}(X_j, Y_j) \geq 0.99 } ]
Base Extension (Addbase)

For remaining DMUs not in the base (( Q = {1,\ldots,n} \setminus B_1 )), run DEA and include in base those with efficiency scores above the threshold: [ B_2 = B_1 \cup { j \in Q : \text{DEA}(X_j, Y_j) \geq 0.99 } ]
Final Base Refinement

Repeat the base refinement on the extended set ( B2 ) to ensure only highly efficient units are included: [ B{\text{final}} = { j \in B_2 : \text{DEA}(X_j, Y_j) \geq 0.99 } ]
Efficiency Score Calculation

Using the final base set ( B{\text{final}} ), compute the DEA efficiency scores for all DMUs in the dataset: [ qX_i = \text{DEA}(X_i, Y_i \mid, \text{reference set } B{\text{final}}),\quad \forall i ]
Mathematical DEA Model
For each DMU ( i ), the input-oriented DEA efficiency score ( \theta_i ) is typically computed by solving:

[ \begin{align} \text{Minimize} \quad & \thetai \ \text{Subject to} \quad & \sum{j \in B{\text{final}}} \lambda_j X_j \leq \theta_i X_i \ & \sum{j \in B{\text{final}}} \lambda_j Y_j \geq Y_i \ & \sum{j \in B_{\text{final}}} \lambda_j = 1 \ & \lambda_j \geq 0,\quad \forall j \end{align} ]

where ( \lambda_j ) are the weights for constructing a "reference" DMU.

Summary:
DeaLargeScale efficiently prunes the set of DMUs to a base set of highly efficient candidates using ratio-based selection, iterative refinement, and extension. The final DEA efficiency scores for all DMUs are then calculated with respect to this optimized reference set, yielding a faster and scalable analysis for large datasets.