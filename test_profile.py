
import numpy as np
import os
import timeit

from libDEA.dea_multiprocessing import DeaMultiprocessing
from libDEA.dea_largescale import DeaLargeScale
from libDEA.dea_profile import DeaProfile
##############################################

import numpy as np

def generateXY(m,fX_k,fY_k, fileX, fileY):

    # Ensure the folder exists
    os.makedirs(os.path.dirname(fileX), exist_ok=True)
    os.makedirs(os.path.dirname(fileY), exist_ok=True)
    
    X = np.random.uniform(0, 10, size=(fX_k, m))
    Y = np.random.uniform(0, 10, size=(fY_k, m))
    
    np.save(fileX, X)
    np.save(fileY, Y)
    
    return X,Y

X, Y = generateXY(m, fX_k, fY_k, fileX, fileY)

DP = DeaProfile()
DP.get_base(X, Y,  q_type ="x", steps = 10, size = 100)


x, y = X[:,5], Y[:,5]*0.2
DP.get_yx_profile( x, y )

DP.get_xx_profile( x, y , 0, 1)
DP.get_xx_profile( x, y , 1, 2)
DP.get_xx_profile( x, y , 0, 2)

# Example usage:
# X, Y = generate_base_XY(fX_k=3, fY_k=2, scale_range=range(1,11), N=1, bias=0.0)
    
    



    

