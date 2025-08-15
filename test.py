
import numpy as np
import os
import timeit

from libDEA.dea_multiprocessing import DeaMultiprocessing
from libDEA.dea_largescale import DeaLargeScale
from libDEA.dea_profile import DeaProfile
##############################################


def compare_dea_methods(X, Y):
    execution_time = {}

    # Run DeaMultiprocessing
    DEAMP = DeaMultiprocessing(THREAD_N=8)
    DEAMP.set_DEA(X, Y, q_type="x")

    start_time = timeit.default_timer()
    qX1 = DEAMP.run(X, Y, q_type="x")
    elapsed_time = timeit.default_timer() - start_time

    execution_time['DeaMultiprocessing'] = elapsed_time
    print(f"DeaMultiprocessing elapsed time: {elapsed_time:.4f} seconds")
    qX1 = np.array(qX1)

    # Run DeaLargeScale
    DEALS = DeaLargeScale(THREAD_N=8)
    start_time = timeit.default_timer()
    qX2 = DEALS.run(X, Y, q_type="x", steps=5, size=100)
    elapsed_time = timeit.default_timer() - start_time
    execution_time['DeaLargeScale'] = elapsed_time

    print(f"DeaLargeScale elapsed time: {elapsed_time:.4f} seconds")
    qX2 = np.array(qX2)

    # Compare outputs
    assert np.allclose(qX1, qX2, atol=1e-8), \
        "Results from DeaMultiprocessing and DeaLargeScale do not match!"

    print("Both methods returned the same results.")

    return execution_time

#     
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


def run_dea_comparison(m, fX_k, fY_k):
    # Prepare file names
    fileX = f'mydata/X{m}_{fX_k}_{fY_k}.npy'
    fileY = f'mydata/Y{m}_{fX_k}_{fY_k}.npy'

    # Generate and load data
    X, Y = generateXY(m, fX_k, fY_k, fileX, fileY)
    X = np.load(fileX)
    Y = np.load(fileY)

    execution_time = {}

    # Run DeaMultiprocessing
    DEAMP = DeaMultiprocessing(THREAD_N=8)
    DEAMP.set_DEA(X, Y, q_type="x")

    start_time = timeit.default_timer()
    qX1 = DEAMP.run(X, Y, q_type="x")
    elapsed_time = timeit.default_timer() - start_time

    execution_time['DeaMultiprocessing'] = elapsed_time
    print(f"DeaMultiprocessing elapsed time: {elapsed_time:.4f} seconds")
    qX1 = np.array(qX1)

    # Run DeaLargeScale
    DEALS = DeaLargeScale(THREAD_N=8)
    start_time = timeit.default_timer()
    qX2 = DEALS.run(X, Y, q_type="x", steps=5, size=100)
    elapsed_time = timeit.default_timer() - start_time
    execution_time['DeaLargeScale'] = elapsed_time

    print(f"DeaLargeScale elapsed time: {elapsed_time:.4f} seconds")
    qX2 = np.array(qX2)

    # Compare outputs
    assert np.allclose(qX1, qX2, atol=1e-8), \
        "Results from DeaMultiprocessing and DeaLargeScale do not match!"
    print("Both methods returned the same results.")

    return execution_time

# Example of how to call the function:
execution_time = run_dea_comparison(m=100, fX_k=5, fY_k=3)
for key, value in execution_time.items():
    print(f"{key}: {value:.4f} seconds")

exit()

# print(times) 
 
  
m = 100
fX_k = 5
fY_k = 3

fileX = f'mydata/X{m}_{fX_k}_{fY_k}.npy'
fileY = f'mydata/Y{m}_{fX_k}_{fY_k}.npy'

X,Y = generateXY(m,fX_k,fY_k, fileX, fileY)

X = np.load(fileX)
Y = np.load(fileY)

execution_time = compare_dea_methods(X, Y)

for key, value in execution_time.items():
    print(f"{key}: {value:.4f} seconds")

exit()

############################
DEAMP = DeaMultiprocessing(THREAD_N = 8)
DEAMP.set_DEA(X, Y, q_type ="x")


start_time = timeit.default_timer()
qX1 = DEAMP.run(X, Y, q_type="x")
elapsed_time = timeit.default_timer() - start_time

execution_time = {}
execution_time['DeaMultiprocessing'] = elapsed_time

print(f"Elapsed time: {elapsed_time:.4f} seconds")
qX1 = np.array(qX1)

# Run DeaLargeScale

DEALS = DeaLargeScale(THREAD_N = 8)
start_time = timeit.default_timer()
qX2 = DEALS.run(X, Y, q_type ="x",steps = 5, size = 100)
elapsed_time = timeit.default_timer() - start_time
execution_time['DeaLargeScale'] = elapsed_time


qX2 = np.array(qX2)

for key, value in execution_time.items():
    print(f"{key}: {value:.4f} seconds")






assert np.allclose(qX1, qX2, atol=1e-8), "Results from DeaMultiprocessing and DeaLargeScale do not match!"

print("Both methods returned the same results.")

print(qX1[:10])
print(qX2[:10])



    
    

