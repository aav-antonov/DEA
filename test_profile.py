
import numpy as np
import os
import timeit

from libDEA.dea_multiprocessing import DeaMultiprocessing
from libDEA.dea_largescale import DeaLargeScale
from libDEA.dea_profile import DeaProfile
##############################################

import numpy as np

def generate_base_XY(fX_k, fY_k, scale_range, N, bias=0.0):
    """
    Generates efficient DMUs based on inputs and outputs directions.
    - fX_k: number of input features
    - fY_k: number of output features
    - scale_range: sequence of scale values, e.g., range(1,11)
    - N: number of 'directional' DMUs per scale value
    - bias: add this constant to x_sum and y_sum
    Returns:
        X: (fX_k, num_DMUs) input matrix
        Y: (fY_k, num_DMUs) output matrix
    """
    
    xy_sum =[]
    for scale_i in scale_range:
        xy_sum.append([bias + scale_i, np.sqrt(scale_i)])
        

        
    X_list = []
    Y_list = []
    for _ in range(N):
            # Random proportions that sum to 1 (Dirichlet is ideal)
        alfaX = np.random.dirichlet(np.ones(fX_k))
        alfaY = np.random.dirichlet(np.ones(fY_k))
        X_direction, Y_direction = [], []
        for [x,y] in xy_sum:
            
            X_direction.append(x * alfaX) # Shape: (fX_k,)
            Y_direction.append(y * alfaY)# Shape: (fY_k,)
            X = np.column_stack(X_direction)
            Y = np.column_stack(Y_direction)
            #print(X.shape, Y.shape)
        X_list.append(X)
        Y_list.append(Y)
    
    X = np.column_stack(X_list)
    Y = np.column_stack(Y_list)
    return X, Y
    
X, Y = generate_base_XY(3, 2, range(1,11), 500, bias=2.0)

DP = DeaProfile()
DP.get_base(X, Y,  q_type ="x", steps = 10, size = 100)

qX2 = DP.DEALS.run(X, Y, q_type="x", steps=5, size=100)
print(qX2)
x, y = X[:,5], Y[:,5]*0.75
DP.get_yx_profile( x, y )

# Example usage:
# X, Y = generate_base_XY(fX_k=3, fY_k=2, scale_range=range(1,11), N=1, bias=0.0)
    
    



    

