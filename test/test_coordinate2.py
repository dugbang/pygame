import math

import numpy as np
from unittest import TestCase

from coordinate import Matrix


def get_lines_lists(obj):
    lines = []
    for line in obj['lines']:
        rec = []
        for point in line:
            rec.append([point.item(0), point.item(1)])
        lines.append(rec)
    return lines


def get_circles_lists(obj):
    circles = []
    for circle, r in obj['circles']:
        circles.append([circle.item(0), circle.item(1), r])
    return circles


def get_area_of_shape(obj):
    lines = get_lines_lists(obj)
    min_x = min_y = max_x = max_y = i = 0
    for line in lines:
        for point in line:
            if i == 0:
                min_x = max_x = point[0]
                min_y = max_y = point[1]
                i = 1
            else:
                min_x = min(min_x, point[0])
                max_x = max(max_x, point[0])

                min_y = min(min_y, point[1])
                max_y = max(max_y, point[1])

    circles = get_circles_lists(obj)
    for x, y, r in circles:
        # print(point[0], point[1], point[2])
        min_x = min(min_x, x - r)
        max_x = max(max_x, x + r)

        min_y = min(min_y, y - r)
        max_y = max(max_y, y + r)

    # print(min_x, min_y, max_x, max_y)
    return [[min_x, min_y], [min_x, max_y], [max_x, max_y], [max_x, min_y]]


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
        points = self.__get_line_lists()
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
        circles = self.__get_circle_lists()
        for x, y, r in circles:
            # print(type(min_x), x, y, r)
            min_x = min(min_x, x - r)
            max_x = max(max_x, x + r)

            min_y = min(min_y, y - r)
            max_y = max(max_y, y + r)

        # print(min_x, min_y, max_x, max_y)
        return [[min_x, min_y], [min_x, max_y], [max_x, max_y], [max_x, min_y]]

    def __get_line_lists(self):
        lines_ = list()
        for shape in self.shape_list:
            for line in shape['lines']:
                # rec = []
                for point in line:
                    # print(point.item(0), point.item(1))
                    lines_.append([point.item(0), point.item(1)])
            # lines_.append(rec)
        return lines_

    def __get_circle_lists(self):
        ret = list()
        for shape in self.shape_list:
            circles = shape['circles']
            for circle, r in circles:
                ret.append([circle.item(0), circle.item(1), r])
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
            self.shape_list[i] = {'lines': [], 'circles': [], 'line_types': [], }

            self.shape_list[i]['line_types'] = self.obj_list[i].shape['line_types']
            for line in self.obj_list[i].shape['lines']:
                rec = []
                for point in line:
                    rec.append(mat_operation * point)
                    # rec.append(mat_operation * np.mat([[point[0]], [point[1]], [1]]))
                self.shape_list[i]['lines'].append(rec)

            try:
                for x, y, r in self.obj_list[i].shape['circles']:
                    self.shape_list[i]['circles'].append([(mat_operation * np.mat([[x], [y], [1]])), r])
            except:
                for circle, r in self.obj_list[i].shape['circles']:
                    self.shape_list[i]['circles'].append([mat_operation * circle, r])


class PixelCoordinate:
    """
    그림을 그리는 적절한 순서를 유지한다.
    pygame.Surface 와 같은 개념, 단 y축의 방향은 반대
    pygame.Surface 을 이용할 경우 (0, 0) 에서 시작할 수 있음.
    """
    def __init__(self, x=0, y=0, direction=0):
        self.pos_x = x
        self.pos_y = y
        self.direction = direction
        # scale 을 어떻게 결정할 것인가?
        self.view = None

    def set_position(self, x=0, y=0, direction=0):
        self.pos_x = x
        self.pos_y = y
        self.direction = direction

    def set_view(self, view):
        self.view = view


class Coordinate:
    robot = ViewCoordinate()
    # mini_map = SubCoordinate()
    # views = [rebot, mini_map]
    # view_of_world = [SubCoordinate(), SubCoordinate()]
    # pixel_of_system = [SubCoordinate(), SubCoordinate(), SubCoordinate()]
    win_main = PixelCoordinate()    # 큰 화면
    win_sub = PixelCoordinate()     # 미니맵용
    win_info = PixelCoordinate()    # 정보출력


class RealObject:
    def __init__(self, x=0, y=0, direction=0):
        # line_types
        # 1; line(open), 2; close(blank), 3; close(fill color)
        self.shape = {'lines': [], 'circles': [], 'line_types': [], }

        self.pos_x = x
        self.pos_y = y
        self.direction = direction

    def set_position(self, x=0, y=0, direction=0):
        self.pos_x = x
        self.pos_y = y
        self.direction = direction

    def repositioning(self):
        mat_tr_zero = Matrix.translation(-self.pos_x, -self.pos_y)
        mat_ro = Matrix.rotation(self.direction)
        mat_tr_org = Matrix.translation(self.pos_x, self.pos_y)
        mat_operation = mat_tr_zero * mat_ro * mat_tr_org

        lines = []
        for line in self.shape['lines']:
            rec = []
            try:
                for x, y in line:
                    rec.append(mat_operation * np.mat([[x], [y], [1]]))
            except:
                for point in line:
                    rec.append(mat_operation * point)
            lines.append(rec)
        self.shape['lines'] = lines

        circles = []
        try:
            for x, y, r in self.shape['circles']:
                circles.append([(mat_operation * np.mat([[x], [y], [1]])), r])
        except:
            for circle, r in self.shape['circles']:
                circles.append([mat_operation * circle, r])
        self.shape['circles'] = circles


