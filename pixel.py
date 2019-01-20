import pygame

from constant import BLACK, WHITE, BLUE, GREEN, RED
from coordinate import GraphicCircle, GraphicLine, GraphicPoint


class PixelWindow:
    def __init__(self, x=0, y=0, width=100, height=100, screen_=None):
        self.left = x
        self.top = y
        self.width = width
        self.height = height

        self.win = pygame.Surface((width, height))
        self.screen = screen_

        self.view = None
        self.view_offset_x = 0
        self.view_offset_y = height
        self.relation = None
        self.__shape = {'lines': [], 'circles': [], }

    def __reset_shape(self):
        self.__shape = {'lines': [], 'circles': [], }

    def __test_tmp(self):
        self.__reset_shape()

        # test code...
        self.__shape['circles'].append(GraphicCircle(x=100, y=100, radius=100, width=0, color=RED))
        self.__shape['circles'].append(GraphicCircle(x=150, y=100, radius=50, width=0, color=BLUE))
        body = GraphicLine(line_type=2, width=1, color=WHITE)
        body.points = [GraphicPoint(-150, -100),
                       GraphicPoint(-150, 100),
                       GraphicPoint(150, 100),
                       GraphicPoint(150, -100)]
        sensing = GraphicLine(line_type=3, width=0, color=WHITE)
        sensing.points = [GraphicPoint(150, 50),
                          GraphicPoint(170, 50),
                          GraphicPoint(170, -50),
                          GraphicPoint(150, -50)]
        temp = GraphicLine(line_type=1, width=2, color=BLACK)
        temp.points = [GraphicPoint(0, 0),
                       GraphicPoint(300, 300)]
        self.__shape['lines'].append(body)
        self.__shape['lines'].append(sensing)
        self.__shape['lines'].append(temp)

    def set_view_coordinate(self, view, relation=None):
        self.view = view
        # self.view_offset_x = x
        # self.view_offset_y = y
        self.relation = relation
        self.__reset_shape()

    def update(self, msec=100):

        self.__test_tmp()

        key_state = pygame.key.get_pressed()
        if key_state[pygame.K_LEFT]:
            pass
        elif key_state[pygame.K_RIGHT]:
            pass
        elif key_state[pygame.K_UP]:
            pass
        elif key_state[pygame.K_DOWN]:
            pass

    def draw(self, bg=WHITE):
        self.win.fill(bg)

        for circle in self.__shape['circles']:
            x, y, r = circle.get_element()
            pygame.draw.circle(self.win, circle.color, [x, y], r, circle.width)

        for line in self.__shape['lines']:
            line_ = []
            for point in line.points:
                line_.append(point.get_element())

            if line.line_type == 1:
                pygame.draw.lines(self.win, line.color, False, line_, line.width)
            elif line.line_type == 2:
                pygame.draw.lines(self.win, line.color, True, line_, line.width)
            elif line.line_type == 3:
                pygame.draw.polygon(self.win, line.color, line_, line.width)
            else:
                raise Exception('line type error; {}'.format(line.line_type))

        self.screen.blit(self.win, (self.left, self.top))

