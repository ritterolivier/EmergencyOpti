import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

class Charts():

    def __init__(self, solution=None, centres=None, villages=None, time=None):
        self._solution = solution
        self._centres = centres
        self._villages = villages
        self._time = time

    def plot_solution(self):
        # Create the scatter plots
        fig, ax = plt.subplots(figsize=(10, 6))

        # Get the list of all centers and villages
        all_centers = list(self._centres.get_localisation_dict().keys())
        all_villages = list(self._villages.get_localisation_dict().keys())
        
        # Get the opened centers
        opened_centers = self._solution.get_opened_centers()

        # Get the allocation of each center if applicable
        if(self._solution.get_modelType() == 'Deterministic' or self._solution.get_modelType() == 'Robust'):
            center_village_association = self._solution.get_center_village_association()
        else:
            center_village_association = {}

        # Create lists of latitudes and longitudes for non-supplied and supplied villages
        non_supplied_village_lats = []
        non_supplied_village_lons = []
        supplied_village_lats = []
        supplied_village_lons = []

        # Iterate over all villages and separate them to supplied and non-supplied
        for v in all_villages:
            lat, lon = self._villages.get_localisation(v)
            if any(v in village_list for village_list in center_village_association.values()):
                supplied_village_lats.append(lat)
                supplied_village_lons.append(lon)
            else:
                non_supplied_village_lats.append(lat)
                non_supplied_village_lons.append(lon)

        # Draw non-supplied villages
        ax.scatter(non_supplied_village_lons, non_supplied_village_lats, c='blue', s=10)
        
        # Draw supplied villages
        ax.scatter(supplied_village_lons, supplied_village_lats, c='purple', s=10)
        for lat, lon, v in zip(supplied_village_lats, supplied_village_lons, all_villages):
            ax.text(lon, lat, str(v), fontsize=10, color='purple')

        # Draw centers with different colors based on their status
        for c in all_centers:
            lat, lon = self._centres.get_localisation(c)
            color = 'green' if c in opened_centers else 'red'
            shape = '^'
            ax.scatter(lon, lat, c=color, marker=shape)
            if c in opened_centers:
                ax.text(lon, lat, str(c), fontsize=10, color=color)

        # Draw lines from each open center to the villages they supply
        for c, villages in center_village_association.items():
            center_lat, center_lon = self._centres.get_localisation(c)
            for v in villages:
                village_lat, village_lon = self._villages.get_localisation(v)
                ax.plot([center_lon, village_lon], [center_lat, village_lat], 'k--')

        # Add labels and legend
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')

        from matplotlib.lines import Line2D
        legend_elements = [Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=10, label='Non-supplied villages'),
                        Line2D([0], [0], marker='o', color='w', markerfacecolor='purple', markersize=10, label='Supplied villages'),
                        Line2D([0], [0], marker='^', color='w', markerfacecolor='red', markersize=10, label='Classic Center'),
                        Line2D([0], [0], marker='^', color='w', markerfacecolor='green', markersize=10, label='Drone Center')]
        ax.legend(handles=legend_elements, loc='upper right')

    # Set title and save the figure
        if(self._solution.get_modelType() == 'Deterministic'):
            filename = f'{self._solution.get_modelType()}{self._solution.get_beta()}.png'
            plt.title(f'Villages and Centers for {self._solution.get_modelType()} method\nDemand met : {self._solution.get_of():.2f}\n Beta : {self._solution.get_beta()}\n Time : {self._time:.2f}s')
        if(self._solution.get_modelType() == 'Robust'):
            filename = f'{self._solution.get_modelType()}{self._solution.get_gamma()}.png'
            plt.title(f'Villages and Centers for {self._solution.get_modelType()} method\nDemand met : {self._solution.get_of():.2f}\n Gamma : {self._solution.get_gamma()}\n Time : {self._time:.2f}s')
        if(self._solution.get_modelType() == 'Stochastic'):
            filename = f'{self._solution.get_modelType()}.png'
            plt.title(f'Villages and Centers for {self._solution.get_modelType()} method - {self._solution.get_nb_scena()} Scenarios\nMean demand met : {self._solution.get_of():.2f}\n Time : {self._time:.2f}s')

        fig.savefig(filename)

    def plot_dronesCenters(self):
        # Get the drone-center associations
        drone_dict = self._solution.get_drone_association()

        # Create lists for center IDs and drone IDs
        center_ids = []
        drone_ids = []

        # Iterate over the drone_dict
        for center, drones in drone_dict.items():
            for drone in drones:
                # Append the center and drone IDs to the respective lists
                center_ids.append(center)
                drone_ids.append(drone)

        # Create the scatter plot
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Scatter plot with colors based on the y-value (center ID)
        for i in range(len(center_ids)):
            color = 'red' if center_ids[i] % 2 == 0 else 'blue'
            ax.scatter(drone_ids[i], center_ids[i], c=color, marker='s')
            ax.text(drone_ids[i], center_ids[i], f'{drone_ids[i]}', fontsize=9, ha='right')

        # Set yticks to the unique center_ids where drones are assigned
        ax.set_yticks(list(set(center_ids)))
        
        # Add labels and legend
        plt.xlabel('Drone IDs')
        plt.ylabel('Center IDs')

        if(self._solution.get_modelType() == 'Deterministic'):
            filename = f'{self._solution.get_modelType()}{self._solution.get_beta()}Drones.png'
            plt.title(f'Drones - Centers for {self._solution.get_modelType()} method\nDemand met : {self._solution.get_of():.2f}\n Beta : {self._solution.get_beta()}\n Time : {self._time:.2f}s')
        if(self._solution.get_modelType() == 'Robust'):
            filename = f'{self._solution.get_modelType()}{self._solution.get_gamma()}Drones.png'
            plt.title(f'Drones - Centers for {self._solution.get_modelType()} method\nDemand met : {self._solution.get_of():.2f}\n Gamma : {self._solution.get_gamma()}\n Time : {self._time:.2f}s')
        if(self._solution.get_modelType() == 'Stochastic'):
            filename = f'{self._solution.get_modelType()}Drones.png'
            plt.title(f'Drones - Centers for {self._solution.get_modelType()} method - {self._solution.get_nb_scena()} Scenarios\nMean demand met : {self._solution.get_of():.2f}\n Time : {self._time:.2f}s')

        # Save the plot
        fig.savefig(filename)