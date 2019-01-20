import math

import numpy as np
from unittest import TestCase

from coordinate import Matrix


class Coordinate:
    def __init__(self, x=0, y=0, direction=0):
        self.pos_x = x
        self.pos_y = y
        self.direction = direction

        self.shape = {'lines': [], 'circles': [], }

    def get_lines_lists(self):
        lines = []
        for line in self.shape['lines']:
            rec = []
            for point in line:
                rec.append([point.item(0), point.item(1)])
            lines.append(rec)
        return lines

    def get_circles_lists(self):
        circles = []
        for circle, r in self.shape['circles']:
            circles.append([circle.item(0), circle.item(1), r])
        return circles

    def get_area_of_shape(self):
        lines = self.get_lines_lists()
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

        circles = self.get_circles_lists()
        for x, y, r in circles:
            # print(point[0], point[1], point[2])
            min_x = min(min_x, x - r)
            max_x = max(max_x, x + r)

            min_y = min(min_y, y - r)
            max_y = max(max_y, y + r)

        # print(min_x, min_y, max_x, max_y)
        return [[min_x, min_y], [min_x, max_y], [max_x, max_y], [max_x, min_y]]


class GraphicObject:
    def __init__(self):
        self.shape = {'lines': [], 'circles': [], }

        self.world = Coordinate()
        self.view = Coordinate()
        self.window = Coordinate()  # 시스템 그래픽에서 화면기준이 어떻게 정의되는가?

    def set_pixel_coordinate(self, x=0, y=480, direction=0, scale_x=1, scale_y=1):
        self.window.pos_x = x
        self.window.pos_y = -y
        self.window.direction = direction

        self.window.shape = {'lines': [], 'circles': [], }
        self._shape_position_of_pixel(scale_x, scale_y, self.view)

    def _shape_position_of_pixel(self, scale_x, scale_y, source):
        mat_ro_x = Matrix.rotation_axis_x(math.pi)
        mat_sc = Matrix.scale(scale_x, scale_y)
        mat_ro = Matrix.rotation(self.window.direction)
        mat_tr = Matrix.translation(self.window.pos_x, self.window.pos_y)
        mat_operation = mat_ro_x * mat_sc * mat_ro * mat_tr
        # mat_operation = mat_sc * mat_ro * mat_tr
        for line in source.shape['lines']:
            rec = []
            for point in line:
                rec.append(mat_operation * np.mat([[point[0]], [point[1]], [1]]))
            self.window.shape['lines'].append(rec)
        for circle, r in source.shape['circles']:
            self.window.shape['circles'].append([(mat_operation * circle), r])

    def set_view_coordinate(self, x=0, y=0, direction=0):
        self.view.pos_x = x
        self.view.pos_y = y
        self.view.direction = direction

        self.view.shape = {'lines': [], 'circles': [], }
        self._shape_reposition_of_view(target=self.view)

    def _shape_reposition_of_view(self, target=None):
        # target_view = self.view
        offset_x = self.world.pos_x - target.pos_x
        offset_y = self.world.pos_y - target.pos_y
        offset_direction = self.world.direction - target.direction

        # print(offset_x, offset_y)

        mat_tr_zero = Matrix.translation(-self.world.pos_x, -self.world.pos_y)
        mat_ro = Matrix.rotation(offset_direction)
        mat_tr_org = Matrix.translation(self.world.pos_x, self.world.pos_y)

        mat_tr = Matrix.translation(offset_x, offset_y)
        mat_operation = mat_tr_zero * mat_ro * mat_tr_org * mat_tr

        for line in self.shape['lines']:
            rec = []
            for point in line:
                rec.append(mat_operation * np.mat([[point[0]], [point[1]], [1]]))
            target.shape['lines'].append(rec)
        for x, y, r in self.shape['circles']:
            target.shape['circles'].append([(mat_operation * np.mat([[x], [y], [1]])), r])

        # for line in self.world.shape['lines']:
        #     rec = []
        #     for point in line:
        #         rec.append(mat_operation * point)
        #     target.shape['lines'].append(rec)
        #
        # for circle, r in self.world.shape['circles']:
        #     target.shape['circles'].append([(mat_operation * circle), r])

    def set_world_coordinate(self, x=0, y=0, direction=0):
        self.world.pos_x = x
        self.world.pos_y = y
        self.world.direction = direction

        self.world.shape = {'lines': [], 'circles': [], }
        self.__shape_position_of_world()

    def __shape_position_of_world(self):
        mat_ro = Matrix.rotation(self.world.direction)
        mat_tr = Matrix.translation(self.world.pos_x, self.world.pos_y)
        mat_operation = mat_ro * mat_tr
        for line in self.shape['lines']:
            rec = []
            for point in line:
                rec.append(mat_operation * np.mat([[point[0]], [point[1]], [1]]))
            self.world.shape['lines'].append(rec)
        for x, y, r in self.shape['circles']:
            self.world.shape['circles'].append([(mat_operation * np.mat([[x], [y], [1]])), r])


