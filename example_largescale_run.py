
import numpy as np

from libDEA.dea_multiprocessing import DeaMultiprocessing
from libDEA.dea_largescale import DeaLargeScale
from libDEA.dea_profile import DeaProfile
##############################################    
#Example()
def generateXY(m,fX_k,fY_k, fileX, fileY):
    
    X = np.random.uniform(0, 10, size=(fX_k, m))
    Y = np.random.uniform(0, 10, size=(fY_k, m))
    
    np.save(fileX, X)
    np.save(fileY, Y)
    
    return X,Y
    
    
    
##############################################  
m = 10000
fX_k = 5
fY_k = 3

fileX = f'mydata/X{m}_{fX_k}_{fY_k}.npy'
fileY = f'mydata/Y{m}_{fX_k}_{fY_k}.npy'

#X,Y = generateXY(m,fX_k,fY_k, fileX, fileY)

X = np.load(fileX)
Y = np.load(fileY)



DEAProfile = DeaProfile(THREAD_N = 8)

#DEAProfile.get_base(X, Y,  q_type ="x", steps = 10, size = 100)

DEAProfile.get_xx_profile(X[:,1296], Y[:,1296],2,0)

DEAProfile.get_yx_profile( X[:,1596], Y[:,1596])

exit()

DEALS = DeaLargeScale(THREAD_N = 8)
qX = DEALS.run(X, Y, q_type ="x",steps = 5, size = 100)

exit()

DEAMP = DeaMultiprocessing(THREAD_N = 8)
DEAMP.set_DEA(X, Y, q_type ="x")
qX = DEAMP.run(X, Y, q_type ="x")
qX = np.array(qX)
print(qX.shape)
# [END program]
exit()


    
    

