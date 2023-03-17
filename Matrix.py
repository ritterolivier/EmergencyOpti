import pandas as pd
import JSInstance

class Matrix:
    def __init__(self, villages : JSInstance, centres : JSInstance):
        self.rows = len(villages. index)
        self.cols = len(centres. index)
        self.matrix = [[0 for _ in range(len(villages. index))] for _ in range(len(centres. index))]

    

    def __str__(self):
        matrix_str = ""
        for i in range(self.rows):
            for j in range(self.cols):
                matrix_str += str(self.matrix[i][j]) + " "
            matrix_str += "\n"
        return matrix_str

    def set_value(self, row, col, value):
        self.matrix[row][col] = value

    def get_value(self, row, col):
        return self.matrix[row][col]
    

    def fillMatrix(self, villages : JSInstance, centres : JSInstance):
        
        pass
