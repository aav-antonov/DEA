
import numpy as np
import pickle

from libDEA.dea_multiprocessing import DeaMultiprocessing
from libDEA.utils import timer
from libDEA.select_base_by_rations import SelectBaseCandidates
import os




class DeaLargeScale():    
    """
    Class for DEA (Data Envelopment Analyses)

    """
 
    def __init__(self, THREAD_N = None ):

        if THREAD_N is None:
            num_cores = os.cpu_count()
            print(f"DeaLargeScale()::Detected CPU cores: {num_cores}")
            THREAD_N = num_cores
        else:
            num_cores = THREAD_N
                
        self.THREAD_N = THREAD_N
        self.DEAM = DeaMultiprocessing(THREAD_N = self.THREAD_N)

    def run(self, X, Y, q_type ="x", intervals=5):
        
        self.X, self.Y = X, Y
        
        #Compute candidates for the base columns using ratios 
        SBC = SelectBaseCandidates(X, Y, intervals=intervals)
        
        #Compute the base columns by removing non-efficient ones
        base_columns = self.rebase( np.array(SBC.base_indexes), X, Y, q_type =q_type)
        q_columns_np = np.array(list(set(range(X.shape[1])) - set(base_columns)))
        
        #Extend the base columns by finding efficient ones in q_columns
        base_columns = self.addbase(base_columns, q_columns_np , X, Y, q_type =q_type)
        
        #Final compute of the base columns by removing non-efficient ones
        self.full_base = self.rebase( base_columns, X, Y, q_type ="x")
        
        #Final compute scores for all columns 
        qX = self.get_scores(self.full_base, X, Y, q_type ="x")

        return qX

    
    def save_me(self, file_out = "dea.pkl"):
     
        # Create a dictionary to store your data
        data_dict = {'X': self.X, 'Y': self.Y, 'base': self.full_base}

        # Save the dictionary to a file using pickle
        with open(file_out, 'wb') as f:
            pickle.dump(data_dict, f)

    def load_me(self, file_dea = "dea.pkl"):
        
        # Load the data back
        with open(file_dea, 'rb') as f:
            data = pickle.load(f) 
        
        self.X = data['X']
        self.Y = data['Y']
        self.full_base = data['base']

    
    def set_DEA(self,X, Y, q_type ="x"):
        self.DEAM.set_DEA(X, Y, q_type =q_type)

    
    def get_scores(self, base_columns, X, Y, q_type ="x"):
        
        self.set_DEA(X[:, base_columns], Y[:, base_columns], q_type = q_type)
        qX = self.DEAM.run(X, Y , q_type = q_type)
         
        return qX

    
    def rebase(self, base_columns, X, Y, q_type ="x"):
        """
        Compute the base columns by removing non-efficient ones
        """
        self.set_DEA(X[:, base_columns], Y[:, base_columns], q_type = q_type)
        qX = self.DEAM.run(X[:, base_columns], Y[:, base_columns] , q_type = q_type)
        base_columns = base_columns[np.where( np.array(qX) >= 0.99)]
        return base_columns
   

    def addbase(self, base_columns, q_columns, X, Y, q_type ="x"):
        """
        Extend the base columns by finding efficient ones in q_columns
        """
        self.set_DEA(X[:, base_columns], Y[:, base_columns], q_type = q_type)
        qX = self.DEAM.run(X[:, q_columns], Y[:, q_columns] , q_type = q_type)
        base_columns = np.union1d(base_columns, q_columns[np.where(np.array(qX) >= 0.99)])
        
        return base_columns
    
    

    

