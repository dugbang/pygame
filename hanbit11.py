import pygame
from pygame.color import Color
from runner import Runner

FPS = 28

if __name__ == "__main__":
    pygame.init()

    size = (400, 300)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Runner Animation Group")

    run = True
    clock = pygame.time.Clock()

    background_img = pygame.image.load("./hanbit/background.png")

    runner1 = Runner()
    runner1.rect.x = 0
    runner1.rect.y = 170

    runner2 = Runner()
    runner2.rect.x = 130
    runner2.rect.y = 170

    runner3 = Runner()
    runner3.rect.x = 250
    runner3.rect.y = 170

    runner_group = pygame.sprite.Group()
    runner_group.add(runner1)
    runner_group.add(runner2)
    runner_group.add(runner3)

    # 게임 루프
    while run:
        # 1) 사용자 입력 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # 2) 게임 상태 업데이트
        runner_group.update()

        # 3) 게임 상태 그리기
        screen.blit(background_img, screen.get_rect())
        runner_group.draw(screen)
        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()
