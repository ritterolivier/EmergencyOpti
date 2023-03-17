import pandas as pd
import JSInstance
import math


class Matrix:
    def __init__(self, villages : JSInstance, centres : JSInstance):
        self._rows = len(villages. index)
        self._cols = len(centres. index)
        self._matrix = [[0 for _ in range(len(villages. index))] for _ in range(len(centres. index))]
        
        self.fillMatrix(villages, centres)


    

    def __str__(self):
        matrix_str = ""
        for i in range(self.rows):
            for j in range(self.cols):
                matrix_str += str(self._matrix[i][j]) + " "
            matrix_str += "\n"
        return matrix_str

    def set_value(self, row, col, value):
        self._matrix[row][col] = value

    def get_value(self, row, col):
        return self._matrix[row][col]
    
    def get_matrix(self):
        return self._matrix
    

    def fillMatrix(self, villages : JSInstance, centres : JSInstance):
        df_ville = villages.get_df()
        df_centre = centres.get_df()

        i = 0
        for row in df_ville.iterrows():
            j = 0
            for row2 in df_centre.iterrow():
                value = math.sqrt(
                    math.pow(
                    (row["Latitude"] - row2["Latitude"]) , 2
                    )
                    +
                    math.pow(
                    (row["Longitude"] - row2["Longitude"]) , 2
                    )
                    )
                self.set_value(i, j, value)
                j+=1
            i+=1
