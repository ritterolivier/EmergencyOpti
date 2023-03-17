import numpy as np
from JSInstance import JSInstance
from DeterministicSolver import DeterministicSolver
#from StochasticSolver import StochasticSolver
#from RobustSolver import RobustSolver

if __name__ == '__main__':
    print("------------ Welcome to the job-shop solver ----------------")

    # Step 1: Create an instance from the datafile
    filename = "/Users/d0li/Nextcloud/IMT/Semestre 4/Optimisation dans l'incertain/dataJS.xlsx"
    instance = JSInstance(filename)
    # If necessary, print the information stored in the instance
    instance.print()

    # Step 2: Create a deterministic mathematical program from the instance
    detsolver = DeterministicSolver(instance)
    # 2.1: Define the model
    detsolver.create_model()
    # 2.2: Solve the instance
    detsolver.solve_milp()

    # Step 3: Create a stochastic mathematical program from the instance
    #stochsolver = StochasticSolver(...)
    # 3.1: Define the model
    #stochsolver.create_model()
    # 3.2: Solve the instance
    #stochsolver.solve_milp()

    # Step 4: Create a robust mathematical program from the instance
    #robsolver = RobustSolver(...)
    # 4.1: Define the model
    #robsolver.create_model()
    # 4.2: Solve the instance
    #robsolver.solve_milp()

    # Step 5: Retrieve the solutions obtained in each case
    detsolution = detsolver.get_solution()
    print("========== Deterministic solution ==========")
    detsolution.print()
    #stochsolution = stochsolver.get_solution()
    #print("========== Stochastic solution ==========")
    #stochsolution.print()
    #robsolution = robsolver.get_solution()
    #print("========== Robust solution ==========")
    #robsolution.print()

    # Step 4: Test it against a large set of (simulated) scenarios
    nbscenarios = 10000
    # Create scenarios with random processing times (uniform within 15% of the nominal value)
    ptscenarios = np.ndarray(shape=(nbscenarios, instance._processtimes.index.size, instance._processtimes.columns.size)) 
    for s in range(nbscenarios):
        ptscenarios[s] = np.multiply(instance._processtimes, (0.85 + 0.3 * np.random.random(size=instance._processtimes.shape)))

    print("========== Test of the different models ==========")
    detsolution.test(ptscenarios, "Deterministic")
    #stochsolution.test(ptscenarios, ...)
    #robsolution.test(ptscenarios, ...)


#First, it imports the necessary packages and classes.
#Then, it defines a main() function that will execute the entire script.
#Inside the main() function, it prints a welcome message to the console.
#It creates an instance of the job-shop problem from an Excel file, which contains the data for the problem.
#It creates a deterministic mathematical program from the instance and solves it using a MILP solver.
#It creates stochastic and robust mathematical programs, but these are commented out and not