import pandas as pd
import JSInstance
import math


class Matrix:
    def __init__(self, villages : JSInstance, centres : JSInstance):
        df_ville = villages.get_df()
        df_centre = centres.get_df()

        df_ville = df_ville.astype({'Latitude': 'float', 'Longitude': 'float'})
        df_centre = df_centre.astype({'Latitude': 'float', 'Longitude': 'float'})

        self._rows = len(df_ville.index)
        self._cols = len(df_centre.index)

        self._matrix = [[0 for _ in range(self._cols)] for _ in range(self._rows)]

        for index, row in df_ville.iterrows():
            for index2, row2 in df_centre.iterrows():
                value = math.sqrt(
                    math.pow(
                    (row["Latitude"] - row2["Latitude"]) , 2
                    )
                    +
                    math.pow(
                    (row["Longitude"] - row2["Longitude"]) , 2
                    )
                    )
                print(value)
                self.set_value(index-1, index2-1, value)



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
    
