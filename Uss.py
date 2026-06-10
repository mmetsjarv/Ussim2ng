import random
import pygame

# --- Pygame algatamine ---
pygame.init()
pygame.mixer.init()

# Taustamuusika laadimine ja käivitamine
pygame.mixer.music.load("Raining tacos.mp3")
pygame.mixer.music.set_volume(0.9)      # heli tugevus (0.0 kuni 1.0)
pygame.mixer.music.play(-1)             # -1 = mängib lõputult

# --- Piltide laadimine ---
apple_img = pygame.image.load("Apple.png")
apple_img = pygame.transform.scale(apple_img, (20, 20))

coin_img = pygame.image.load("Coin.png")
coin_img = pygame.transform.scale(coin_img, (20, 20))

snake_head_img = pygame.image.load("Head.png")
snake_body_img = pygame.image.load("Body.png")
snake_tail_img = pygame.image.load("Saba.png")
snake_corner_img = pygame.image.load("Corner.png")

# Ussi graafika suuruse muutmine
snake_head_img = pygame.transform.scale(snake_head_img, (20, 20))
snake_body_img = pygame.transform.scale(snake_body_img, (20, 20))
snake_tail_img = pygame.transform.scale(snake_tail_img, (20, 20))
snake_corner_img = pygame.transform.scale(snake_corner_img, (20, 20))

# --- Värvid ---
green = (0, 102, 51)
taust = (153, 232, 158)

# --- Ekraani mõõtmed ---
dis_width = 800
dis_height = 600

# Mänguakna loomine
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Ussimäng - Metsjärv')

clock = pygame.time.Clock()

# Ussi seaded
snake_block = 20   # ühe ruudu suurus
snake_speed = 10   # kiirus

# Fondid (teksti jaoks)
font_style = pygame.font.SysFont("Comic Sans MS", 24, bold=True)
score_font = pygame.font.SysFont("Comic Sans MS", 35, bold=True)

# --- Punktide kuvamine ---
def your_score(score):
    value = score_font.render("Your Score: " + str(score), True, green)
    dis.blit(value, [0, 0])

# --- Sõnumi kuvamine (nt "kaotasid") ---
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])

# --- Suuna arvutamine kahe punkti vahel ---
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

# --- Suuna pööramine pildile ---
def get_rotation(direction):
    return {"RIGHT": 0, "DOWN": 270, "LEFT": 180, "UP": 90}[direction]

# --- Kas kehaosa on kurv ---
def is_corner(dir_in, dir_out):
    return dir_in != dir_out

# --- Kurvi õige pööramine ---
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

# --- Ussi joonistamine ---
def our_snake(snake_list, direction="RIGHT"):
    if len(snake_list) == 0:
        return

    # Kui ainult 1 osa, joonista pea
    if len(snake_list) == 1:
        x, y = snake_list[0]
        angle = get_rotation(direction)
        rotated = pygame.transform.rotate(snake_head_img, angle)
        dis.blit(rotated, (x, y))
        return

    for i, segment in enumerate(snake_list):
        x, y = segment

        # Saba (esimene segment)
        if i == 0:
            direction = get_direction(snake_list[i], snake_list[i + 1])
            angle = get_rotation(direction)
            rotated = pygame.transform.rotate(snake_tail_img, angle)
            dis.blit(rotated, (x, y))

        # Pea (viimane segment)
        elif i == len(snake_list) - 1:
            direction = get_direction(snake_list[i - 1], snake_list[i])
            angle = get_rotation(direction)
            rotated = pygame.transform.rotate(snake_head_img, angle)
            dis.blit(rotated, (x, y))

        # Keha
        else:
            dir_in = get_direction(snake_list[i - 1], snake_list[i])
            dir_out = get_direction(snake_list[i], snake_list[i + 1])

            # Kui kurv
            if is_corner(dir_in, dir_out):
                angle = get_corner_rotation(dir_in, dir_out)
                rotated = pygame.transform.rotate(snake_corner_img, angle)
            else:
                angle = get_rotation(dir_in)
                rotated = pygame.transform.rotate(snake_body_img, angle)

            dis.blit(rotated, (x, y))

# --- Põhimäng ---
def gameloop():
    game_over = False
    game_close = False

    # Algpositsioon
    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_list = []
    length_of_snake = 1
    score = 0

    # Toidu asukoht
    foodx = random.randrange(0, dis_width - snake_block, snake_block)
    foody = random.randrange(0, dis_height - snake_block, snake_block)

    # Mündi (boonuse) asukoht
    coinx = random.randrange(0, dis_width - snake_block, snake_block)
    coiny = random.randrange(0, dis_height - snake_block, snake_block)

    coin_visible = False
    coin_timer = 0

    while not game_over:

        coin_timer += 1

        # Mündi ilmumine
        if not coin_visible and coin_timer >= snake_speed * 10:
            coinx = random.randrange(0, dis_width - snake_block, snake_block)
            coiny = random.randrange(0, dis_height - snake_block, snake_block)
            coin_visible = True
            coin_timer = 0

        # Mündi kadumine
        if coin_visible and coin_timer >= snake_speed * 5:
            coin_visible = False
            coin_timer = 0

        # --- Kaotuse ekraan ---
        while game_close:
            dis.fill(taust)

            dis.blit(apple_img, (foodx, foody))

            if coin_visible:
                dis.blit(coin_img, (coinx, coiny))

            message("You lost! Press R-Play again or Q-Quit", green)

            score_text = score_font.render("Your Score: " + str(score), True, green)
            dis.blit(score_text, [dis_width / 3, dis_height / 2])

            pygame.display.update()

            # Taaskäivitus või väljumine
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_r:
                        return gameloop()

        # --- Sisendi kontroll ---
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

        # --- Piiridest väljumine ---
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True

        # Liikumine
        x1 += x1_change
        y1 += y1_change

        dis.fill(taust)
        dis.blit(apple_img, (foodx, foody))

        if coin_visible:
            dis.blit(coin_img, (coinx, coiny))

        # Ussi uuendamine
        snake_head = [x1, y1]
        snake_list.append(snake_head)

        if len(snake_list) > length_of_snake:
            del snake_list[0]

        # Enda otsa põrkumine
        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        # Suuna määramine
        if x1_change > 0:
            current_direction = "RIGHT"
        elif x1_change < 0:
            current_direction = "LEFT"
        elif y1_change < 0:
            current_direction = "UP"
        elif y1_change > 0:
            current_direction = "DOWN"
        else:
            current_direction = "RIGHT"

        # Ussi joonistamine
        our_snake(snake_list, current_direction)

        # Punktid
        your_score(score)

        pygame.display.update()

        # --- Õuna söömine ---
        if x1 == foodx and y1 == foody:
            while [foodx, foody] in snake_list:
                foodx = random.randrange(0, dis_width - snake_block, snake_block)
                foody = random.randrange(0, dis_height - snake_block, snake_block)
            length_of_snake += 1
            score += 1

        # --- Mündi võtmine ---
        if coin_visible and x1 == coinx and y1 == coiny:
            score += 5
            length_of_snake += 1
            coin_visible = False
            coin_timer = 0

        clock.tick(snake_speed)

    pygame.mixer.music.stop()
    pygame.quit()
    quit()

# Mängu käivitamine
gameloop()
