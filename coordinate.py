import math

import numpy as np


class Matrix:
    @staticmethod
    def translation(x, y):
        return np.mat([[1, 0, x],
                       [0, 1, y],
                       [0, 0, 1]])

    @staticmethod
    def scale(x, y):
        return np.mat([[x, 0, 0],
                       [0, y, 0],
                       [0, 0, 1]])

    @staticmethod
    def rotation(radian):
        return np.mat([[math.cos(radian), -math.sin(radian), 0],
                       [math.sin(radian), math.cos(radian), 0],
                       [0, 0, 1]])

    @staticmethod
    def rotation_axis_x(radian):
        return np.mat([[1, 0, 0],
                       [0, math.cos(radian), 0],
                       [0, 0, 1]])


