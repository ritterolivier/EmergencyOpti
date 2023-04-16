import numpy as np
import pandas as pd
from JSInstance import JSInstance

class Villages(JSInstance):
    def __init__(self, datafile="data_drones.xlsx", sheetname="Demand points"):
        # Initialize the parent class (JSInstance)
        super().__init__(datafile, sheetname)
        self._localisation_dict = self.create_localisation_dict()
        self._demand_dict = self.create_demand_dict()


    def create_demand_dict(self):
        demand_dict = self._processtimes["Quantity (kg)"].to_dict()
        return demand_dict

    def create_localisation_dict(self):
        localisation_dict = self._processtimes[["Latitude", "Longitude"]].apply(tuple, axis=1).to_dict()
        return localisation_dict

    def get_localisation(self, id):
        return self._localisation_dict.get(id)


    def get_demand(self, id):
        return self._demand_dict.get(id)
    
    def get_all_ids(self):
        return list(self._demand_dict.keys())

    def get_demand_dict(self):
        return self._demand_dict

    def get_localisation_dict(self):
        return self._localisation_dict
    
    def euclidean_distance(self, point1, point2):
        lat1, lon1 = point1
        lat2, lon2 = point2
        return np.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)
    
    def create_center_distance_dict(self, center_obj):
        center_localisation_dict = center_obj.get_localisation_dict()
        village_center_distance_dict = {}

        for village_id, village_loc in self.get_localisation_dict().items():
            village_center_distance_dict[village_id] = {}
            for center_id, center_loc in center_localisation_dict.items():
                village_center_distance_dict[village_id][center_id] = self.euclidean_distance(village_loc, center_loc)

        self.center_distance_dict = village_center_distance_dict



if __name__ == "__main__":
    village = Villages()
    village.print()

    print("Demand dict:")
    print(village.get_demand_dict())

    print("Localization dict:")
    print(village.get_localisation_dict())

    # Test the get methods
    id_to_test = 4
    print(f"Demand for id {id_to_test}: {village.get_demand(id_to_test)}")
    print(f"Localization for id {id_to_test}: {village.get_localisation(id_to_test)}")

    # Test the new methods
    print("All IDs:")
    print(village.get_all_ids())

    print("Complete demand dictionary:")
    print(village.get_demand_dict())

    print("Complete localisation dictionary:")
    print(village.get_localisation_dict())
