import math

import numpy as np
from unittest import TestCase


def get_matrix_translation(x, y):
    return np.mat([[1, 0, x],
                   [0, 1, y],
                   [0, 0, 1]])


def get_matrix_scale(x, y):
    return np.mat([[x, 0, 0],
                   [0, y, 0],
                   [0, 0, 1]])


def get_matrix_rotation(radian):
    return np.mat([[math.cos(radian), -math.sin(radian), 0],
                   [math.sin(radian), math.cos(radian), 0],
                   [0, 0, 1]])


class MobileRobotTmp:
    def __init__(self):
        self.__shape = {'lines': [], 'circles': [], }
        self.__shape['lines'].append(([-150, -100], [-150, 100], [150, 100], [150, -100], [-150, -100]))
        self.__shape['lines'].append(([150, 50], [170, 50], [170, -50], [150, -50], [150, 50]))
        self.__shape['circles'].append((0, 0, 100))
        self.__shape['circles'].append((0, 0, 50))

        self.__shape_of_world = {'lines': [], 'circles': [], }

        # self.mass = 10000  # 10kg, 나중에 동역학 부분을 처리할 때 진행

    def tdd_setting(self, shape):
        self.__shape = shape

    def set_world_position(self, x=0, y=0, rotation=0):
        self.__shape_of_world = {'lines': [], 'circles': []}
        mat_ro = get_matrix_rotation(rotation)
        mat_tr = get_matrix_translation(x, y)

        self.__set_lines_element_of_world(mat_ro, mat_tr)
        self.__set_circles_element_of_world(mat_ro, mat_tr)

    def __set_circles_element_of_world(self, mat_ro, mat_tr):
        rec = []
        for x, y, r in self.__shape['circles']:
            new_p = mat_ro * mat_tr * np.mat([[x], [y], [1]])
            rec.append([new_p, r])
        self.__shape_of_world['circles'].append(rec)

    def __set_lines_element_of_world(self, mat_ro, mat_tr):
        for line in self.__shape['lines']:
            rec = []
            for point in line:
                new_p = mat_ro * mat_tr * np.mat([[point[0]], [point[1]], [1]])
                rec.append(new_p)
            self.__shape_of_world['lines'].append(rec)

    @staticmethod
    def __get_lines_lists(lines_elements):
        lines = []
        for line in lines_elements:
            rec = []
            for point in line:
                rec.append([point.item(0), point.item(1)])
            lines.append(rec)
        return lines

    @staticmethod
    def __get_circles_lists(circles_elements):
        circles = []
        for circle in circles_elements:
            for point, r in circle:
                circles.append([point.item(0), point.item(1), r])
        return circles

    def get_lines_of_world_coordinate(self):
        return self.__get_lines_lists(self.__shape_of_world['lines'])

    def get_circles_of_world_coordinate(self):
        return self.__get_circles_lists(self.__shape_of_world['circles'])

    def get_area_of_world(self):
        lines = self.get_lines_of_world_coordinate()
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

        circles = self.get_circles_of_world_coordinate()
        for x, y, r in circles:
            # print(point[0], point[1], point[2])
            min_x = min(min_x, x - r)
            max_x = max(max_x, x + r)

            min_y = min(min_y, y - r)
            max_y = max(max_y, y + r)

        # print(min_x, min_y, max_x, max_y)
        return [[min_x, min_y], [min_x, max_y], [max_x, max_y], [max_x, min_y]]

    def output(self):
        for p in self.__get_lines_lists(self.__shape_of_world['lines']):
            print(p)

        for p in self.__get_circles_lists(self.__shape_of_world['circles']):
            print(p)


class GraphicObject:
    shape = {'lines': [], 'circles': [], }


class MobileRobot(GraphicObject):
    def __init__(self):
        self.shape['lines'].append(([-150, -100], [-150, 100], [150, 100], [150, -100], [-150, -100]))
        self.shape['lines'].append(([150, 50], [170, 50], [170, -50], [150, -50], [150, 50]))
        self.shape['circles'].append((0, 0, 100))
        self.shape['circles'].append((0, 0, 50))