class MobileRobot(RealObject):
    def __init__(self):
        super().__init__()
        self.shape['line_types'] = [2, 3]

        self.shape['lines'].append(([-150, -100], [-150, 100], [150, 100], [150, -100]))
        self.shape['lines'].append(([150, 50], [170, 50], [170, -50], [150, -50]))
        self.shape['circles'].append([0, 0, 100])
        self.shape['circles'].append([0, 0, 50])


class MobileRobotTDD(MobileRobot):
    def __init__(self):
        super().__init__()
        self.shape = {'lines': [], 'circles': [], 'line_types': [], }

        # self.shape['points'].append([[-100, -100], [-100, 100], [100, 100], [100, -100]])
        # self.shape['points'].append([[100, 50], [170, 50], [170, -50], [100, -50]])
        self.shape['line_types'] = [2, 3]

        self.shape['lines'].append([[-100, -100], [-100, 100], [100, 100], [100, -100]])
        self.shape['lines'].append([[100, 50], [170, 50], [170, -50], [100, -50]])
        self.shape['circles'].append([0, 0, 100])
        self.shape['circles'].append([0, 0, 100])

    def get_circles_of_direction(self, direction):
        circles_ = []
        for x, y, r in self.shape['circles']:
            new_x = x * math.cos(direction) - y * math.sin(direction)
            new_y = y * math.cos(direction) + x * math.sin(direction)
            circles_.append([new_x, new_y, r])
        return circles_

    def get_circles_of_offset(self, offset_x, offset_y):
        circles_ = []
        for circle, r in self.shape['circles']:
            circles_.append([circle.item(0) + offset_x, circle.item(1) + offset_y, r])

        return circles_

    def get_lines_of_offset(self, offset_x, offset_y):
        lines_ = []
        for points in self.shape['lines']:
            rec = []
            for point in points:
                rec.append([point[0] + offset_x, point[1] + offset_y])
            lines_.append(rec)
        return lines_


class TestCoordinateSystem(TestCase):
    def setUp(self):
        # pass
        self.coordinate = Coordinate()
        # 아래와 같이 선언하여 전체를 테스트할 경우 에러가 발생함....ㅠ
        # self.tdd_robot = MobileRobotTDD()
        # self.coordinate.robot.add_object(self.tdd_robot)
        self.coordinate.robot.add_object(MobileRobotTDD())
        self.tdd_robot = self.coordinate.robot.obj_list[0]

    def test_object(self):
        self.assertEqual(self.tdd_robot, self.coordinate.robot.obj_list[0])
        # self.tdd_robot.repositioning()
        # self.tdd_robot.set_position()
        self.tdd_robot.repositioning()
        # for points in self.tdd_robot.shape['points']:
        #     for point in points:
        #         print(point[0], point[1])
        #         print('')
        self.coordinate.robot.repositioning()
        self.coordinate.robot.repositioning()
        self.coordinate.robot.repositioning()
        # for shape in self.coordinate.robot.shape_list:
        #     for line in shape['lines']:
        #         for point in line:
        #             print(point[0], point[1])
        #             print('')

        print(self.coordinate.robot.get_total_area())

    def test_robot_view_robot_rotation(self):

        offset_x = self.tdd_robot.pos_x - 200
        offset_y = self.tdd_robot.pos_y - 200

        self.assertEqual(self.tdd_robot, self.coordinate.robot.obj_list[0])

        self.tdd_robot.set_position(direction=math.pi/2)
        self.coordinate.robot.set_position(x=offset_x, y=offset_y)
        self.coordinate.robot.repositioning()

        manual_ = self.tdd_robot.get_circles_of_offset(-offset_x, -offset_y)
        matrix_ = get_circles_lists(self.coordinate.robot.shape_list[0])
        # matrix_org = get_circles_lists(self.coordinate.robot.obj_list[0].shape)
        self.assertListEqual(matrix_, manual_)
        # self.assertListEqual(matrix_, matrix_org)
        # print(manual_)
        # print(matrix_)
        print(self.coordinate.robot.get_total_area())

    def test_robot_view_translation(self):

        offset_x = self.tdd_robot.pos_x - 200
        offset_y = self.tdd_robot.pos_y - 200

        self.coordinate.robot.set_position(x=offset_x, y=offset_y)
        self.coordinate.robot.repositioning()

        manual_ = self.tdd_robot.get_circles_of_offset(-offset_x, -offset_y)
        matrix_ = get_circles_lists(self.coordinate.robot.shape_list[0])
        # matrix_org = get_circles_lists(self.coordinate.robot.obj_list[0].shape)
        self.assertListEqual(matrix_, manual_)
        # print(matrix_)
        # self.assertListEqual(matrix_, matrix_org)
        # print(self.coordinate.robot.obj_list[0].shape['circles'])
        print(self.coordinate.robot.get_total_area())

