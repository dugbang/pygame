import pygame

from constant import WIDTH, HEIGHT, FPS, BLACK, BLUE, GREEN, RED
from pixel import PixelWindow


class MainWindow:
    pygame.init()

    def __init__(self, width=WIDTH, height=HEIGHT, title='title'):
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()

        pygame.display.set_caption(title)

        self.key = None

    def loop(self):
        all_sprites = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        player2 = Player()
        player2.rect.center = (WIDTH / 3, HEIGHT / 3)
        all_sprites.add(player2)

        run = True
        # key = None
        update_flag = True
        start_pos = [0, 0]

        win_main = PixelWindow(50, 50, 660, 508, self.screen)
        win_mini = PixelWindow(760, 50, 270, 250, self.screen)
        win_info = PixelWindow(760, 330, 270, 220, self.screen)

        while run:
            time_passed = self.clock.tick(FPS)

            # 1) 사용자 입력 처리
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.KEYDOWN:
                    self.key = event.key

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                print('update_flag; ', update_flag)
                update_flag = False if update_flag else True

            # 2) 게임 논리 실행
            win_main.update(time_passed)
            win_mini.update(time_passed)
            win_info.update(time_passed)

            # 2) 게임 상태 업데이트
            if start_pos[0] > self.screen.get_width():
                start_pos[0] = 0
            else:
                start_pos[0] += 5

            if update_flag:
                all_sprites.update()

            # 3) 게임 상태 그리기
            # 3) 게임 상태 그리기
            self.screen.fill(BLACK)
            all_sprites.draw(self.screen)

            if self.key == pygame.K_1 or self.key == pygame.K_LEFT:
                pygame.draw.line(self.screen, BLACK,
                                 start_pos,
                                 (self.screen.get_width(), self.screen.get_height()), 10)
            elif self.key == pygame.K_2 or self.key == pygame.K_RIGHT:
                pygame.draw.ellipse(self.screen, RED,
                                    pygame.Rect(start_pos, (50, 50)))
            elif self.key == pygame.K_3 or self.key == pygame.K_UP:
                pygame.draw.polygon(self.screen, GREEN,
                                    [start_pos,
                                     (0, self.screen.get_height()),
                                     (self.screen.get_width(), self.screen.get_height())])
            elif self.key == pygame.K_4 or self.key == pygame.K_DOWN:
                pygame.draw.rect(self.screen, BLUE,
                                 pygame.Rect(start_pos, (50, 50)))

            # all_sprites.draw(screen)
            # screen.blit(win_main, (50, 50))
            # pygame.draw.polygon(win_main, GREEN, [(100, 100), (300, 100), (100, 150), ])
            # screen.blit(win_mini, (760, 50))
            # screen.blit(win_info, (760, 330))
            win_main.draw(bg=BLUE)
            win_mini.draw(bg=GREEN)
            win_info.draw(bg=RED)

            pygame.display.flip()
            pass


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)

    def update(self):
        self.rect.x += 5
        if self.rect.left > WIDTH:
            self.rect.right = 0


if __name__ == "__main__":

    app = MainWindow()
    app.loop()
    pygame.quit()