class MobileRobot(GraphicObject):
    def __init__(self):
        super().__init__()
        self.shape['lines'].append(([-150, -100], [-150, 100], [150, 100], [150, -100], [-150, -100]))
        self.shape['lines'].append(([150, 50], [170, 50], [170, -50], [150, -50], [150, 50]))
        self.shape['circles'].append([0, 0, 100])
        self.shape['circles'].append([0, 0, 50])

        self.sensing_view = Coordinate()
        self.sensing_pixel = Coordinate()

    def set_sensing_view_coordinate(self, x=0, y=0, direction=0):
        """
        윈도좌표계를 사용하면 필요없을 듯...
        """
        self.sensing_view.pos_x = x
        self.sensing_view.pos_y = y
        self.sensing_view.direction = direction
        self.sensing_view.shape = {'lines': [], 'circles': [], }

        self._shape_reposition_of_view(target=self.sensing_view)

    def output(self):
        print(self.__class__.__name__)
        for line in self.world.shape['lines']:
            for point in line:
                print(point)
        for circle, r in self.view.shape['circles']:
            print(circle, r)


class MobileRobotTDD(MobileRobot):
    def __init__(self):
        super().__init__()
        self.shape = {'lines': [], 'circles': [], }

        self.__line1 = [[-100, -100], [-100, 100], [100, 100], [100, -100], [-100, -100]]
        self.__line2 = [[100, 50], [170, 50], [170, -50], [100, -50], [100, 50]]
        self.__circle1 = [0, 0, 100]
        self.__circle2 = [50, 0, 50]

        self.shape['lines'].append(self.__line1)
        self.shape['lines'].append(self.__line2)
        self.shape['circles'].append(self.__circle1)
        self.shape['circles'].append(self.__circle2)

    def get_circles_of_direction(self, direction):
        circles_ = []
        for x, y, r in self.shape['circles']:
            new_x = x * math.cos(direction) - y * math.sin(direction)
            new_y = y * math.cos(direction) + x * math.sin(direction)
            circles_.append([new_x, new_y, r])
        return circles_

    def get_circles_of_offset(self, offset_x, offset_y):
        circles_ = []
        for circle in self.shape['circles']:
            circles_.append([circle[0] + offset_x, circle[1] + offset_y, circle[2]])
        return circles_

    def get_lines_of_offset(self, offset_x, offset_y):
        lines_ = []
        for line in self.shape['lines']:
            rec = []
            for point in line:
                rec.append([point[0] + offset_x, point[1] + offset_y])
            lines_.append(rec)
        return lines_


