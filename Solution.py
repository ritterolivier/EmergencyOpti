import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from JSInstance import JSInstance

class Solution:
    # constructor
    def __init__(self, instance=None, cmax=None, alloc=None):
        self._instance = instance
        self._makespan = cmax
        self._alloc = alloc

    def print(self):
        print("Makespan: {}".format(self._makespan))
        print("Job allocation:")
        for j in self._alloc.columns:
            print("Machine {}: {}".format(j, self._alloc.index[self._alloc[j]==1].tolist()))

    def compute_makespan(self, ptimes):
        """Compute the realized makespan for a given matrix of processing times."""
        cmax = 0
        for j in self._instance._processtimes.columns:
            cmax = max(cmax, np.dot(ptimes[:,j-1], self._alloc[j]))

        return(cmax)

    def test(self, ptimesscen, type_solver):
        """ Plot the performances of a given mathematical formulation against randomly generated scenrios."""
        nbscenarios = ptimesscen.shape[0]
        results = np.zeros(nbscenarios)
        for s in range(nbscenarios):
            results[s] = self.compute_makespan(ptimesscen[s])
        
        print(" ** Average makespan with the " + type_solver + " model: {}".format(results.mean()))

        plt.hist(results, bins=20, density=True)
        plt.title("Performances of the " + type_solver + " model")
        plt.savefig("hist_"+type_solver+"_cmax.pdf", format='pdf', bbox_inches='tight')
        plt.show()


