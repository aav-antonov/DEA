import matplotlib.pyplot as plt
import numpy as np
import pickle



from .dea_multiprocessing import DeaMultiprocessing
from .dea_largescale import DeaLargeScale

class DeaProfile():    
    """
    Class for DEA (Data Envelopment Analyses)

    """
 
    def __init__(self):
        self.DEALS = DeaLargeScale()
        
    
    def get_base(self, X, Y,  q_type ="x"):
        
        self.DEALS.get_full_base( X, Y, q_type =q_type)
        self.base = self.DEALS.full_base
        self.X = X
        self.Y = Y
    
    def get_yx_profile(self, x, y, file_output = "plot_yx.png" ):
        

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
        plt.scatter([1], [1], color='red', marker='o', label='input DMU')
        plt.title('Efficient frontier (Production function)')
        plt.legend()
        plt.grid(True)
        plt.ylim(bottom=0, top=np.max(y_filtered)+0.5)
        plt.savefig(file_output)
        plt.clf()

    def power_law_spacing(self, x_min, x_max, k, power=2):
        t = np.linspace(0, 1, k)
        return x_min + (x_max - x_min) * t ** power

    def get_x_series(self, X_base, i, x, k=10):
        """

        Parameters:
            X_base: numpy.ndarray, shape (n_samples, n_features)
            i: int, the column index to vary
            x: numpy.ndarray, shape (n_features,)
            k: int, number of grid points (default 100)

        Returns:
            x_series: numpy.ndarray, shape (k, n_features)
        """
        x_min_i = X_base[:, i].min()/64
        x_max_i = X_base[:, i].max()*64

        x_range_i = self.power_law_spacing(x_min_i, x_max_i, k,  power=3/2)

        # (maintaining the sorted order)
        insert_idx = np.searchsorted(x_range_i, x[i])

        # Insert x_i at the correct position
        x_range_i = np.insert(x_range_i, insert_idx, x[i])

        x_series = np.tile(x, ( k+1, 1))  # 2*k copies of x
        x_series[:, i] = x_range_i

        x_series = x_series.T

        return x_series

    def get_xx_profile(self, x, y , i, j , file_output = "plot_xx"):
        

        X_base = self.X[:,self.base] # numpy
        k = 100
        x_series_i = self.get_x_series(X_base, i, x, k)

        y_i  = np.column_stack([y.copy() for _ in range(k+1)])

        self.DEALS.set_DEA(self.X[:, self.base], self.Y[:, self.base], q_type = "x")

        qXi = self.DEALS.DEAM.run(x_series_i, y_i , q_type = "x")
        qXi = np.array(qXi)
        mask = qXi < 1e+6

        qx_series_i = qXi * x_series_i  # Multiply each row by corresponding qXi
        qx_series_i = qx_series_i[:, mask]

        if qx_series_i.shape[0] == 0 or qx_series_i.shape[1] == 0:
            raise ValueError(f"Looks like DMU\n x: {x}\ny:{y}\n is above Efficient frontier")

        x_axes_i = qx_series_i[i, :]
        x_axes_j = qx_series_i[j, :]


        self.plot_xx(x_axes_i, x_axes_j, x, i, j, file_output = "plot_xx")

    def plot_xx(self,x_axes_i, x_axes_j, x, i, j, file_output = "plot_xx"):

        # Plotting
        print("Plotting plot_xx i, j:", i, j)


        plt.plot(x_axes_i, x_axes_j, color='blue', linewidth=1, label='Efficient frontier')

        plt.xlabel(f'x{j}')
        plt.ylabel(f'x{i}')
        plt.scatter(  x[i], x[j],   color='red', marker='o', label='input DMU')
        plt.title('Slice (x,x) of Efficient frontier (Production function)')
        plt.legend()
        plt.grid(True)
        plt.ylim(bottom=0, top=2.5* x[j] + 0.5)
        plt.xlim(left=0, right=2.5 * x[i] + 0.5)

        plt.savefig(f'{file_output}_{i}_{j}.png')
        plt.clf()    





    
