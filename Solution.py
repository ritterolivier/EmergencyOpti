import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from JSInstance import JSInstance

class Solution:
    # constructor
    def __init__(self, modelType=None, center=None, village=None, of=None, alloc=None, open=None, drone_center=None, demand=None, gamma=None, beta=None, scena=None):
        self._modelType = modelType
        self._center = center
        self._village = village
        self._of = of
        self._alloc = alloc
        self._open = open 
        self._drone_center = drone_center 
        self._demand = demand
        self._gamma = gamma
        self._beta = beta
        self._scena = scena


    def get_nb_scena(self):
        return self._scena

    def get_modelType(self):
        return self._modelType
    
    def get_of(self):
        return self._of
    
    def get_gamma(self):
        return self._gamma
    
    def get_beta(self):
        return self._beta


    def get_opened_centers(self):
        # Compute the list of opened centers from the _open variable
        return [key for key, value in self._open.items() if value > 0]
    

    def get_drone_association(self):
        # Create a dict with centers as keys and the list of drones associated as values
        drone_dict = {}
        for (center, drone), value in self._drone_center.items():
            if value > 0:
                if center in drone_dict:
                    drone_dict[center].append(drone)
                else:
                    drone_dict[center] = [drone]
        return drone_dict
    
    def get_center_weights(self):
        # Create a dict with center as key and the sum of the var values as value
        center_weights = {}
        for (center, village, drone), value in self._demand.items():
            if value > 0:
                if center in center_weights:
                    center_weights[center] += value
                else:
                    center_weights[center] = value
        return center_weights

    def get_village_weights(self):
        # Create a dict with village as key and the sum of the var values as value
        village_weights = {}
        for (center, village, drone), value in self._demand.items():
            if value > 0:
                if village in village_weights:
                    village_weights[village] += value
                else:
                    village_weights[village] = value
        return village_weights

    def get_drone_weights(self):
        # Create a dict with drone as key and the sum of the var values as value
        drone_weights = {}
        for (center, village, drone), value in self._demand.items():
            if value > 0:
                if drone in drone_weights:
                    drone_weights[drone] += value
                else:
                    drone_weights[drone] = value
        return drone_weights
    

    def get_village_association(self):
        # Create a dict with centers as keys and the list of villages associated as values
        village_dict = {}
        for (center, village, drone), value in self._alloc.items():
            if value > 0:
                if center in village_dict:
                    if village not in village_dict[center]:  # avoid duplicate entries
                        village_dict[center].append(village)
                else:
                    village_dict[center] = [village]
        return village_dict
    
    def get_drone_village_association(self):
        # Create a dict with drones as keys and the list of villages associated as values
        drone_village_dict = {}
        for (center, village, drone), value in self._alloc.items():
            if value > 0:
                if drone in drone_village_dict:
                    if village not in drone_village_dict[drone]:  # avoid duplicate entries
                        drone_village_dict[drone].append(village)
                else:
                    drone_village_dict[drone] = [village]
        return drone_village_dict
    

    def get_village_drone_association(self):
        # Create a dict with villages as keys and the list of drones associated as values
        drone_village_dict = {}
        for (center, village, drone), value in self._alloc.items():
            if value > 0:
                if village in drone_village_dict:
                    if drone not in drone_village_dict[village]:  # avoid duplicate entries
                        drone_village_dict[village].append(drone)
                else:
                    drone_village_dict[village] = [drone]
        return drone_village_dict
    
    def get_center_village_association(self):
    # Create a dict with centers as keys and the list of villages associated as values
        center_village_dict = {}
        for (center, village, drone), value in self._alloc.items():
            if value > 0:
                if center in center_village_dict:
                    if village not in center_village_dict[center]:  # avoid duplicate entries
                        center_village_dict[center].append(village)
                else:
                    center_village_dict[center] = [village]
        return center_village_dict


    def print_stoch(self):
        opened_centers = self.get_opened_centers()
        drone_association = self.get_drone_association()
        print(f"Model type: {self._modelType}")
        print(f"Demand met: {self._of:.2f}")



    def print_classic(self):
        opened_centers = self.get_opened_centers()
        drone_association = self.get_drone_association()
        village_association = self.get_village_association()
        drone_village_association = self.get_drone_village_association()
        village_drone_association = self.get_village_drone_association()
        center_weights = self.get_center_weights()
        village_weights = self.get_village_weights()
        drone_weights = self.get_drone_weights()

            

        print(f"Model type: {self._modelType}")
        print(f"Demand met: {self._of:.2f}")
        print(f"Opened centers: {', '.join(map(str, opened_centers))}")
        for center, drones in drone_association.items():
            print(f"Center {center} (Total weight: {format(center_weights[center], '.2f')}): Drones {', '.join(map(str, drones))}")
        for center, villages in village_association.items():
            print(f"Center {center}: Villages {', '.join(map(str, villages))}")
        for village, drones in village_drone_association.items():
            print(f"Village {village}: Drones {', '.join(map(str, drones))}")
        for drone, villages in drone_village_association.items():
            if drone in drone_weights:
                print(f"Drone {drone} (Total weight: {drone_weights[drone]}): Villages {', '.join(map(str, villages))}")
            else:
                print(f"Drone {drone} (No recorded weight): Villages {', '.join(map(str, villages))}")
        for village, weight in village_weights.items():
            village_demand = self._village.get_demand(village)
            print(f"Village {village}: Total weight {weight}, Demand {village_demand}")



    
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


