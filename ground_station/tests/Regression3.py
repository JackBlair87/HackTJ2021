import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import math

def main():
    x_train = [[0],[1],[2],[3],[4],[5]]
    y_train = [[2],[3],[4],[5],[6],[7]]
    x_test = [[6], [7]]

    regressor = LinearRegression()
    regressor.fit(x_train, y_train)


    # print("intercept:", regressor.intercept_)

    print("coefficient:", regressor.coef_[0][0])
    print("intercept:", regressor.intercept_[0])

    y_pred = regressor.predict(x_test)
    print('y_pred:', y_pred)

    # print("shortest distance:", distance(7, 7, slope=regressor.coef_[0][0]))
    print("distance:", distance(x=4, y=4, slope=-1, b=-100))

def distance(x, y, slope=0, b=0):
    if slope == 0:
        return y - (slope * x + b)
    perp_slope = -1 / slope
    perp_b = (y - perp_slope * x)
    intersect_x = (b - perp_b) / (perp_slope - slope)
    intersect_y = intersect_x * slope + b
    distance = math.sqrt((intersect_y-y)**2 + (intersect_x-x)**2)
    return distance


main()