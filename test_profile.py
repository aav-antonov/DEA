
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

#generate random X and Y
m = 250 #number of DMUs
fX_k = 5 #size of resouce space (inputs of DMU) )
fY_k = 3 #size of product space (outputs of DMU) )
X, Y = generateXY(m, fX_k, fY_k, fileX, fileY)

#init class Profile class and set X and Y
DP = DeaProfile()
DP.get_base(X, Y,  q_type ="x")


#select a DMU to profile (in this case with index 5)
x, y = X[:,5], Y[:,5]*0.2  # also scale output to make it inefficient

#Example of plotting y(x) profile
DP.get_yx_profile( x, y, file_output = "plot_yx.png" )

#Example of plotting x(x) profile
DP.get_xx_profile( x, y , 0, 1, file_output = "plot_xx") # see plot_xx_0_1.png
DP.get_xx_profile( x, y , 1, 2, file_output = "plot_xx") # see plot_xx_1_2.png
DP.get_xx_profile( x, y , 0, 2, file_output = "plot_xx") # see plot_xx_0_2.png

    
    



    

