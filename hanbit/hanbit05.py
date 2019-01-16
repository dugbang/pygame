import pygame

pygame.init()
screen = pygame.display.set_mode((300, 100))
pygame.display.set_caption("Drawing image")

clock = pygame.time.Clock()
run = True

# 이미지 로딩
runner_img = pygame.image.load("./runner.png")
runner_rect = runner_img.get_rect()

# 게임 루프
while run:
    # 1) 사용자 입력 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # 2) 게임 상태 업데이트
    if runner_rect.x > screen.get_width():
        runner_rect.x = 0
    else:
        runner_rect.x += 1

    # 3) 게임 상태 그리기
    screen.fill(pygame.color.Color(0, 0, 255))
    screen.blit(runner_img, runner_rect)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
