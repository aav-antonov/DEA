#from ortools.linear_solver import pywraplp
import numpy as np
from multiprocessing import Pool


from senpy.utils.misc import get_logger, timer

from .dea_instance import Dea

  
    
@timer
def get_efficiency_for_list(dea, X, Y, type):
    q = []
    for i in range(X.shape[1]):  # Iterate through the rows of X (or Y)
        X_i = X[:, i]  # Get the i-th row of X as a 1D NumPy array
        Y_i = Y[:, i]  # Get the i-th row of Y as a 1D NumPy array

        if type =="x":    
            q.append(dea.get_efficiency_x( X_i ,Y_i))
        else:
            q.append(dea.get_efficiency_y( X_i ,Y_i))
    return q

    
class DeaMultiprocessing():    
    """
    Senpy class for DEA (Data Envelopment Analyses)

    """
 
    def __init__(self, THREAD_N = 8 ):
                
        self._logger = get_logger(self.__class__.__name__)
        self.THREAD_N = THREAD_N 

    @timer
    def set_DEA(self,X, Y, q_type ="x"):
        self.dea = Dea(X, Y)
        
  
    @timer
    def run(self,X, Y, q_type ="x"):
    
        self._logger.info(f"THREAD_N: {self.THREAD_N}, X: {X.shape}, Y: {Y.shape}")
        
        X_partitions = np.array_split(X, self.THREAD_N, axis=1)
        Y_partitions = np.array_split(Y, self.THREAD_N, axis=1)

        with Pool(processes=self.THREAD_N) as pool:
            data = pool.starmap(get_efficiency_for_list, zip([self.dea] * self.THREAD_N, X_partitions, Y_partitions, [q_type] * self.THREAD_N))

        # Use extend to add elements from sublists to flattened_data
        q = []
        for sublist in data:
            q.extend(sublist)
        
        return q
    


