import pulp
import numpy as np
import pandas as pd
from Matrix import Matrix
from Villages import Villages
from Centres import Centres
from DeterministicSolver2 import DeterministicSolver2

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

    # Print the nested dictionary of distances from each center to each village
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


    print(centres.get_distance_from_village(1,1))

    # Create and solve the problem with the deterministic method
    detsolver = DeterministicSolver2(centres, villages)
    detsolver.create_model()
    detsolver.solve_milp()

    # Get the solution
    solution = detsolver.get_solution()

    # Print the solution
    solution.print()

