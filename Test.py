import pulp
import numpy as np
import pandas as pd
from Matrix import Matrix

# Import custom modules
from JSInstance import JSInstance

villages = JSInstance("data_drones.xlsx", "Demand points")
centres = JSInstance("data_drones.xlsx", "Help centers")

matrix = Matrix(villages, centres); 


for row in matrix.get_matrix():
    print(row, "\n")
    print("\n")

print(len(matrix.get_matrix()))
print(len(matrix.get_matrix()[0]))