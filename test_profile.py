print("""
This script demonstrates the use of Data Envelopment Analysis (DEA) for visualizing the efficiency of decision-making units (DMUs).

DEA (Data Envelopment Analysis) is a method for evaluating the efficiency of DMUs based on their inputs and outputs.

Main steps:
- Generates random datasets of DMU inputs and outputs.
- Initializes a DEA profiler.
- Profiles the efficiency and resource usage of a selected DMU.
- Produces visual output (slices in multidimensional space of X and Y) to visualize efficiency frontier.

Plots are saved to disk as PNG files for further inspection.
""")


import numpy as np
from libDEA.dea_profile import DeaProfile
##############################################

def generateXY(m, fX_k, fY_k):
    """
    Generate random input (X) and output (Y) matrices for DMUs.
    """
    X = np.random.uniform(0, 10, size=(fX_k, m))
    Y = np.random.uniform(0, 10, size=(fY_k, m))
    return X, Y

# Specify parameters for DMUs and spaces
print("Setting number of DMUs and input/output dimensions.")
m = 250    # number of DMUs
fX_k = 5   # size of resource space (number of inputs)
fY_k = 3   # size of product space (number of outputs)

# Generate random X and Y matrices
print("Generating random input (X) and output (Y) data for DMUs.")
X, Y = generateXY(m, fX_k, fY_k)

# Initialize DeaProfile class and set X and Y as base
print("Initializing DEA profile and setting base X and Y data.")
DP = DeaProfile()
DP.get_base(X, Y, q_type="x")

# Select a DMU to profile
dmu_index = 5
print(f"Selecting DMU with index {dmu_index} for profiling and making its outputs inefficient.")
x, y = X[:, dmu_index], Y[:, dmu_index] * 0.7  # scale output to simulate inefficiency

# Example of plotting y(x) profile
print("Generating and saving y(x) profile plot for selected DMU.")
DP.get_yx_profile(x, y, file_output="plot_yx.png")

# Example of plotting x(x) profile for different input pairs
print("Generating and saving x(x) profile plots for selected DMU with different input indices.")
DP.get_xx_profile(x, y, 0, 1, file_output="plot_xx")  # see plot_xx_0_1.png
DP.get_xx_profile(x, y, 1, 2, file_output="plot_xx")  # see plot_xx_1_2.png
DP.get_xx_profile(x, y, 0, 2, file_output="plot_xx")  # see plot_xx_0_2.png

print("All profiles generated and saved successfully.")