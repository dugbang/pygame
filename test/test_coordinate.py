import math

import numpy as np
from unittest import TestCase


class TestTransformation(TestCase):
    """
    기본적인 동작순서는 다음과 같을 것으로 판단됨.
    1. 전체크기와 화면크기에 비례해서 배율을 조건
        - 실제 치수에 대한 값 적용
    2. 기준점 변경
        - pixel
    3. 회전
    """
    def setUp(self):
        pass

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
