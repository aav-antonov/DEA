from ortools.linear_solver import pywraplp
import numpy as np

class Dea():
    
    """
    Class for DEA (Data Envelopment Analyses)
    
    fX numpy array 
    fY numpy array 

    """
 
    def __init__(self, fX, fY):
                
        self.check_input(fX, "fX")
        self.check_input(fY, "fY")
        
        self.fY = fY 
        self.fX = fX

        if fX.shape[1] !=  fY.shape[1]:
            raise ValueError(f'{self.__class__.__name__}: fX has different number of columns with fY: {fX.shape} != {fY.shape}')
        
        self.num_rows_x = fX.shape[0]
        self.num_rows_y = fY.shape[0]
        self.num_columns = fX.shape[1]
        self.set_convex_constraint(convex = [1,1])
        
        
    def set_convex_constraint(self, convex = [1,1]):
        [self.convexMin, self.convexMax] = convex 
        
    def check_input(self, X, decription):
        if isinstance(X, np.ndarray) and np.issubdtype(X.dtype, np.number):
            pass
        else:
            raise ValueError(f'{self.__class__.__name__}: {decription} is not numpy array')
        

    def matrix_constain(self,X,variables, type = "X"):    
        # Create constraints
        constraint_expr_x = []
        for i in range(X.shape[0]):
            constraint_expr = 0
            for j in range(X.shape[1]):
                if type == "X":
                    constraint_expr -= X[i, j] * variables[j]
                else:
                    constraint_expr += X[i, j] * variables[j]
            
            constraint_expr_x.append(constraint_expr)
            
        return constraint_expr_x

    def print_results(self, result_status, solver, variables, q):

        # Check the result status of the optimization solution
        if result_status == pywraplp.Solver.OPTIMAL:
            print("Solution found:")
            print(f'objective value: {solver.Objective().Value()}')
            for var in variables:
                if var.solution_value() > 0:
                    print(f'{var.name()} = {var.solution_value()}')
            print(f'{q.name()} = {q.solution_value()}')
            print("Problem solved in %f milliseconds" % solver.wall_time())
        else:
            print("The problem does not have an optimal solution.")
    
    def get_status(self, result_status):

        # Check the result status of the optimization solution
        if result_status == pywraplp.Solver.OPTIMAL:
            return 1
        else:
            return -1
        
    def get_basis(self, variables):
        basis = []
        for var in variables:
            if var.solution_value() > 0:
                basis.append([var.name(), var.solution_value()])
        return basis

    def get_efficiency_x(self, x, y):
        
        solver = pywraplp.Solver.CreateSolver("GLOP")
        
        q = solver.NumVar(0, solver.infinity(), "q")
        
        variables = [solver.NumVar(0, solver.infinity(), f'x{i+1}') for i in range(self.num_columns)]
        
        constraint_expr_x = self.matrix_constain(self.fX,variables, type = "X")
        constraint_expr_y = self.matrix_constain(self.fY,variables, type = "Y")
        
        for i,constraint_expr in enumerate(constraint_expr_x):
            solver.Add(constraint_expr + x[i] * q >= 0, f"ConstraintX_{i}")
    
        for i,constraint_expr in enumerate(constraint_expr_y):
            solver.Add(constraint_expr >=y[i],f"ConstraintY_{i}")
            
        constraint_a = 0
        for var in variables:
            constraint_a += var
        
        solver.Add( constraint_a <= self.convexMax)
        solver.Add( constraint_a >= self.convexMin)
        
        objective = solver.Objective()
        objective.SetCoefficient(q, 1)
        objective.SetMinimization()

        # Solve the linear program
        result_status = solver.Solve()
        
        #self.print_results(result_status,solver, variables, q)
        status = self.get_status(result_status)
        if status == 1:
            return q.solution_value()
        else:
            return 1e18
        
        
    
    def get_efficiency_y(self, x, y):
        
        solver = pywraplp.Solver.CreateSolver("GLOP")
        
        q = solver.NumVar(0, solver.infinity(), "q")
        
        variables = [solver.NumVar(0, solver.infinity(), f'x{i+1}') for i in range(self.num_columns)]
        
        constraint_expr_x = self.matrix_constain(self.fX,variables, type = "Y")
        constraint_expr_y = self.matrix_constain(self.fY,variables, type = "X")
        
        
        for i,constraint_expr in enumerate(constraint_expr_x):
            solver.Add(constraint_expr  <= x[i], f"ConstraintX_{i}")
    
        for i,constraint_expr in enumerate(constraint_expr_y):
            solver.Add(constraint_expr + y[i] * q <=0,f"ConstraintY_{i}")
            
        constraint_a = 0
        for var in variables:
            constraint_a += var
        
        solver.Add( constraint_a <= self.convexMax)
        solver.Add( constraint_a >= self.convexMin)
        
        objective = solver.Objective()
        objective.SetCoefficient(q, 1)
        objective.SetMaximization()

        # Solve the linear program
        result_status = solver.Solve()

        status = self.get_status(result_status)
        if status == 1:
            return q.solution_value()
        else:
            return 1e18
  
    

    
