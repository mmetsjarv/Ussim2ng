import pygame
from pygame.locals import *
from snake import *
from apple import *

GAME_ON = True
SPEED = 10

pygame.init()
screen = pygame.display.set_mode((400, 400))
clock = pygame.time.Clock()
snake = Snake()
apple = Apple()
apple.set_random_position(400)

while GAME_ON:
    clock.tick(SPEED)
    snake.crawl()

    for event in pygame.event.get():
        if event.type == QUIT:
            GAME_ON = False
        if event.type == KEYDOWN:
            if event.key == K_UP and snake.direction != DOWN:
                print("UP")
                snake.direction = UP
            elif event.key == K_LEFT and snake.direction != RIGHT:
                print("LEFT")
                snake.direction = LEFT
            elif event.key == K_DOWN and snake.direction != UP:
                print("DOWN")
                snake.direction = DOWN
            elif event.key == K_RIGHT and snake.direction != LEFT:
                print("RIGHT")
                snake.direction = RIGHT

    if snake.wall_collision(400) or snake.self_collision():
        GAME_ON = False

    if snake.snake_eat_apple(apple.position):
        apple.set_random_position(400)
        snake.snake_bigger()
        SPEED += 0.5

    screen.fill((0, 0, 0))
    for snake_pos in snake.snake[0:-1]:
        screen.blit(snake.skin, snake_pos)
    screen.blit(snake.head, snake.snake[-1])
    screen.blit(apple.apple, apple.position)

    pygame.display.update()

pygame.quit()