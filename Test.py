import pulp
import numpy as np
import pandas as pd
from Matrix import Matrix

# Import custom modules
from JSInstance import JSInstance

villages = JSInstance("data_drones.xlsx", "Demand points")
centres = JSInstance("data_drones.xlsx", "Help centers")

matrix = Matrix(villages, centres); 
print(matrix.get_matrix()); 
print(villages.get_df())