class TestTransformation(TestCase):
    """
    기본적인 동작순서는 다음과 같을 것으로 판단됨.
    1. 전체크기와 화면크기에 비례해서 배율을 조건
        - 실제 치수에 대한 값 적용
    2. 기준점 변경
        - pixel
    3. 회전
    """
    """
    TDD 순서
    1. 오브젝트를 정의한다.
    2. 월드좌표계에서 위치를 확인한다.
    3. 뷰좌표계에서 위치를 확인한다.
    4. 픽셀좌료계에서 위치를 확인한다.
    """
    def setUp(self):
        self.graphic_object = MobileRobot()
        # self.view_area = [[-100, -100], [400, -100], [400, 400], [-100, 400], [-100, -100]]
        self.robot = MobileRobotTmp()

        self.__line1 = [[-100, -100], [-100, 100], [100, 100], [100, -100], [-100, -100]]
        self.__line2 = [[100, 50], [170, 50], [170, -50], [100, -50], [100, 50]]
        self.__circle1 = [0, 0, 100]
        self.__circle2 = [0, 50, 50]

        # self.__line1 =
        self.__element = {'lines': [], 'circles': []}
        self.__element['lines'].append(self.__line1)
        self.__element['lines'].append(self.__line2)
        self.__element['circles'].append(self.__circle1)
        self.__element['circles'].append(self.__circle2)
        self.robot.tdd_setting(self.__element)

        # self.robot.set_world_position(rotation=math.pi/2)

    def test_robot_area(self):
        self.robot.set_world_position()
        area = self.robot.get_area_of_world()
        # print(area)
        self.assertListEqual(area, [[-100, -100], [-100, 100], [170, 100], [170, -100]])

    def test_robot_world_position_xy(self):

        offset_x = 100
        offset_y = 100
        self.robot.set_world_position(x=offset_x, y=offset_y)

        lines_ = self.__get_lines_of_offset(offset_x, offset_y)
        lines = self.robot.get_lines_of_world_coordinate()
        self.assertListEqual(lines[0], lines_[0])
        self.assertListEqual(lines[1], lines_[1])

        circles_ = self.__get_circles_of_offset(offset_x, offset_y)
        circles = self.robot.get_circles_of_world_coordinate()
        self.assertListEqual(circles[0], circles_[0])
        self.assertListEqual(circles[1], circles_[1])

        offset_x = -10
        offset_y = -50
        self.robot.set_world_position(x=offset_x, y=offset_y)

        lines_ = self.__get_lines_of_offset(offset_x, offset_y)
        lines = self.robot.get_lines_of_world_coordinate()
        self.assertListEqual(lines[0], lines_[0])
        self.assertListEqual(lines[1], lines_[1])

        circles_ = self.__get_circles_of_offset(offset_x, offset_y)
        circles = self.robot.get_circles_of_world_coordinate()
        self.assertListEqual(circles[0], circles_[0])
        self.assertListEqual(circles[1], circles_[1])

    def __get_circles_of_offset(self, offset_x, offset_y):
        circles_ = []
        for circle in self.__element['circles']:
            circles_.append([circle[0] + offset_x, circle[1] + offset_y, circle[2]])
        return circles_

    def __get_lines_of_offset(self, offset_x, offset_y):
        lines_ = []
        for line in self.__element['lines']:
            rec = []
            for point in line:
                rec.append([point[0] + offset_x, point[1] + offset_y])
            lines_.append(rec)
        return lines_

    def test_robot_world_position(self):
        self.robot.set_world_position()
        lines = self.robot.get_lines_of_world_coordinate()
        self.assertListEqual(lines[0], self.__line1)
        self.assertListEqual(lines[1], self.__line2)

        circles = self.robot.get_circles_of_world_coordinate()
        self.assertListEqual(circles[0], self.__circle1)
        self.assertListEqual(circles[1], self.__circle2)

        # lines = self.robot.get_lines_of_world_coordinate()
        # for i, line in enumerate(lines):
        #     self.assertListEqual(line, self.__element['lines'][i])
        #
        # circles = self.robot.get_circles_of_world_coordinate()
        # for i, circle in enumerate(circles):
        #     self.assertListEqual(circle, self.__element['circles'][i])
        #     # self.assertEqual(circle, self.__element['circles'][i])

    def test_Translation(self):
        org_x = 3
        org_y = 3
        om = np.mat([[org_x], [org_y], [1]])
        # tx = 1
        # ty = 2
        trans = [1, 2]  # pixel
        tm = np.mat([[1, 0, trans[0]],
                     [0, 1, trans[1]],
                     [0, 0, 1]])
        new_xy = tm * om
        # print(new_xy[0][0])
        self.assertEqual(new_xy[0], [[4]])
        self.assertEqual(new_xy[1], [[5]])
        # self.assertEqual(new_xy[0], [[2]])
        # self.assertEqual(new_xy[0][0], np.mat([[2], [1], [1]]))
        # self.assert

    def test_Scaling(self):
        org_x = 3
        org_y = 3
        om = np.mat([[org_x], [org_y], [1]])

        scale = [2, 2]
        sm = np.mat([[scale[0], 0, 0],
                     [0, scale[1], 0],
                     [0, 0, 1]])

        new_xy = sm * om
        # print(new_xy)
        self.assertEqual(new_xy[0], [[6]])
        self.assertEqual(new_xy[1], [[6]])

    def test_Rotation_screen(self):
        org_x = 3
        org_y = 3
        om = np.mat([[org_x], [org_y], [1]])

        rm = np.mat([[1, 0, 0],
                     [0, -1, 0],
                     [0, 0, 1]])
        new_xy = rm * om
        # print(new_xy)
        self.assertEqual(new_xy[0], [[3]])
        self.assertEqual(new_xy[1], [[-3]])

    def test_Rotation_point(self):
        """
        라인 트레이서의 라인센싱 부분에 적용할 수 있음.
        :return:
        """

        # rotation = 30
        radian = math.radians(180)
        rm = np.mat([[math.cos(radian), -math.sin(radian), 0],
                     [math.sin(radian), math.cos(radian), 0],
                     [0, 0, 1]])
