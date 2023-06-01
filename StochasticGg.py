import pulp
import cplex
import numpy as np
import pandas as pd
from tqdm import tqdm
import random

# Import custom modules
from JSInstance import JSInstance
from Solution import Solution

# Class for solving deterministic job-shop scheduling problems using MILP
class StochasticGg(object):
    def __init__(self, centers, villages):
        # Initialize MILP model and instance
        self._model = pulp.LpProblem("Drone attribution", pulp.LpMaximize)
        # Get list of centers
        self.center = centers
        # Get list of villages
        self.village = villages
        # Get list of drones
        self.drone = np.arange(1,16)
        # Cunsomption constat
        self._scena = np.arange(1,6)
        self._beta = {}
        for s in self._scena:
            for i in self.center.get_all_ids():
                for j in self.village.get_all_ids():
                    for s in self._scena:
                        beta = random.uniform(2.5,3)
                        self._beta[s,i,j] = beta

    # Method for creating the model
    def create_model(self):
        # Define decision variables, objective function, and constraints
        self.create_variables()
        self.create_objective()
        self.create_constraints()

    # Method for creating decision variables
    def create_variables(self):
        """
        Create the decision variables used in the model.
        """
        # Binary variables x_ijk to define if center i serve j village with k drone
        self._x = pulp.LpVariable.dicts('Drone', 
                                        ((s, i, j, k) for s in self._scena for i in self.center.get_all_ids() for j in self.village.get_all_ids() for k in self.drone),
                                        lowBound=0,cat=pulp.LpContinuous)
        # Binary variables y_i to define if i center is open
        self._y = pulp.LpVariable.dicts('Center opening',
                                  self.center.get_all_ids(),
                                  lowBound=0,cat=pulp.LpBinary)
        
        self._z = pulp.LpVariable.dicts('Center - Drone Allocation',
                                   ((i, k) for i in self.center.get_all_ids() for k in self.drone),
                                        lowBound=0,cat=pulp.LpBinary)
        
        # Binary variables x_ijk to define if center i serve j village with k drone
        self._t = pulp.LpVariable.dicts('Drone allocation', 
                                        ((s, i, j, k) for s in self._scena for i in self.center.get_all_ids() for j in self.village.get_all_ids() for k in self.drone),
                                        lowBound=0,cat=pulp.LpBinary)
        

    # Method for creating the objective function
    def create_objective(self):
        """
        Create the objective function of the model.
        """
        # Objective is to maximize village demande
        self._model += pulp.lpSum(self._x[s,i,j,k] for s in self._scena for i in self.center.get_all_ids() for j in self.village.get_all_ids() for k in self.drone) / np.max(self._scena)


    # Method for creating the constraints
    def create_constraints(self):
        """
        Create the model constraints.
        """
        #1. 700Wh max / drone
        for s in self._scena:
            for k in self.drone:
                self._model +=  1.1 * pulp.lpSum(self._beta[s,i,j] * self.center.get_distance_from_village(i,j) * 
                                                (self._x[s,i,j,k]  + 20*self._t[s,i,j,k]) 
                                                for i in self.center.get_all_ids() for j in self.village.get_all_ids()) <= 700


        #2. At most satisfy the demand
        for s in self._scena:
            for j in self.village.get_all_ids():
                self._model += pulp.lpSum(self._x[s,i,j,k] for i in self.center.get_all_ids() for k in self.drone) <= self.village.get_demand(j) #*bin_trajet8drone

        #3. 30kg max / center
        for s in self._scena:
            for i in self.center.get_all_ids():
                self._model += pulp.lpSum(self._x[s,i,j,k] for j in self.village.get_all_ids() for k in self.drone) <= 30


        #4. 5 opened center max
        self._model += pulp.lpSum(self._y[i] for i in self.center.get_all_ids()) <= 5

        #5. 1 drone est assigné à un unique centre
        for k in self.drone : 
            self._model += pulp.lpSum(self._z[i,k] for i in self.center.get_all_ids()) <= 1
  
        #6. If center not opened, no drone assigned
        for i in self.center.get_all_ids():
                for k in self.drone:
                    self._model += self._y[i] >= self._z[i,k]
        
        #7.If drone is not assigned to village from a center, demand associated is null
        for s in self._scena:
            for i in self.center.get_all_ids():
                for j in self.village.get_all_ids():
                    for k in self.drone:
                        self._model += self._x[s,i,j,k] <= self._t[s,i,j,k]*self.village.get_demand(j)

      

        #8. If drone not assigned to center, impossible to go to a village
        for s in self._scena:
            for i in self.center.get_all_ids():
                for j in self.village.get_all_ids():
                    for k in self.drone:
                        self._model += self._z[i,k] >= self._t[s,i,j,k]

        


    # Method for writing the MILP model to a file
    def write_milp(self):
        """
        Write the model to a file.
        """
        self._model.writeLP("JS_milp.lp")

    # Method for solving the MILP model
    def solve_milp(self):
        """
        Solve the model using the chosen solver.
        """
        # Solve using the default solver used by PuLP
        #self._model.solve()

        #Solving using GUROBI or CPLEX (choose one of the two depending on which one is available)
        #Use the command pulp.pulpTestAll() to check which solvers are available on your machine

        #self._model.solve(pulp.GUROBI_CMD(options=[("MIPgap", 0.03)]))
        #self._model.solve(pulp.GUROBI(msg=1, gapRel=0.001))

        #self._model.solve(pulp.CPLEX_CMD())
        self._model.solve(pulp.CPLEX_PY(msg=0, gapRel=0.02))


    def get_solution(self):
        """
        Create a solution object from the decision variables computed.
        """
        print("HERE")
        print(pulp.value(self._model.objective))
        print("HERE")
        sol = Solution(self.center, self.village)
        if self._model.status > 0:
            sol._max_demand = pulp.value(self._model.objective)
            sol._alloc = {key: var.varValue for key, var in self._x.items() if var.varValue > 0}
            sol._open = {key: var.varValue for key, var in self._y.items() if var.varValue > 0}
            sol._drone_center = {key: var.varValue for key, var in self._z.items() if var.varValue > 0}
            sol._supplied = {key: False for key in self.village.get_all_ids()}
            for i, j, k in sol._alloc:
                if sol._alloc[(i, j, k)]:
                    sol._supplied[j] = True
                    sol._drone_consumption[(i, j, k)] = 2 * 1.1 * self.beta * self.center.get_distance_from_village(i,j) * (self.village.get_demand(j) + 10) * sol._alloc[(i, j, k)]
        return sol
