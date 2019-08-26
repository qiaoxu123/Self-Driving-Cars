# Utility classes and functions for Coursera SDC Course 2.
#
# Author: Trevor Ablett
# University of Toronto Institute for Aerospace Studies

import numpy as np

class StampedData():
    def __init__(self):
        self.data = []
        self.t = []

    def convert_lists_to_numpy(self):
        self.data = np.array(self.data)
        self.t = np.array(self.t)