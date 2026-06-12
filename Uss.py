import random
import pygame
import os

# Pygame algatamine
pygame.init()
pygame.mixer.init()

# High score fail
HIGHSCORE_FILE = "highscore.txt"

def load_highscore():
    if os.path.exists(HIGHSCORE_FILE):
        with open(HIGHSCORE_FILE, "r") as f:
            try:
                return int(f.read())
            except:
                return 0
    return 0

def save_highscore(score):
    with open(HIGHSCORE_FILE, "w") as f:
        f.write(str(score))

high_score = load_highscore()

# Taustamuusika
pygame.mixer.music.load("Raining tacos.mp3")
pygame.mixer.music.set_volume(0.9)
pygame.mixer.music.play(-1)

# Pildid
apple_img = pygame.image.load("Apple.png")
apple_img = pygame.transform.scale(apple_img, (20, 20))

coin_img = pygame.image.load("Coin.png")
coin_img = pygame.transform.scale(coin_img, (20, 20))

snake_head_img = pygame.image.load("Head.png")
snake_body_img = pygame.image.load("Body.png")
snake_tail_img = pygame.image.load("Saba.png")
snake_corner_img = pygame.image.load("Corner.png")

snake_head_img = pygame.transform.scale(snake_head_img, (20, 20))
snake_body_img = pygame.transform.scale(snake_body_img, (20, 20))
snake_tail_img = pygame.transform.scale(snake_tail_img, (20, 20))
snake_corner_img = pygame.transform.scale(snake_corner_img, (20, 20))

# Värvid
green = (0, 102, 51)
taust = (153, 232, 158)

# Ekraan
dis_width = 800
dis_height = 600
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Ussimäng - Metsjärv')

clock = pygame.time.Clock()

snake_block = 20
snake_speed = 10

font_style = pygame.font.SysFont("Comic Sans MS", 24, bold=True)
score_font = pygame.font.SysFont("Comic Sans MS", 35, bold=True)


def your_score(score, high_score):
    text = score_font.render(
        f"Score: {score}  High Score: {high_score}", True, green
    )
    dis.blit(text, [10, 10])


def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])


def get_direction(from_pos, to_pos):
    dx = to_pos[0] - from_pos[0]
    dy = to_pos[1] - from_pos[1]

    if dx > 0:
        return "RIGHT"
    if dx < 0:
        return "LEFT"
    if dy > 0:
        return "DOWN"
    return "UP"


def get_rotation(direction):
    return {"RIGHT": 0, "DOWN": 270, "LEFT": 180, "UP": 90}[direction]


def is_corner(dir_in, dir_out):
    return dir_in != dir_out


def get_corner_rotation(dir_in, dir_out):
    combos = {
        ("RIGHT", "UP"): 270,
        ("DOWN", "LEFT"): 270,
        ("RIGHT", "DOWN"): 0,
        ("UP", "LEFT"): 0,
        ("LEFT", "UP"): 180,
        ("DOWN", "RIGHT"): 180,
        ("LEFT", "DOWN"): 90,
        ("UP", "RIGHT"): 90,
    }
    return combos.get((dir_in, dir_out), 0)


def our_snake(snake_list, direction="RIGHT"):
    if len(snake_list) == 0:
        return

    if len(snake_list) == 1:
        x, y = snake_list[0]
        rotated = pygame.transform.rotate(snake_head_img, get_rotation(direction))
        dis.blit(rotated, (x, y))
        return

    for i, segment in enumerate(snake_list):
        x, y = segment

        if i == 0:
            dir_ = get_direction(snake_list[i], snake_list[i + 1])
            rotated = pygame.transform.rotate(snake_tail_img, get_rotation(dir_))
            dis.blit(rotated, (x, y))

        elif i == len(snake_list) - 1:
            dir_ = get_direction(snake_list[i - 1], snake_list[i])
            rotated = pygame.transform.rotate(snake_head_img, get_rotation(dir_))
            dis.blit(rotated, (x, y))

        else:
            dir_in = get_direction(snake_list[i - 1], snake_list[i])
            dir_out = get_direction(snake_list[i], snake_list[i + 1])

            if is_corner(dir_in, dir_out):
                rotated = pygame.transform.rotate(
                    snake_corner_img,
                    get_corner_rotation(dir_in, dir_out)
                )
            else:
                rotated = pygame.transform.rotate(
                    snake_body_img,
                    get_rotation(dir_in)
                )

            dis.blit(rotated, (x, y))


def gameloop():
    global high_score

    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_list = []
    length_of_snake = 1
    score = 0

    foodx = random.randrange(0, dis_width - snake_block, snake_block)
    foody = random.randrange(0, dis_height - snake_block, snake_block)

    coinx = random.randrange(0, dis_width - snake_block, snake_block)
    coiny = random.randrange(0, dis_height - snake_block, snake_block)

    coin_visible = False
    coin_timer = 0

    while not game_over:

        coin_timer += 1

        if not coin_visible and coin_timer >= snake_speed * 10:
            coinx = random.randrange(0, dis_width - snake_block, snake_block)
            coiny = random.randrange(0, dis_height - snake_block, snake_block)
            coin_visible = True
            coin_timer = 0

        if coin_visible and coin_timer >= snake_speed * 5:
            coin_visible = False
            coin_timer = 0

        while game_close:
            dis.fill(taust)

            dis.blit(apple_img, (foodx, foody))
            if coin_visible:
                dis.blit(coin_img, (coinx, coiny))

            message("You lost! R - restart | Q - quit", green)

            your_score(score, high_score)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_r:
                        return gameloop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change

        dis.fill(taust)
        dis.blit(apple_img, (foodx, foody))

        if coin_visible:
            dis.blit(coin_img, (coinx, coiny))

        snake_head = [x1, y1]
        snake_list.append(snake_head)

        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        if x1_change > 0:
            direction = "RIGHT"
        elif x1_change < 0:
            direction = "LEFT"
        elif y1_change < 0:
            direction = "UP"
        elif y1_change > 0:
            direction = "DOWN"
        else:
            direction = "RIGHT"

        our_snake(snake_list, direction)
        your_score(score, high_score)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            while [foodx, foody] in snake_list:
                foodx = random.randrange(0, dis_width - snake_block, snake_block)
                foody = random.randrange(0, dis_height - snake_block, snake_block)
            length_of_snake += 1
            score += 1

        if coin_visible and x1 == coinx and y1 == coiny:
            score += 10   # <-- MUUTUS: +10
            length_of_snake += 1
            coin_visible = False
            coin_timer = 0

        clock.tick(snake_speed)

    if score > high_score:
        high_score = score
        save_highscore(high_score)

    pygame.mixer.music.stop()
    pygame.quit()
    quit()


gameloop()
