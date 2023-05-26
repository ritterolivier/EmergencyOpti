import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from JSInstance import JSInstance

class Solution:
    # constructor
    def __init__(self, center=None, village=None, max_demand=None, alloc=None, drone_comsumption=None, open=None, drone_center=None):
        self._max_demand = max_demand
        self._alloc = alloc
        self._drone_consumption = drone_comsumption if drone_comsumption else {}
        self._open = open if open else {}
        self._drone_center = drone_center if drone_center else {}
        self._supplied = {}
        self._center_demand = {} 
        self._opened_centers = {}
        self.center = center
        self.village = village

    def get_open(self):
        return self._open
    
    def get_max_demand(self):
        return self._max_demand
    
    def get_opened_center(self):
        return self._opened_centers
    
    def get_supplied(self):
        return self._supplied

    def get_drone_center(self):
        return self._drone_center        

    def print(self):
        print(f"Max demand: {self._max_demand:.2f}")

        drone_dict = {}
        supplied_villages = {} 
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
                self._opened_centers[i] = True

        print("Opened centers:")
        for center in self.center.get_all_ids():
            if center in self._opened_centers:  # if center is in opened_centers dictionary, it is open
                print(center, end=', ')
        print("\n")

        '''print("Closed centers:")
        for center in self.center.get_all_ids():
            if center not in self._opened_centers:  # if center is not in opened_centers dictionary, it is not open
                print(center, end=', ')
        print("\n")'''

        print("Supplied villages:")
        for village in self.village.get_all_ids():
            if self._supplied[village]:
                print(village, end=', ')
        print("\n")

        '''print("Unsupplied villages:")
        for village in self.village.get_all_ids():
            if not self._supplied[village]:
                print(village, end=', ')
        print("\n")'''

        for drone in drone_dict:
            print(f"Drone {drone} serves:")
            total_consumption = 0
            for village, center in drone_dict[drone]:
                consumption = self._drone_consumption[(center, village, drone)]
                print(f"\tVillage {village} from center {center} with consumption {consumption:.2f} Wh")
                total_consumption += consumption  # Add the consumption of this trip to the total
            print(f"Total consumption for drone {drone}: {total_consumption:.2f} Wh")

        '''# Check for multiple drones serving the same village
        for village, drones in supplied_villages.items():
            if len(drones) > 1:
                print(f"Warning: Village {village} is supplied by multiple drones: {', '.join(map(str, drones))}")
            else : 
                print(f"Village {village} is not supplied by multiple drones: {', '.join(map(str, drones))}")'''

        print("Total demand and drones for each center:")
        for center, demand in self._center_demand.items():
            drones = [v for (c, v), drone in self._drone_center.items() if c == center and drone == 1.0]
            drones_str = ', '.join(map(str, drones)) if drones else "No drone assigned"
            print(f"\tCenter {center}: {demand:.2f}, Drone: {drones_str}")
    
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


    def __str__(self):
        # Create a string to hold the formatted solution representation
        solution_str = ""

        # Add the maximum demand
        solution_str += f"Max demand: {self._max_demand:.2f}\n"

        # Add the opened centers
        solution_str += "Opened centers:\n"
        for center in self.center.get_all_ids():
            if center in self._opened_centers:
                solution_str += f"{center}, "
        solution_str += "\n"

        '''# Add the closed centers
        solution_str += "Closed centers:\n"
        for center in self.center.get_all_ids():
            if center not in self._opened_centers:
                solution_str += f"{center}, "
        solution_str += "\n"'''

        # Add the supplied villages
        solution_str += "Supplied villages:\n"
        for village in self.village.get_all_ids():
            if self._supplied[village]:
                solution_str += f"{village}, "
        solution_str += "\n"

        '''# Add the unsupplied villages
        solution_str += "Unsupplied villages:\n"
        for village in self.village.get_all_ids():
            if not self._supplied[village]:
                solution_str += f"{village}, "
        solution_str += "\n"'''

        # Add the drone information
        drone_dict = {}
        supplied_villages = {}
        for i, j, k in self._alloc:
            if self._alloc[(i, j, k)]:
                if k in drone_dict:
                    drone_dict[k].append((j, i))
                else:
                    drone_dict[k] = [(j, i)]
                self._supplied[j] = True
                self._center_demand[i] = self._center_demand.get(i, 0) + self.village.get_demand(j)
                if j in supplied_villages:
                    supplied_villages[j].append(k)
                else:
                    supplied_villages[j] = [k]
                self._opened_centers[i] = True

        for drone in drone_dict:
            solution_str += f"Drone {drone} serves:\n"
            total_consumption = 0
            for village, center in drone_dict[drone]:
                consumption = self._drone_consumption[(center, village, drone)]
                solution_str += f"\tVillage {village} from center {center} with consumption {consumption:.2f} Wh\n"
                total_consumption += consumption
            solution_str += f"Total consumption for drone {drone}: {total_consumption:.2f} Wh\n"

        '''# Check for multiple drones serving the same village
        for village, drones in supplied_villages.items():
            if len(drones) > 1:
                solution_str += f"Warning: Village {village} is supplied by multiple drones: {', '.join(map(str, drones))}\n"
            else:
                solution_str += f"Village {village} is not supplied by multiple drones: {', '.join(map(str, drones))}\n"'''

        solution_str += "Total demand and drones for each center:\n"
        for center, demand in self._center_demand.items():
            drones = [v for (c, v), drone in self._drone_center.items() if c == center and drone == 1.0]
            drones_str = ', '.join(map(str, drones)) if drones else "No drone assigned"
            solution_str += f"\tCenter {center}: {demand:.2f}, Drones: {drones_str}\n"




        # Return the formatted solution string
        return solution_str


