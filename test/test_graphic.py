import math
from unittest import TestCase

from coordinate import GraphicPoint, GraphicCircle, GraphicLine, MobileRobot, ViewCoordinate


class PixelCoordinate:
    """
    pygame.Surface 와 같은 개념, 단 y축의 방향은 반대
    pygame.Surface 을 이용할 경우 (0, 0) 에서 시작할 수 있음. set position 등은 구현하지 않음.
    GUI 부분에서 구현해야 할 클래스로 판단
    """
    def __init__(self, width=100, height=100):
        self.width = width
        self.height = height
        # self.direction = direction
        # scale 을 어떻게 결정할 것인가? > 내부적으로 계산하거나 플래그 적용...
        self.view = None
        self.relation = None

    def set_view_coordinate(self, view, relation=None):
        self.view = view
        self.relation = relation

    def draw(self):
        pass


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
            elem = circle.get_element()
            circles_.append([elem[0] + offset_x, elem[1] + offset_y, elem[2]])

        return circles_

    @staticmethod
    def get_circles_from_obj(obj):
        circles_ = []
        for circle in obj['circles']:
            elem = circle.get_element()
            circles_.append([elem[0], elem[1], elem[2]])

        return circles_


class TestGraphic(TestCase):
    def setUp(self):

        self.robot_view = ViewCoordinate()
        self.robot_view.add_object(MobileRobotTDD())

        self.robot = self.robot_view.obj_list[0]

    def test_robot_view_robot_rotation(self):
        self.assertEqual(self.robot, self.robot_view.obj_list[0])

        offset_x = self.robot.center_x - 200
        offset_y = self.robot.center_y - 200

        self.robot.set_position(direction=math.pi/2)

        self.robot_view.set_position(x=offset_x, y=offset_y)
        self.robot_view.repositioning()

        manual_ = self.robot.get_circles_of_offset(-offset_x, -offset_y)
        matrix_ = self.robot.get_circles_from_obj(self.robot_view.shape_list[0])

        self.assertListEqual(matrix_, manual_)
        self.assertListEqual([[100.0, 100.0], [100.0, 350.0], [300.0, 350.0], [300.0, 100.0]],
                             self.robot_view.get_total_area())

    def test_robot_view_translation(self):

        offset_x = self.robot.center_x - 200
        offset_y = self.robot.center_y - 200

        self.robot_view.set_position(x=offset_x, y=offset_y)
        self.robot_view.repositioning()

        manual_ = self.robot.get_circles_of_offset(-offset_x, -offset_y)
        matrix_ = self.robot.get_circles_from_obj(self.robot_view.shape_list[0])

        self.assertListEqual(matrix_, manual_)
        self.assertListEqual([[100.0, 100.0], [100.0, 300.0], [350.0, 300.0], [350.0, 100.0]],
                             self.robot_view.get_total_area())

    def test_object(self):
        self.assertEqual(self.robot, self.robot_view.obj_list[0])

    def test_robot_view_repositioning(self):

        self.robot_view.repositioning()
        self.assertListEqual([[-100.0, -100.0], [-100.0, 100.0], [150.0, 100.0], [150.0, -100.0]],
                             self.robot_view.get_total_area())

    def test_robot_repositioning(self):
        self.robot.repositioning()


