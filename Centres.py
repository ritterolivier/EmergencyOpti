import numpy as np
import pandas as pd
from JSInstance import JSInstance
import math
from scipy.spatial import distance

class Centres(JSInstance):
    def __init__(self, datafile="data_drones.xlsx", sheetname="Help centers"):
        # Initialize the parent class (JSInstance)
        super().__init__(datafile, sheetname)
        self._localisation_dict = self.create_localisation_dict()

    def create_localisation_dict(self):
        localisation_dict = self._processtimes[["Latitude", "Longitude"]].apply(tuple, axis=1).to_dict()
        return localisation_dict

    def get_localisation(self, id):
        return self._localisation_dict.get(id)
    
    def get_all_ids(self):
        return list(self._localisation_dict.keys())

    def get_localisation_dict(self):
        return self._localisation_dict
    
    
    def euclidean_distance(self, point1, point2):
        lat1, lon1 = point1
        lat2, lon2 = point2
        return np.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)
    
    def haversine_distance(self, point1, point2):
        lat1, lon1 = point1
        lat2, lon2 = point2
        # Convert latitude and longitude from degrees to radians
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        return math.acos(math.sin(lat1) * math.sin(lat2) + math.cos(lat1) * math.cos(lat2) * math.cos(lon2 - lon1)) * 6371
    
    def create_village_distance_dict(self, village_obj):
        village_localisation_dict = village_obj.get_localisation_dict()
        center_village_distance_dict = {}

        for center_id, center_loc in self._localisation_dict.items():
            center_village_distance_dict[center_id] = {}
            for village_id, village_loc in village_localisation_dict.items():
                center_village_distance_dict[center_id][village_id] = self.haversine_distance(center_loc, village_loc)
                #math.dist(center_loc, village_loc)
                #self.euclidean_distance(center_loc, village_loc)

        self.village_distance_dict = center_village_distance_dict

    def get_distance_from_village(self, center_key, village_key):
        return self.village_distance_dict[center_key][village_key]


if __name__ == "__main__":
    centre = Centres()
    centre.print()

    print("Localization dict:")
    print(centre.get_localisation_dict())

    # Test the get methods
    id_to_test = 4
    print(f"Localization for id {id_to_test}: {centre.get_localisation(id_to_test)}")

    # Test the new methods
    print("All IDs:")
    print(centre.get_all_ids())

    print("Complete localisation dictionary:")
    print(centre.get_localisation_dict())
