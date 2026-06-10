import random
import pygame

pygame.init()  # Käivitab pygame'i

# Õuna pildi laadimine ja suuruse muutmine
apple_img = pygame.image.load("Apple.png")
apple_img = pygame.transform.scale(apple_img, (20, 20))

# Mündi pildi laadimine ja suuruse muutmine
coin_img = pygame.image.load("Coin.png")
coin_img = pygame.transform.scale(coin_img, (20, 20))

# Värvide määramine (RGB)
snek_color = (58, 0, 102)      # Ussi värv
green = (0, 102, 51)           # Teksti värv
taust = (153, 232, 158)        # Taustavärv

# Mänguakna mõõtmed
dis_width = 800
dis_height = 600

# Mänguakna loomine
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Ussimäng - Metsjärv')

# Kell kaadrite kiiruse kontrollimiseks
clock = pygame.time.Clock()

# Ussi ühe ruudu suurus
snake_block = 20

# Ussi liikumiskiirus
snake_speed = 10

# Fontide loomine
font_style = pygame.font.SysFont("Comic Sans MS", 24, bold=True)
score_font = pygame.font.SysFont("Comic Sans MS", 35, bold=True)


# Funktsioon punktide kuvamiseks
def your_score(score):
    value = score_font.render("Your Score: " + str(score), True, green)
    dis.blit(value, [0, 0])


# Funktsioon ussi joonistamiseks
def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, snek_color,
                         [x[0], x[1], snake_block, snake_block])


# Funktsioon sõnumi kuvamiseks
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])


# Peamine mängutsükkel
def gameloop():

    # Mängu olekud
    game_over = False
    game_close = False

    # Ussi alguskoht
    x1 = dis_width / 2
    y1 = dis_height / 2

    # Alguses uss ei liigu
    x1_change = 0
    y1_change = 0

    # Ussi keha list
    snake_list = []

    # Ussi algpikkus
    length_of_snake = 1

    # Punktid
    score = 0

    # Õuna juhuslik asukoht
    foodx = random.randrange(0, dis_width - snake_block, snake_block)
    foody = random.randrange(0, dis_height - snake_block, snake_block)

    # Mündi juhuslik asukoht
    coinx = random.randrange(0, dis_width - snake_block, snake_block)
    coiny = random.randrange(0, dis_height - snake_block, snake_block)

    # Münt alguses nähtamatu
    coin_visible = False

    # Taimer mündi ilmumiseks
    coin_timer = 0

    # Mäng käib seni, kuni game_over muutub True-ks
    while not game_over:

        # Suurendatakse mündi taimerit
        coin_timer += 1

        # Kui münt ei ole nähtav ja aeg täis, siis ilmub münt
        if not coin_visible and coin_timer >= snake_speed * 10:
            coinx = random.randrange(0, dis_width - snake_block, snake_block)
            coiny = random.randrange(0, dis_height - snake_block, snake_block)
            coin_visible = True
            coin_timer = 0

        # Kui münt on liiga kaua nähtav, siis kaob ära
        if coin_visible and coin_timer >= snake_speed * 5:
            coin_visible = False
            coin_timer = 0

        # Kaotuse ekraan
        while game_close:

            # Täidetakse taust
            dis.fill(taust)

            # Joonistatakse õun
            dis.blit(apple_img, (foodx, foody))

            # Kui münt on nähtav, joonistatakse ka münt
            if coin_visible:
                dis.blit(coin_img, (coinx, coiny))

            # Kuvatakse kaotuse teade
            message("You lost! Press R-Play again or Q-Quit", green)

            # Punktide tekst
            score_text = score_font.render(
                "Your Score: " + str(score),
                True,
                green
            )

            # Kuvatakse punktid
            dis.blit(score_text, [dis_width / 3, dis_height / 2])

            pygame.display.update()

            # Oodatakse kasutaja valikut
            for event in pygame.event.get():

                # Q lõpetab mängu
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False

                    # R alustab mängu uuesti
                    if event.key == pygame.K_r:
                        gameloop()

        # Sündmuste kontroll
        for event in pygame.event.get():

            # Akna sulgemine
            if event.type == pygame.QUIT:
                game_over = True

            # Klahvivajutused
            if event.type == pygame.KEYDOWN:

                # Vasakule
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0

                # Paremale
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0

                # Üles
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0

                # Alla
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        # Kui uss läheb ekraanilt välja, kaotab mängija
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True

        # Ussi asukoha uuendamine
        x1 += x1_change
        y1 += y1_change

        # Tausta värvimine
        dis.fill(taust)

        # Õuna joonistamine
        dis.blit(apple_img, (foodx, foody))

        # Mündi joonistamine, kui see on nähtav
        if coin_visible:
            dis.blit(coin_img, (coinx, coiny))

        # Ussi pea asukoht
        snake_head = [x1, y1]

        # Lisatakse pea ussi kehasse
        snake_list.append(snake_head)

        # Kui keha on liiga pikk, eemaldatakse vanim osa
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        # Kontrollitakse, kas uss sõitis iseendale otsa
        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        # Joonistatakse uss
        our_snake(snake_block, snake_list)

        # Kuvatakse punktid
        your_score(score)

        pygame.display.update()

        # Kui uss sööb õuna
        if x1 == foodx and y1 == foody:

            # Uus õuna asukoht
            foodx = random.randrange(
                0, dis_width - snake_block, snake_block)
            foody = random.randrange(
                0, dis_height - snake_block, snake_block)

            # Uss kasvab
            length_of_snake += 1

            # Punktid suurenevad
            score += 1

        # Kui uss võtab mündi
        if coin_visible and x1 == coinx and y1 == coiny:

            # Lisatakse 5 punkti
            score += 5

            # Uss kasvab ühe võrra
            length_of_snake += 1

            # Münt kaob
            coin_visible = False
            coin_timer = 0

        # Määrab mängu kiiruse
        clock.tick(snake_speed)

    # Sulgeb pygame'i
    pygame.quit()
    quit()


# Käivitatakse mäng
gameloop()