class TestTransformation(TestCase):
    """
    TDD 순서
    1. 오브젝트를 정의한다.
    2. 월드좌표계에서 위치를 확인한다.
    3. 뷰좌표계에서 위치를 확인한다.
    4. 픽셀좌표계에서 위치를 확인한다.
    """
    def setUp(self):
        self.tdd_robot = MobileRobotTDD()

    def test_xy_move_world_01(self):
        offset_x = 10
        offset_y = 10
        self.tdd_robot.set_world_coordinate(x=offset_x, y=offset_y)

        manual_ = self.tdd_robot.get_circles_of_offset(offset_x, offset_y)
        matrix_ = self.tdd_robot.world.get_circles_lists()
        self.assertListEqual(matrix_[0], manual_[0])
        self.assertListEqual(matrix_[1], manual_[1])

        manual_ = self.tdd_robot.get_lines_of_offset(offset_x, offset_y)
        matrix_ = self.tdd_robot.world.get_lines_lists()
        self.assertListEqual(matrix_[0], manual_[0])
        self.assertListEqual(matrix_[1], manual_[1])

        offset_x_view = -200
        offset_y_view = -200
        self.tdd_robot.set_view_coordinate(x=offset_x_view, y=offset_y_view)

        manual_ = self.tdd_robot.get_circles_of_offset(offset_x-offset_x_view, offset_y-offset_y_view)
        matrix_ = self.tdd_robot.view.get_circles_lists()
        self.assertListEqual(matrix_[0], manual_[0])
        self.assertListEqual(matrix_[1], manual_[1])
        print(matrix_[0])
        print(matrix_[1])

        manual_ = self.tdd_robot.get_lines_of_offset(offset_x-offset_x_view, offset_y-offset_y_view)
        matrix_ = self.tdd_robot.view.get_lines_lists()
        self.assertListEqual(matrix_[0], manual_[0])
        self.assertListEqual(matrix_[1], manual_[1])

        self.tdd_robot.set_pixel_coordinate()
        matrix_ = self.tdd_robot.window.get_circles_lists()
        print(matrix_[0])
        print(matrix_[1])

    def test_xy_move_world_00(self):
        offset_x = 0
        offset_y = 0
        self.tdd_robot.set_world_coordinate(x=offset_x, y=offset_y)

        manual_ = self.tdd_robot.get_circles_of_offset(offset_x, offset_y)
        matrix_ = self.tdd_robot.world.get_circles_lists()
        self.assertListEqual(matrix_[0], manual_[0])
        self.assertListEqual(matrix_[1], manual_[1])

        manual_ = self.tdd_robot.get_lines_of_offset(offset_x, offset_y)
        matrix_ = self.tdd_robot.world.get_lines_lists()
        self.assertListEqual(matrix_[0], manual_[0])
        self.assertListEqual(matrix_[1], manual_[1])

        offset_x_view = -200
        offset_y_view = -200
        self.tdd_robot.set_view_coordinate(x=offset_x_view, y=offset_y_view)

        manual_ = self.tdd_robot.get_circles_of_offset(offset_x-offset_x_view, offset_y-offset_y_view)
        matrix_ = self.tdd_robot.view.get_circles_lists()
        self.assertListEqual(matrix_[0], manual_[0])
        self.assertListEqual(matrix_[1], manual_[1])
        # print(manual_[0])
        # print(manual_[1])

        manual_ = self.tdd_robot.get_lines_of_offset(offset_x-offset_x_view, offset_y-offset_y_view)
        matrix_ = self.tdd_robot.view.get_lines_lists()
        self.assertListEqual(matrix_[0], manual_[0])
        self.assertListEqual(matrix_[1], manual_[1])

        self.tdd_robot.set_pixel_coordinate()

    def test_graphic(self):
        graphic_object = MobileRobot()
        # view_area = ViewArea()

        # graphic_object.output()
        # view_area.output()

        graphic_object.set_world_coordinate()
        graphic_object.set_view_coordinate(x=-200, y=-200)
        graphic_object.output()
        # graphic_object.set_sensing_view_coordinate(100, 30)

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
        # rotation = 30
        radian = math.radians(180)
        rm = np.mat([[math.cos(radian), -math.sin(radian), 0],
                     [math.sin(radian), math.cos(radian), 0],
                     [0, 0, 1]])

