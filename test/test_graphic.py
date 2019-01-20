from unittest import TestCase

import numpy as np

from coordinate import Matrix


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
    def __init__(self, x=0, y=0, radius=10, fill=False, color=None):
        self.mat = np.mat([[x], [y], [1]])
        self.r = radius
        self.fill = fill
        self.color = color

    def get_element(self):
        return self.mat.item(0), self.mat.item(1), self.r


class GraphicLine:
    """
    # line_types
    # 1; line(open), 2; close(blank), 3; close(fill color)
    """
    def __init__(self, line_type=0, fill=False, color=None):
        self.line_type = line_type
        self.fill = fill
        self.color = color
        self.points = []


def circle_operation(circle, mat_operation):
    circle_ = GraphicCircle()
    circle_.color = circle.color
    circle_.fill = circle.fill
    circle_.r = circle.r
    circle_.mat = mat_operation * circle.mat
    return circle_


def line_operation(line, mat_operation):
    line_ = GraphicLine()
    line_.line_type = line.line_type
    line_.color = line.color
    line_.fill = line.fill
    tmp_point = GraphicPoint()
    for point in line.points:
        tmp_point.mat = mat_operation * point.mat
        line_.points.append(tmp_point)
    return line_


class RealObject:
    def __init__(self, x=0, y=0, direction=0):
        self.shape = {'lines': [], 'circles': [], }

        self.pos_x = x
        self.pos_y = y
        self.direction = direction

    def set_position(self, x=0, y=0, direction=0):
        self.pos_x = x
        self.pos_y = y
        self.direction = direction

    def reset_shape(self):
        self.shape = {'lines': [], 'circles': [], }

    def repositioning(self):
        mat_tr_zero = Matrix.translation(-self.pos_x, -self.pos_y)
        mat_ro = Matrix.rotation(self.direction)
        mat_tr_org = Matrix.translation(self.pos_x, self.pos_y)
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
        body = GraphicLine(line_type=2, color=0, fill=False)
        body.points = [GraphicPoint(-150, -100),
                       GraphicPoint(-150, 100),
                       GraphicPoint(150, 100),
                       GraphicPoint(150, -100)]

        sensing = GraphicLine(line_type=3, color=0, fill=True)
        sensing.points = [GraphicPoint(150, 50),
                          GraphicPoint(170, 50),
                          GraphicPoint(170, -50),
                          GraphicPoint(150, -50)]

        self.shape['lines'].append(body)
        self.shape['lines'].append(sensing)
        self.shape['circles'].append(GraphicCircle(x=0, y=0, radius=100, color=0, fill=False))
        self.shape['circles'].append(GraphicCircle(x=0, y=0, radius=50, color=0, fill=True))


class ViewCoordinate:
    def __init__(self, x=0, y=0, direction=0):
        self.pos_x = x
        self.pos_y = y
        self.direction = direction

        self.obj_list = []
        self.shape_list = []

    def set_position(self, x=0, y=0, direction=0):
        self.pos_x = x
        self.pos_y = y
        self.direction = direction

    def add_object(self, obj):
        self.obj_list.append(obj)
        self.shape_list.append({'lines': [], 'circles': [], 'line_types': [], })

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
            offset_x = self.obj_list[i].pos_x - self.pos_x
            offset_y = self.obj_list[i].pos_y - self.pos_y

            mat_axis_zero = Matrix.translation(-self.pos_x, -self.pos_y)
            mat_axis_ro = Matrix.rotation(self.direction)
            mat_axis_org = Matrix.translation(self.pos_x, self.pos_y)
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


class MobileRobotTDD(MobileRobot):
    def __init__(self):
        super().__init__()
        self.reset_shape()

        body = GraphicLine(line_type=2, color=0, fill=False)
        body.points = [GraphicPoint(-150, -100),
                       GraphicPoint(-150, 100),
                       GraphicPoint(150, 100),
                       GraphicPoint(150, -100)]

        sensing = GraphicLine(line_type=3, color=0, fill=True)
        sensing.points = [GraphicPoint(150, 50),
                          GraphicPoint(170, 50),
                          GraphicPoint(170, -50),
                          GraphicPoint(150, -50)]

        self.shape['lines'].append(body)
        self.shape['lines'].append(sensing)
        self.shape['circles'].append(GraphicCircle(x=0, y=0, radius=100, color=0, fill=False))
        self.shape['circles'].append(GraphicCircle(x=50, y=0, radius=50, color=0, fill=True))


class TestGraphic(TestCase):
    def setUp(self):

        self.robot_view = ViewCoordinate()
        self.robot_view.add_object(MobileRobotTDD())

        self.robot = self.robot_view.obj_list[0]

    def test_object(self):
        self.assertEqual(self.robot, self.robot_view.obj_list[0])

    def test_robot_view_repositioning(self):

        self.robot_view.repositioning()
        self.assertListEqual([[-100.0, -100.0], [-100.0, 100.0], [150.0, 100.0], [150.0, -100.0]],
                             self.robot_view.get_total_area())

    def test_robot_repositioning(self):
        self.robot.repositioning()

