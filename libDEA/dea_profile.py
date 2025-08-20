import matplotlib.pyplot as plt
import numpy as np
import pickle



from .dea_multiprocessing import DeaMultiprocessing
from .dea_largescale import DeaLargeScale

class DeaProfile():    
    """
    Senpy class for DEA (Data Envelopment Analyses)

    """
 
    def __init__(self):
        self.DEALS = DeaLargeScale()
        
    
    def get_base(self, X, Y,  q_type ="x", steps = 10, size = 100):
        
        self.base = self.DEALS.get_base(X, Y, q_type =q_type, steps = steps, size = size)
        self.X = X
        self.Y = Y
    
    def get_yx_profile(self, x, y ):
        
        print(x.shape)
        # Create an array with multiples of x from 0.1 to 2.0
        m = np.arange(0.1, 10.1, 0.1)
        xP = x * m[:, np.newaxis]
        yP = y * m[:, np.newaxis]
        
        xP = xP.T
        yP = yP.T
                
        
        
        self.DEALS.set_DEA(self.X[:, self.base], self.Y[:, self.base], q_type = "x")
        
        qY = self.DEALS.DEAM.run(xP, yP , q_type = "y")
        qY = np.array(qY)
        qY[qY > 1e+10] = 0
                        
        y = qY * m
        
        mask = (y != 0)
        m_filtered = m[mask]
        y_filtered = y[mask]

        # Include the point (0, y0) at the beginning
        m_filtered = np.concatenate(([m_filtered[0] ], m_filtered))
        y_filtered = np.concatenate(([0], y_filtered))
        
        # Plotting
        plt.plot(m_filtered, y_filtered)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.scatter([1], [1], color='red', marker='o', label='agent') 
        plt.title('Production function')
        plt.legend()
        plt.grid(True)
        plt.ylim(bottom=0, top=np.max(y_filtered)+0.5)
        plt.savefig('plot_yx.png')
        plt.clf()


        
    
    def get_xx_profile(self, x, y , i,j):
        
        # Generate a series of arrays with x[1] incremented by k
        k_values = np.arange(0, 10)
        xPi = np.column_stack([x.copy() for _ in k_values])
        xPi[i, :] += k_values* xPi[i, 0]*0.5
        
        xPj = np.column_stack([x.copy() for _ in k_values])
        xPj[j, :] += k_values* xPi[j, 0]*0.5

        yP  = np.column_stack([y.copy() for _ in k_values])
                
        self.DEALS.set_DEA(self.X[:, self.base], self.Y[:, self.base], q_type = "x")
        
        qXi = self.DEALS.DEAM.run(xPi, yP , q_type = "x")
        qXi = np.array(qXi)
        qXi[qXi > 1e+10] = 0
        
        qXj = self.DEALS.DEAM.run(xPj, yP , q_type = "x")
        qXj = np.array(qXj)
        qXj[qXj > 1e+10] = 0
        
        qxPi = xPi*qXi
        
        y_axes_i = qxPi[i, :]
        x_axes_i = qxPi[j, :]
        
        qxPj = xPj*qXj

        y_axes_j = qxPj[i, :]
        x_axes_j = qxPj[j, :]
       
        y_axes = np.concatenate((y_axes_i, y_axes_j[::-1]))
        x_axes = np.concatenate((x_axes_i, x_axes_j[::-1]))
        
        # Plotting
        #plt.plot(x_axes, y_axes)
        plt.plot(x_axes_i, y_axes_i, label='Slice 1')
        plt.plot(x_axes_j[::-1], y_axes_j[::-1], label='Slice 2')

        min_x_i = np.min(x_axes_i)
        max_x_j = np.max(x_axes_j)

        # Draw a line from (min_x_i, max_x_j) to (min_x_i, max_x_j + 1)
        plt.plot([min_x_i, min_x_i], [max_x_j, max_x_j + 1], color='green', linewidth=2, label='Edge')
        
        plt.xlabel(f'x{j}')
        plt.ylabel(f'x{i}')
        plt.scatter(  xPj[j, 0], xPj[i, 0],  color='red', marker='o', label='agent') 
        plt.title('Slice of Production function')
        plt.legend()
        plt.grid(True)
        plt.ylim(bottom=0, top=np.max(y_axes)+0.5)
        plt.savefig(f'plot_xx_{i}_{j}.png')
        plt.clf()    





    
