import numpy as np
import pandas as pd


class JSInstance():

    # Constructor
    def __init__(self, datafile="", sheet_name=""):
        """
        Collect the informations from the input file to build the job-shop scheduling instance.
        """
        #Check that the file is an excel spreadsheet
        if datafile[-5:] == ".xlsx":
            #Get the informations on the processing times of each job
            self._processtimes = pd.read_excel(datafile, sheet_name, index_col=0)
        else:
            raise NameError("Expected a '.xlsx' file")

    def print(self):
        """Print the main information about the instance."""
        if self._processtimes.empty:
            print("Empty instance: Use a data file to fill the parameters")
        else:
            print("Number of the village: {}".format(self._processtimes.index.size))
            print("Number of machines: {}".format(self._processtimes.columns.size))
            # Add some (local) options to display the dataframe
            with pd.option_context('display.max_rows', None,
                       'display.max_columns', None,
                       'display.precision', 3):
                print(self._processtimes)


        
