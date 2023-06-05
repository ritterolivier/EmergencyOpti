import pulp
import numpy as np
import pandas as pd
from tqdm import tqdm
from random import random

# Import custom modules
from JSInstance import JSInstance
from Solution import Solution

# Class for solving deterministic job-shop scheduling problems using MILP
class Robust(object):
    def __init__(self, centers, villages, gamma):
        # Initialize MILP model and instance
        self._model = pulp.LpProblem("Drone attribution", pulp.LpMaximize)
        # Get list of centers
        self.center = centers
        # Get list of villages
        self.village = villages
        # Get list of drones
        self.drone = np.arange(1,31)
        # Cunsomption constats
        self._beta = 2.75
        self._bChap = 0.25
        self._gamma = gamma

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
        # Continuous variable x_ijk to define the weight carried by drone k between center i and village j 
        self._x = pulp.LpVariable.dicts('Weight allocation', 
                                        ((i, j, k) for i in self.center.get_all_ids() for j in self.village.get_all_ids() for k in self.drone),
                                        lowBound=0,cat=pulp.LpInteger)
        
        # Binary variables x_ijk to define if center i serve j village with k drone
        self._t = pulp.LpVariable.dicts('Drone allocation', 
                                        ((i, j, k) for i in self.center.get_all_ids() for j in self.village.get_all_ids() for k in self.drone),
                                        lowBound=0,cat=pulp.LpBinary)
        
        # Binary variables y_i to define if i center is open
        self._y = pulp.LpVariable.dicts('Center opening',
                                  self.center.get_all_ids(),
                                  cat=pulp.LpBinary)
        
        # Binary variables z_ik to define drone to center allocation
        self._z = pulp.LpVariable.dicts('Center - Drone Allocation',
                                   ((i, k) for i in self.center.get_all_ids() for k in self.drone),
                                        cat=pulp.LpBinary)
        
        self._q = pulp.LpVariable.dicts("q", ((k) for k in self.drone), lowBound=0, cat=pulp.LpContinuous)

        self._r = pulp.LpVariable.dicts('Center - Village - Drones',
                                   ((i, j, k) for i in self.center.get_all_ids() for j in self.village.get_all_ids() for k in self.drone),
                                        lowBound=0,cat=pulp.LpContinuous)
        

    # Method for creating the objective function
    def create_objective(self):
        """
        Create the objective function of the model.
        """
        # Objective is to maximize village demande
        self._model += pulp.lpSum(self._x[i, j, k] for i in self.center.get_all_ids() for j in self.village.get_all_ids() for k in self.drone)


    # Method for creating the constraints
    def create_constraints(self):
        """
        Create the model constraints.
        """
        #1. 700Wh max / drone
        for k in self.drone:
            self._model +=  pulp.lpSum(self._beta * self.center.get_distance_from_village(i,j) * 
                                            (self._x[i,j,k]  + 20*self._t[i, j, k]) 
                                            for i in self.center.get_all_ids() for j in self.village.get_all_ids()) + self._gamma * self._q[k] + pulp.lpSum(
                                                self._r[i,j,k] for i in self.center.get_all_ids() for j in self.village.get_all_ids()
                                            ) <= 700


        #2. At most satisfy the demand
        for j in self.village.get_all_ids():
            self._model += pulp.lpSum(self._x[i,j,k] for i in self.center.get_all_ids() for k in self.drone) <= self.village.get_demand(j) #*bin_trajet8drone

        #3. 30kg max / center
        for i in self.center.get_all_ids():
            self._model += pulp.lpSum(self._x[i,j,k] for j in self.village.get_all_ids() for k in self.drone) <= 30


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
        for i in self.center.get_all_ids():
            for j in self.village.get_all_ids():
                for k in self.drone:
                    self._model += self._x[i,j,k] <= self._t[i,j,k]*self.village.get_demand(j)

      

        #8. If drone not assigned to center, impossible to go to a village
        for i in self.center.get_all_ids():
            for j in self.village.get_all_ids():
                for k in self.drone:
                    self._model += self._z[i,k] >= self._t[i,j,k]

        
        #9. ????
        for i in self.center.get_all_ids():
            for j in self.village.get_all_ids():
                for k in self.drone:
                    self._model += self._q[k] + self._r[i,j,k] >= (self._bChap * (
                        self._x[i,j,k] + 20 * self._t[i,j,k]) 
                        * self.center.get_distance_from_village(i,j))

        


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
        self._model.solve(pulp.CPLEX_PY(msg=1, gapRel=0.005))

    def get_solution(self):
        """
        Create a solution object from the decision variables computed.
        """
        sol = Solution('Robust',self.center, self.village)
        if self._model.status > 0:
            sol._of = pulp.value(self._model.objective)
            sol._alloc = {key: var.varValue for key, var in self._t.items() if var.varValue > 0}
            sol._demand = {key: var.varValue for key, var in self._x.items() if var.varValue > 0}
            sol._open = {key: var.varValue for key, var in self._y.items() if var.varValue > 0}
            sol._drone_center = {key: var.varValue for key, var in self._z.items() if var.varValue > 0}
            sol._gamma = self._gamma

        return sol