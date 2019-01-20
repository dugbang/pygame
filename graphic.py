import pygame

from constant import WIDTH, HEIGHT, FPS, BLACK, BLUE, GREEN, RED
from pixel import PixelWindow

pygame.init()

# WIDTH = 720
# HEIGHT = 405

size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("graphic testing")

clock = pygame.time.Clock()


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

    all_sprites = pygame.sprite.Group()
    player = Player()
    all_sprites.add(player)
    player2 = Player()
    player2.rect.center = (WIDTH / 3, HEIGHT / 3)
    all_sprites.add(player2)

    run = True
    key = None
    update_flag = True
    start_pos = [0, 0]

    win_main = PixelWindow(50, 50, 660, 508, screen)
    win_mini = PixelWindow(760, 50, 270, 250, screen)
    win_info = PixelWindow(760, 330, 270, 220, screen)

    # Game Loop
    while run:
        time_passed = clock.tick(FPS)
        # print(time_passed)  # real time milli second

        # 1) 사용자 입력 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                key = event.key

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            print('update_flag; ', update_flag)
            update_flag = False if update_flag else True

        # 2) 게임 논리 실행
        win_main.update(time_passed)
        win_mini.update(time_passed)
        win_info.update(time_passed)

        # 2) 게임 상태 업데이트
        if start_pos[0] > screen.get_width():
            start_pos[0] = 0
        else:
            start_pos[0] += 5

        if update_flag:
            all_sprites.update()

        # 3) 게임 상태 그리기
        screen.fill(BLACK)
        all_sprites.draw(screen)

        if key == pygame.K_1 or key == pygame.K_LEFT:
            pygame.draw.line(screen, BLACK,
                             start_pos,
                             (screen.get_width(), screen.get_height()), 10)
        elif key == pygame.K_2 or key == pygame.K_RIGHT:
            pygame.draw.ellipse(screen, RED,
                                pygame.Rect(start_pos, (50, 50)))
        elif key == pygame.K_3 or key == pygame.K_UP:
            pygame.draw.polygon(screen, GREEN,
                                [start_pos,
                                 (0, screen.get_height()),
                                 (screen.get_width(), screen.get_height())])
        elif key == pygame.K_4 or key == pygame.K_DOWN:
            pygame.draw.rect(screen, BLUE,
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

    pygame.quit()

