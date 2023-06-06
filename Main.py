import numpy as np
import pandas as pd
from Charts import Charts
from Villages import Villages
from Centres import Centres
from Deterministic import Deterministic
from Robust import Robust
from Stochastic import Stochastic
from Simulation import Simulation
from tqdm import tqdm
from random import random
import time


if __name__ == "__main__":
    centres = Centres()

    # Create a Villages object
    villages = Villages()

    # Compute the distance between each center and village
    centres.create_village_distance_dict(villages)
    villages.create_center_distance_dict(centres)

    # Create and solve the problem with the deterministic method
    for beta in (2.3, 2.75, 3):
        detSolver = Deterministic(centres, villages, beta)
        detSolver.create_model()

        start_time = time.time()
        detSolver.solve_milp()
        end_time = time.time()
        time_taken = end_time - start_time

        # Get the solution
        detSol = detSolver.get_solution()

        # Create the charts
        charts = Charts(detSol, centres, villages, time_taken)
        charts.plot_solution()
        charts.plot_dronesCenters()
        
    # Create and solve the problem with the robust method
    for gamma in (0, 0.1, 0.2, 0.3, 0.4, 0.6, 0.8, 1):
        robSolver = Robust(centres, villages, gamma)
        robSolver.create_model()

        start_time = time.time()
        robSolver.solve_milp()
        end_time = time.time()
        time_taken = end_time - start_time

        # Get the solution
        robSol = robSolver.get_solution()

        # Create the charts
        charts = Charts(robSol, centres, villages,time_taken)
        charts.plot_solution()
        charts.plot_dronesCenters()

    # Create and solve the problem with the stochastic method
    stochSolver = Stochastic(centres, villages, 16)
    stochSolver.create_model()

    start_time = time.time()
    stochSolver.solve_milp()
    end_time = time.time()
    time_taken = end_time - start_time

    # Get the solution
    stochSol = stochSolver.get_solution()

    # Create the charts
    charts = Charts(stochSol, centres, villages, time_taken)
    charts.plot_solution()
    charts.plot_dronesCenters()

