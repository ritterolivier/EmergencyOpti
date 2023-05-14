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
        self._center_demand = {} 
        self.center = center
        self.village = village

    def print(self):
        print(f"Max demand: {self._max_demand:.2f}")

        drone_dict = {}
        supplied_villages = {} # Added line
        for i, j, k in self._alloc:
            if self._alloc[(i, j, k)]:
                if k in drone_dict:
                    drone_dict[k].append((j, i))
                else:
                    drone_dict[k] = [(j, i)]
                self._supplied[j] = True
                # add demand of village to corresponding center
                self._center_demand[i] = self._center_demand.get(i, 0) + self.village.get_demand(j)
                # Add village to supplied_villages
                if j in supplied_villages:
                    supplied_villages[j].append(k)
                else:
                    supplied_villages[j] = [k]

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
            if self._supplied[village]:
                print(village, end=', ')
        print("\n")

        print("Unsupplied villages:")
        for village in self.village.get_all_ids():
            if not self._supplied[village]:
                print(village, end=', ')
        print("\n")

        for drone in drone_dict:
            print(f"Drone {drone} serves:")
            total_consumption = 0
            for village, center in drone_dict[drone]:
                consumption = self._drone_consumption[(center, village, drone)]
                print(f"\tVillage {village} from center {center} with consumption {consumption:.2f} Wh")
                total_consumption += consumption  # Add the consumption of this trip to the total
            print(f"Total consumption for drone {drone}: {total_consumption:.2f} Wh")

        # Check for multiple drones serving the same village
        for village, drones in supplied_villages.items():
            if len(drones) > 1:
                print(f"Warning: Village {village} is supplied by multiple drones: {', '.join(map(str, drones))}")
            else : 
                print(f"Village {village} is not supplied by multiple drones: {', '.join(map(str, drones))}")

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


