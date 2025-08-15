
import numpy as np
import os

from libDEA.dea_multiprocessing import DeaMultiprocessing
from libDEA.dea_largescale import DeaLargeScale
from libDEA.dea_profile import DeaProfile
##############################################    
#Example()
def generateXY(m,fX_k,fY_k, fileX, fileY):

    # Ensure the folder exists
    os.makedirs(os.path.dirname(fileX), exist_ok=True)
    os.makedirs(os.path.dirname(fileY), exist_ok=True)
    
    X = np.random.uniform(0, 10, size=(fX_k, m))
    Y = np.random.uniform(0, 10, size=(fY_k, m))
    
    np.save(fileX, X)
    np.save(fileY, Y)
    
    return X,Y
    
    
    
##############################################  
m = 100
fX_k = 5
fY_k = 3

fileX = f'mydata/X{m}_{fX_k}_{fY_k}.npy'
fileY = f'mydata/Y{m}_{fX_k}_{fY_k}.npy'

X,Y = generateXY(m,fX_k,fY_k, fileX, fileY)

X = np.load(fileX)
Y = np.load(fileY)

############################
DEAMP = DeaMultiprocessing(THREAD_N = 8)
DEAMP.set_DEA(X, Y, q_type ="x")
qX1 = DEAMP.run(X, Y, q_type ="x")
qX1 = np.array(qX1)
print(qX1.shape)

DEALS = DeaLargeScale(THREAD_N = 8)
qX2 = DEALS.run(X, Y, q_type ="x",steps = 5, size = 100)
qX2 = np.array(qX2)

print(qX2.shape)


assert np.allclose(qX1, qX2, atol=1e-8), "Results from DeaMultiprocessing and DeaLargeScale do not match!"

print("Both methods returned the same results.")

print(qX1[:10])
print(qX2[:10])



    
    

