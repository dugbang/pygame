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


class GraphicPoint:
    def __init__(self, x=0, y=0):
        self.mat = np.mat([[x], [y], [1]])

    # def get(self):
    #     return self.mat
    # @property
    # @mat.setter
    # def mat(self, m):

    def get_element(self):
        return self.mat.item(0), self.mat.item(1)


class GraphicCircle:
    def __init__(self, x=0, y=0, radius=10, width=0, color=None):
        self.mat = np.mat([[x], [y], [1]])
        self.r = radius
        self.width = width
        self.color = color

    def get_element(self):
        return self.mat.item(0), self.mat.item(1), self.r


def circle_operation(circle, mat_operation):
    circle_ = GraphicCircle(radius=circle.r, width=circle.width, color=circle.color)
    circle_.mat = mat_operation * circle.mat
    return circle_


class GraphicLine:
    """
    # line_types
    # 1; line(open), 2; line(close), 3; ploy
    """
    def __init__(self, line_type=0, width=0, color=None):
        self.line_type = line_type
        self.width = width
        self.color = color
        self.points = []


def line_operation(line, mat_operation):
    line_ = GraphicLine(line_type=line.line_type, width=line.width, color=line.color)
    point_ = GraphicPoint()
    for point in line.points:
        point_.mat = mat_operation * point.mat
        line_.points.append(point_)
    return line_


class RealObject:
    def __init__(self, x=0, y=0, direction=0):
        self.shape = {'lines': [], 'circles': [], }

        self.center_x = x
        self.center_y = y
        self.direction = direction

    def set_position(self, x=0, y=0, direction=0):
        self.center_x = x
        self.center_y = y
        self.direction = direction

    def reset_shape(self):
        self.shape = {'lines': [], 'circles': [], }

    def repositioning(self):
        mat_tr_zero = Matrix.translation(-self.center_x, -self.center_y)
        mat_ro = Matrix.rotation(self.direction)
        mat_tr_org = Matrix.translation(self.center_x, self.center_y)
        mat_operation = mat_tr_zero * mat_ro * mat_tr_org

        lines = []
        for line in self.shape['lines']:
            lines.append(line_operation(line, mat_operation))
        self.shape['lines'] = lines

        circles = []
        for circle in self.shape['circles']:
            circles.append(circle_operation(circle, mat_operation))

        self.shape['circles'] = circles


class MobileRobot(RealObject):
    def __init__(self):
        super().__init__()
        body = GraphicLine(line_type=2, width=0, color=0)
        body.points = [GraphicPoint(-150, -100),
                       GraphicPoint(-150, 100),
                       GraphicPoint(150, 100),
                       GraphicPoint(150, -100)]

        sensing = GraphicLine(line_type=2, width=0, color=0)
        sensing.points = [GraphicPoint(150, 50),
                          GraphicPoint(170, 50),
                          GraphicPoint(170, -50),
                          GraphicPoint(150, -50)]

        self.shape['lines'].append(body)
        self.shape['lines'].append(sensing)
        self.shape['circles'].append(GraphicCircle(x=0, y=0, radius=100, width=0, color=0))
        self.shape['circles'].append(GraphicCircle(x=0, y=0, radius=50, width=0, color=0))


class ViewCoordinate:
    def __init__(self, x=0, y=0, direction=0):
        self.zero_x = x
        self.zero_y = y
        self.direction = direction

        self.obj_list = []
        self.shape_list = []

    def set_position(self, x=0, y=0, direction=0):
        self.zero_x = x
        self.zero_y = y
        self.direction = direction

    def add_object(self, obj):
        self.obj_list.append(obj)
        self.shape_list.append({'lines': [], 'circles': [], })

    def get_total_area(self):
        min_x = min_y = max_x = max_y = 0
        points = self.__get_all_line_points()
        for i, point in enumerate(points):
            # print(point[0], point[1])
            if i == 0:
                min_x = max_x = point[0]
                min_y = max_y = point[1]
            else:
                min_x = min(min_x, point[0])
                max_x = max(max_x, point[0])

                min_y = min(min_y, point[1])
                max_y = max(max_y, point[1])

        # print(type(min_x))
        circles = self.__get_all_circle_points()
        for x, y, r in circles:
            # print(type(min_x), x, y, r)
            min_x = min(min_x, x - r)
            max_x = max(max_x, x + r)

            min_y = min(min_y, y - r)
            max_y = max(max_y, y + r)

        # print(min_x, min_y, max_x, max_y)
        return [[min_x, min_y], [min_x, max_y], [max_x, max_y], [max_x, min_y]]

    def __get_all_line_points(self):
        lines_ = list()
        for shape in self.shape_list:
            for line in shape['lines']:
                # rec = []
                for point in line.points:
                    # print(point.item(0), point.item(1))
                    lines_.append(point.get_element())
            # lines_.append(rec)
        return lines_

    def __get_all_circle_points(self):
        ret = list()
        for shape in self.shape_list:
            circles = shape['circles']
            for circle in circles:
                ret.append(circle.get_element())
        return ret

    def repositioning(self):
        for i in range(len(self.obj_list)):
            offset_x = self.obj_list[i].center_x - self.zero_x
            offset_y = self.obj_list[i].center_y - self.zero_y

            mat_axis_zero = Matrix.translation(-self.zero_x, -self.zero_y)
            mat_axis_ro = Matrix.rotation(self.direction)
            mat_axis_org = Matrix.translation(self.zero_x, self.zero_y)
            mat_axis_operation = mat_axis_zero * mat_axis_ro * mat_axis_org

            mat_tr = Matrix.translation(offset_x, offset_y)
            mat_operation = mat_axis_operation * mat_tr

            self.obj_list[i].repositioning()
            self.shape_list[i] = {'lines': [], 'circles': [], }

            # self.shape_list[i]['line_types'] = self.obj_list[i].shape['line_types']
            for line in self.obj_list[i].shape['lines']:
                self.shape_list[i]['lines'].append(line_operation(line, mat_operation))

            for circle in self.obj_list[i].shape['circles']:
                self.shape_list[i]['circles'].append(circle_operation(circle, mat_operation))


