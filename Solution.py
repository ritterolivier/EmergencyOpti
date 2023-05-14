import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from JSInstance import JSInstance

class Solution:
    # constructor
    def __init__(self, center=None, village=None, max_demand=None, alloc=None, drone_comsumption=None, open=None):
        self._max_demand = max_demand
        self._alloc = alloc
        self._drone_consumption = drone_comsumption if drone_comsumption else {}
        self._open = open if open else {}
        self._supplied = {}
        self._center_demand = {}  # New attribute to store total demand for each center
        self.center = center
        self.village = village

    def print(self):
        print(f"Max demand: {self._max_demand:.2f}")
        print("Opened centers:")
        for center in self.center.get_all_ids():
            if center in self._open:
                print(center, end=', ')
        print("\n")
        print("Unopened centers:")
        for center in self.center.get_all_ids():
            if center not in self._open:
                print(center, end=', ')
        print("\n")
        print("Supplied villages:")
        for village in self.village.get_all_ids():
            if village in self._supplied:
                print(village, end=', ')
        print("\n")
        print("Unsupplied villages:")
        for village in self.village.get_all_ids():
            if village not in self._supplied:
                print(village, end=', ')
        print("\n")
        drone_dict = {}
        for i, j, k in self._alloc:
            if self._alloc[(i, j, k)]:
                if k in drone_dict:
                    drone_dict[k].append((j, i))
                else:
                    drone_dict[k] = [(j, i)]
                self._supplied[j] = True
                # add demand of village to corresponding center
                self._center_demand[i] = self._center_demand.get(i, 0) + self.village.get_demand(j)
        for drone in drone_dict:
            print(f"Drone {drone} serves:")
            for village, center in drone_dict[drone]:
                print(f"\tVillage {village} from center {center} with consumption {self._drone_consumption[(center, village, drone)]:.2f} Wh")
        # print total demand for each center
        print("Total demand for each center:")
        for center, demand in self._center_demand.items():
            print(f"\tCenter {center}: {demand:.2f}")
    
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


