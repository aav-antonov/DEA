
import numpy as np
import os
import timeit

from libDEA.dea_multiprocessing import DeaMultiprocessing
from libDEA.dea_largescale import DeaLargeScale

##############################################

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
def run_dea_largescale(m, fX_k, fY_k):
    # Prepare file names
    fileX = f'mydata/X{m}_{fX_k}_{fY_k}.npy'
    fileY = f'mydata/Y{m}_{fX_k}_{fY_k}.npy'

    # Generate and load data
    X, Y = generateXY(m, fX_k, fY_k, fileX, fileY)
    X = np.load(fileX)
    Y = np.load(fileY)

    execution_time = {}
    print(f"Running DeaLargeScale with m={m}, fX_k={fX_k}, fY_k={fY_k}")

    
    # Run DeaLargeScale
    DEALS = DeaLargeScale(THREAD_N=8)
    start_time = timeit.default_timer()
    qX2 = DEALS.run(X, Y, q_type="x")
    elapsed_time = timeit.default_timer() - start_time
    execution_time['DeaLargeScale'] = elapsed_time

    print(f"DeaLargeScale elapsed time: {elapsed_time:.4f} seconds")
    qX2 = np.array(qX2)

    

    return execution_time

def run_dea_comparison(m, fX_k, fY_k):
    # Prepare file names
    fileX = f'mydata/X{m}_{fX_k}_{fY_k}.npy'
    fileY = f'mydata/Y{m}_{fX_k}_{fY_k}.npy'

    # Generate and load data
    X, Y = generateXY(m, fX_k, fY_k, fileX, fileY)
    X = np.load(fileX)
    Y = np.load(fileY)

    execution_time = {}
    print(f"Running DEA comparison with m={m}, fX_k={fX_k}, fY_k={fY_k}")
    # Run DeaMultiprocessing
    DEAMP = DeaMultiprocessing()
    DEAMP.set_DEA(X, Y, q_type="x")

    start_time = timeit.default_timer()
    qX1 = DEAMP.run(X, Y, q_type="x")
    elapsed_time = timeit.default_timer() - start_time

    execution_time['DeaMultiprocessing'] = elapsed_time
    print(f"DeaMultiprocessing elapsed time: {elapsed_time:.4f} seconds")
    qX1 = np.array(qX1)

    # Run DeaLargeScale
    DEALS = DeaLargeScale()
    start_time = timeit.default_timer()
    qX2 = DEALS.run(X, Y, q_type="x")
    elapsed_time = timeit.default_timer() - start_time
    execution_time['DeaLargeScale'] = elapsed_time

    print(f"DeaLargeScale elapsed time: {elapsed_time:.4f} seconds")
    qX2 = np.array(qX2)

    # Compare outputs
    assert np.allclose(qX1, qX2, atol=1e-8), \
        "Results from DeaMultiprocessing and DeaLargeScale do not match!"
    print("DeaMultiprocessing and DeaLargeScale returned the same results.")

    return execution_time


print("""
This script benchmarks and tests the performance and correctness of two DEA implementations.

DEA (Data Envelopment Analysis) is a method for evaluating the efficiency of decision-making units (DMUs) based on their inputs and outputs.

- DeaMultiprocessing: Base method that computes efficiency for each unit directly using multiprocessing.
- DeaLargeScale: Optimized version designed for large-scale data and improved performance.

Random datasets of varying sizes are generated, both methods are executed, results are compared for accuracy, and computation time is measured.
""")

# Example of how to call the function:
execution_time_all = []
m = 250
fX_k = 5
fY_k = 3
for k in range(1, 7):
    
    print(f"Running DEA comparison for m={m}, fX_k={fX_k}, fY_k={fY_k}")
    
    if k < 4:   # Run the DEA comparison
        etime = run_dea_comparison(m=m, fX_k=5, fY_k=3)
        execution_time_all.append([f"m={m}, fX_k={fX_k}, fY_k={fY_k}",etime])
    else:  # Run the DeaLargeScale
        etime = run_dea_largescale(m=m, fX_k=5, fY_k=3)
        execution_time_all.append([f"m={m}, fX_k={fX_k}, fY_k={fY_k}",etime])
    m *=2

for [setsize, execution_time] in execution_time_all:
    for key, value in execution_time.items():
        print(f"{setsize} {key}: {value:.4f} seconds")

