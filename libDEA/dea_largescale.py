
import numpy as np
import pickle

from libDEA.dea_multiprocessing import DeaMultiprocessing
from libDEA.utils import timer


class DeaLargeScale():    
    """
    Senpy class for DEA (Data Envelopment Analyses)

    """
 
    def __init__(self, THREAD_N = 8 ):
                
        self.THREAD_N = THREAD_N
        self.DEAM = DeaMultiprocessing(THREAD_N = self.THREAD_N)

        
    @timer
    def get_base(self,X, Y, q_type ="x", steps = 10, size = 100):
        
        print(f"DeaLargeScale() get_base THREAD_N: {self.THREAD_N}, X: {X.shape}, Y: {Y.shape}")
        
        init_base_columns = self.init_base(X, Y, q_type =q_type, steps = steps, size = size)
        
        full_base_columns = self.full_base( init_base_columns, X, Y, q_type = q_type)
        
        return full_base_columns
    
    @timer
    def save_me(self,X, Y, full_base_columns, file_out = "dea.pkl"):
     
        # Create a dictionary to store your data
        data_dict = {'X': X, 'Y': Y, 'base': full_base_columns}

        # Save the dictionary to a file using pickle
        with open(file_out, 'wb') as f:
            pickle.dump(data_dict, f)

    @timer
    def load_me(self, file_dea = "dea.pkl"):
        
        # Load the data back
        with open(file_dea, 'rb') as f:
            data = pickle.load(f) 
        
        X = data['X']
        Y = data['Y']
        base = data['base']

        return X, Y, base

    @timer
    def run(self,X, Y, q_type ="x", steps = 10, size = 100):
    
        full_base = self.get_base(X, Y, q_type =q_type, steps = steps, size = size)
        
        qX = self.get_scores(full_base, X, Y, q_type =q_type)
        
        self.check_full_base(full_base, qX)
        
        return qX
    
    @timer
    def set_DEA(self,X, Y, q_type ="x"):
        self.DEAM.set_DEA(X, Y, q_type =q_type)

        
    @timer
    def full_base(self, base_columns, X, Y, q_type ="x"):
            
        self.set_DEA(X[:, base_columns], Y[:, base_columns], q_type = q_type)
        qX = self.DEAM.run(X, Y , q_type = q_type)
         
        full_base_columns = self.rebase(np.where(np.array(qX) >= 0.99)[0] , X,Y,q_type ="x")
        
        print(f"full_base:: full_base_columns!!!! {full_base_columns.shape}")
        
        return full_base_columns
    
    @timer
    def get_scores(self, base_columns, X, Y, q_type ="x"):
        
        self.set_DEA(X[:, base_columns], Y[:, base_columns], q_type = q_type)
        
        qX = self.DEAM.run(X, Y , q_type = q_type)
         
        return qX

    @timer
    def check_full_base(self, base_columns, qX):

        base_columns_new = np.where(np.array(qX) >= 0.99)[0]
        
        if np.array_equal(base_columns , base_columns_new ):
            print("check_full_base is OK!!!") 
        else:
            print("ERROR: check_full_base FAILED")
            exit()
    
    
    @timer
    def rebase(self, base_columns, X, Y, q_type ="x"):
        
        print("rebase in:", type(base_columns))
        
        self.set_DEA(X[:, base_columns], Y[:, base_columns], q_type = q_type)
        qX = self.DEAM.run(X[:, base_columns], Y[:, base_columns] , q_type = q_type)
        base_columns = base_columns[np.where( np.array(qX) >= 0.99)]
        print("rebase out:", type(base_columns))
        return base_columns
   

    @timer
    def addbase(self, base_columns, q_columns, X, Y, q_type ="x"):
    
        print(f"addbase:: BASE X_base: {X[:, base_columns].shape}")
        print(f"addbase:: Q X_q: {X[:, q_columns].shape}")
        
        self.set_DEA(X[:, base_columns], Y[:, base_columns], q_type = q_type)
      
        qX = self.DEAM.run(X[:, q_columns], Y[:, q_columns] , q_type = q_type)
                
        base_columns = np.union1d(base_columns, q_columns[np.where(np.array(qX) >= 0.99)])
        
        return base_columns
        
        
    @timer
    def init_base_check(self, unique_columns, base_columns, X, Y, q_type ="x"):
        
        base_columns_new = self.addbase(base_columns,np.array(list(unique_columns)), X,Y,q_type ="x")
        
        if np.array_equal(base_columns , base_columns_new):
            print("init_base_check is OK!!!") 
        else:
            print("ERROR: init_base_check FAILED")
            exit()
            
    @timer
    def init_base(self,X, Y, q_type ="x", steps = 10, size = 100):
        
        unique_columns = set()
        
        base_columns = self.select_rand( X,Y, size)
        base_columns = self.rebase(base_columns, X,Y,q_type ="x")
                
        unique_columns.update(base_columns)
        
        for i in range(steps):
            q_columns = self.select_rand( X,Y, size)
            base_columns = self.addbase(base_columns,q_columns, X,Y,q_type ="x")
            base_columns = self.rebase(base_columns, X,Y,q_type ="x")
            
            unique_columns.update(q_columns)
        
        ### use this to check if something goes wrong
        self.init_base_check(unique_columns, base_columns, X, Y, q_type ="x")
        
        return base_columns
    
    def select_rand(self, X,Y, size):
                
        if size is not None:
            n = X.shape[1]
            # Randomly select column indices
            random_columns = np.random.choice(n, size, replace=False)
            return random_columns
        
        all_columns = np.arange(n)
        return all_columns

    
