import pulp
import numpy as np
import pandas as pd
from Matrix import Matrix
from Villages import Villages
from Centres import Centres
from Deterministic import Deterministic
from Stochastic import Stochastic
from StochasticG import StochasticG
from Robust import Robust
import random
from tqdm import tqdm

"""# Import custom modules
from JSInstance import JSInstance

villages = JSInstance("data_drones.xlsx", "Demand points")
centres = JSInstance("data_drones.xlsx", "Help centers")

matrix = Matrix(villages, centres); 


for row in matrix.get_matrix():
    print(row, "\n")
    print("\n")

print(len(matrix.get_matrix()))
print(len(matrix.get_matrix()[0]))
"""


if __name__ == "__main__":
    centres = Centres()

    # Create a Villages object
    villages = Villages()

    # Compute the distance between each center and village
    centres.create_village_distance_dict(villages)
    villages.create_center_distance_dict(centres)

    '''# Print the nested dictionary of distances from each center to each village
    print("Center to Village distances:")
    for center_id, distances in centres.village_distance_dict.items():
        print(f"Center {center_id}:")
        for village_id, distance in distances.items():
            print(f"\tVillage {village_id}: {distance:.2f} km")

    # Print the nested dictionary of distances from each village to each center
    print("Village to Center distances:")
    for village_id, distances in villages.center_distance_dict.items():
        print(f"Village {village_id}:")
        for center_id, distance in distances.items():
            print(f"\tCenter {center_id}: {distance:.2f} km")

    with open("center_to_village_distances.txt", "w") as f:
        print("Center to Village distances:", file=f)
        for center_id, distances in centres.village_distance_dict.items():
            print(f"Center {center_id}:", file=f)
            for village_id, distance in distances.items():
                print(f"\tVillage {village_id}: {distance:.2f} km", file=f)

    # Print the nested dictionary of distances from each village to each center to a text file
    with open("village_to_center_distances.txt", "w") as f:
        print("Village to Center distances:", file=f)
        for village_id, distances in villages.center_distance_dict.items():
            print(f"Village {village_id}:", file=f)
            for center_id, distance in distances.items():
                print(f"\tCenter {center_id}: {distance:.2f} km", file=f)

                distances_match = True
    for center_id, center_distances in centres.village_distance_dict.items():
        for village_id, center_distance in center_distances.items():
            village_distance = villages.center_distance_dict[village_id][center_id]
            if center_distance != village_distance:
                distances_match = False
                break

    # Print the result
    if distances_match:
        print("All distances between centers and villages are the same.")
    else:
        print("Not all distances between centers and villages are the same.")


    print(centres.get_distance_from_village(1,1))'''

    # Create and solve the problem with the deterministic method
    detsolver = Deterministic(centres, villages)
    detsolver.create_model()
    detsolver.solve_milp()

    # Get the solution
    detsol = detsolver.get_solution()

    # Print the solution
    detsol.print()



    # Create and solve the problem with the stochastic method
    detsolver = StochasticG(centres, villages)
    detsolver.create_model()
    detsolver.solve_milp()

    # Get the solution
    detsol = detsolver.get_solution()

    # Print the solution
    detsol.print()

'''

    # Create and solve the problem with the Stochastic method
    stochDic = {}

    for i in tqdm(range(0,100)):
        beta = random.uniform(2.5,3)
        stochsolver = Stochastic(centres, villages, detsolver, beta)
        stochsolver.create_model()
        stochsolver.solve_milp()

        # Get the solution
        stochsol = stochsolver.get_solution()

        # Print the solution
        stochsol.print()

        stochDic[i] = [stochsol, beta]

        with open('stochresult.txt', 'a') as f:
            f.write(f'Iteration: {i}\n')
            f.write(f'Beta value: {beta}\n')
            f.write('Solution:\n')
            f.write(str(stochsol))  # Write the solution. The solution class should have an appropriate __str__ method.
            f.write('\n')

    import matplotlib.pyplot as plt
    import operator

    betas = []
    max_demands = []

    # Loop through the dictionary and extract the beta and max_demand values
    for i in stochDic:
        solution, beta = stochDic[i]
        betas.append(beta)
        max_demands.append(solution.get_max_demand())

    # Create the scatter plot
    plt.figure(figsize=(10, 6))
    plt.scatter(betas, max_demands, alpha=0.6)
    plt.title("Beta vs Max Demand")
    plt.xlabel("Beta")
    plt.ylabel("Max Demand")
    plt.grid(True)
    plt.show()


    # Initialize a dictionary to keep track of the supply count for each village
    village_supply_count = {}

    # Loop through the dictionary and count the supply for each village
    for i in stochDic:
        solution, beta = stochDic[i]
        supplied_villages = solution.get_supplied()
        for village, supplied in supplied_villages.items():
            if supplied:  # Only increment the count if the village has been supplied
                if village in village_supply_count:
                    village_supply_count[village] += 1
                else:
                    village_supply_count[village] = 1

    # Prepare data for the plot
    villages = list(village_supply_count.keys())
    supply_counts = list(village_supply_count.values())

    # Sort the dictionary by supply count in descending order
    sorted_villages = sorted(village_supply_count.items(), key=operator.itemgetter(1), reverse=True)

    # Extract village IDs and supply counts into separate lists
    villages, supply_counts = zip(*sorted_villages)

    # Create the x coordinates for the bars
    x = np.arange(len(villages))

    # Create the bar plot
    plt.figure(figsize=(10, 6))
    bars = plt.bar(x, supply_counts, tick_label=villages)

    plt.title("Village Supply Count")
    plt.xlabel("Village ID")
    plt.ylabel("Supply Count")
    plt.xticks(rotation='vertical')  # Rotate x-axis labels for readability

    # Add the supply count on top of each bar
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval, int(yval), va='bottom')  # va='bottom' to align the label at the top of the bar

    plt.grid(True)
    plt.tight_layout()  # To ensure the x-axis labels fit into the figure area
    plt.show()


    # Create and solve the problem with the deterministic method
    detsolver = Robust(centres, villages)
    detsolver.create_model()
    detsolver.solve_milp()

    # Get the solution
    detsol = detsolver.get_solution()

    # Print the solution
    detsol.print()

    

'''