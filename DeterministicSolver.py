import pulp
import numpy as np
import pandas as pd

from JSInstance import JSInstance
from Solution import Solution


class DeterministicSolver(object):
    def __init__(self, instance):
        self._model = pulp.LpProblem("Job-shop scheduling",
                                     pulp.LpMinimize)
        self._instance = instance
        self._jobs = instance._processtimes.index
        self._machines = np.array(instance._processtimes.columns, dtype=int)

    def create_model(self):
        self.create_variables()
        self.create_objective()
        self.create_constraints()

    def create_variables(self):
        """
        Create the decision variables used in the model.
        """
        # Binary variables x_ij to define the allocation of jobs to machines
        self._x = pulp.LpVariable.dicts('allocation', (self._jobs, self._machines),
                                        cat=pulp.LpBinary)
        # Continuous variable cmax that represents the makespan
        self._cmax = pulp.LpVariable('makespan', lowBound=0, upBound=None, cat=pulp.LpContinuous)

        # Remark: It is also possible to create continuous or integer variables and add lower and upper bounds
        # self._contx = pulp.LpVariable.dicts(..., lowBound=0, upBound=None, cat=LpContinuous)
        # self._intx = pulp.LpVariable.dicts(..., lowBound=0, upBound=10, cat=LpInteger)

    def create_objective(self):
        """
        Create the objective function of the model.
        """
        self._model += self._cmax 

    def create_constraints(self):
        """
        Create the model constraints.
        """
        # Each job must be allocated to one machine
        for i in self._jobs:
            self._model += pulp.lpSum(self._x[i][j] for j in self._machines) == 1

        # The finishing time of each machine is a lower boun on Cmax
        for j in self._machines:
            self._model += pulp.lpSum(self._instance._processtimes.loc[i, j] * self._x[i][j] for i in self._jobs) <= self._cmax

    def write_milp(self):
        """
        Write the model to a file.
        """
        self._model.writeLP("JS_milp.lp")

    def solve_milp(self):
        """
        Solve the model using the chosen solver.
        """
        #IMPORTANT: If the problem is too complex to be solved optimaly, we can use the parameter 'gapRel' that allows to obtain a solution at least as good as gapRel*100% of the optimal one
        #Solving with the default solver used by PuLP
        self._model.solve()

        #Solving using GUROBI or CPLEX (choose one of the two depending on which one is available)
        #Use the command pulp.pulpTestAll() to check which solvers are available on your machine

        #self._model.solve(pulp.GUROBI_CMD(options=[("MIPgap", 0.03)]))
        #self._model.solve(pulp.GUROBI(msg=1, gapRel=0.001))

        #self._model.solve(pulp.CPLEX_CMD())
        #self._model.solve(pulp.CPLEX_PY(msg=0, gapRel=0.005))

    def get_solution(self):
        """
        Create a solution object from the decision variables computed.
        """
        sol = Solution(instance=self._instance)
        if self._model.status > 0:
            sol._makespan = pulp.value(self._model.objective)
            sol._alloc = pd.DataFrame(0, index=self._jobs, columns=self._machines)
            for i in self._jobs:
                for j in self._machines:
                    if self._x[i][j].varValue == 1:
                        sol._alloc.loc[i,j] = 1

        return sol 

