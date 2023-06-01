import pulp
import cplex
import gurobipy
import numpy as np
import pandas as pd
from Matrix import Matrix
from Villages import Villages
from Centres import Centres
from Deterministic import Deterministic
from DeterministicG import DeterministicG
from Stochastic import Stochastic
from StochasticG import StochasticG
from Robust import Robust
from RobustG import RobustG
from StochasticGg import StochasticGg
import random
from tqdm import tqdm


if __name__ == "__main__":
    centres = Centres()

    # Create a Villages object
    villages = Villages()

    # Compute the distance between each center and village
    centres.create_village_distance_dict(villages)
    villages.create_center_distance_dict(centres)

    # Create and solve the problem with the deterministic method
    detsolver = RobustG(centres, villages, 0)
    detsolver.create_model()
    detsolver.solve_milp()

    # Get the solution
    detsol = detsolver.get_solution()

    # Print the solution
    detsol.print()

    '''# Create and solve the problem with the deterministic method
    detsolver = DeterministicG(centres, villages)
    detsolver.create_model()
    detsolver.solve_milp()

    # Get the solution
    detsol = detsolver.get_solution()

    # Print the solution
    detsol.print()'''



    """# Create and solve the problem with the stochastic method
    detsolver = StochasticG(centres, villages)
    detsolver.create_model()
    detsolver.solve_milp()

    # Get the solution
    detsol = detsolver.get_solution()

    # Print the solution
    detsol.print()"""

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