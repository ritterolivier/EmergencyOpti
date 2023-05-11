import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from JSInstance import JSInstance

class Solution:
    # constructor
    def __init__(self, max_demand=None, alloc=None, drone_comsumption=None):
        self._max_demand = max_demand
        self._alloc = alloc
        self._drone_consumption = {}
        

    def print(self):
        print("Max demand: {}".format(self._max_demand))
        print("Drone allocation:")
        for i, j, k in self._alloc:
            if self._alloc[(i, j, k)]:
                print(f"Drone {k} from center {i} to village {j}")
        for drone, consumption in self._drone_consumption.items():
            print(f"Drone {drone}: {consumption:.2f} Wh")
    
    def test(self, ptimesscen, type_solver):
        """
        Plot the performances of a given mathematical formulation against randomly generated scenarios.

        Parameters:
        - ptimesscen: matrix of processing times for each job on each machine for multiple scenarios
        - type_solver: string representing the type of mathematical formulation to be tested
        """
        nbscenarios = ptimesscen.shape[0]
        results = np.zeros(nbscenarios)
        for s in range(nbscenarios):
            results[s] = self.compute_makespan(ptimesscen[s])
        
        print(" ** Average makespan with the " + type_solver + " model: {}".format(results.mean()))

        plt.hist(results, bins=20, density=True)
        plt.title("Performances of the " + type_solver + " model")
        plt.savefig("hist_"+type_solver+"_cmax.pdf", format='pdf', bbox_inches='tight')
        plt.show()


