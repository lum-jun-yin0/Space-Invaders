import pygame as py, sys, random
from game import Game

py.init()

SCREEN_WIDTH = 1250
SCREEN_HEIGHT = 650
OFFSET = 50

GREY = (29, 29, 27)
YELLOW = (243, 216, 63)

font = py.font.Font("Font/monogram.ttf", 40)
level_surface = font.render("LEVEL 01",False, YELLOW)
game_over_surface = font.render("GAME OVER", False, YELLOW)
restart_surface = font.render("Press spacebar to restart", False, YELLOW)
score_text_surface = font.render("SCORE", False, YELLOW)
highscore_text_surface = font.render("HIGHSCORE", False, YELLOW)

screen = py.display.set_mode((SCREEN_WIDTH + OFFSET, SCREEN_HEIGHT + 2*OFFSET))
py.display.set_caption("Space Invaders")

clock = py.time.Clock()

game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, OFFSET )

#PRONE TO CHANGE
SHOOT_LASER = py.USEREVENT
py.time.set_timer(SHOOT_LASER, 300)

MYSTERYSHIP = py.USEREVENT + 1
py.time.set_timer(MYSTERYSHIP, random.randint(4000,8000))

while True:
    for event in py.event.get():
        if event.type == py.QUIT:
            py.exit()
            sys.exit()
        if event.type == SHOOT_LASER and game.run:
            game.alien_shoot_laser()
        if event.type == MYSTERYSHIP and game.run:
            game.create_mystery_ship()
            py.time.set_timer(MYSTERYSHIP, random.randint(4000,8000))

        keys = py.key.get_pressed()
        if keys[py.K_SPACE] and game.run == False:
            game.reset()
    
    #Updating
    if game.run:
        game.spaceship_group.update()
        game.move_aliens()
        game.alien_lasers_group.update()
        game.mystery_ship_group.update()
        game.check_for_collisions()

    #Drawing
    screen.fill(GREY)
    py.draw.rect(screen, YELLOW, (10, 10, 1280, 710), 2, 0, 60, 60, 60, 60)
    py.draw.line(screen, YELLOW, (20, 660), (1280, 660), 3)
    if game.run:
        screen.blit(level_surface, (1125, 675, 50, 50))
    else:
        screen.blit(game_over_surface, (1125, 675, 50, 50))
        screen.blit(restart_surface, (625, 325, 50, 50))

    game.spaceship_group.draw(screen)
    game.spaceship_group.sprite.lasers_group.draw(screen)
    game.aliens_group.draw(screen)
    game.alien_lasers_group.draw(screen)
    game.mystery_ship_group.draw(screen)

    x = 50
    for life in range(game.lives):
        screen.blit(game.spaceship_group.sprite.image, (x, 675))
        x += 50

    screen.blit(score_text_surface, (50, 15, 50, 50))
    formatted_score = str(game.score).zfill(5)
    score_surface = font.render(formatted_score, False, YELLOW)
    screen.blit(score_surface, (50, 40, 50, 50))
    screen.blit(highscore_text_surface, (1115, 15, 50, 50))
    formatted_highscore = str(game.highscore).zfill(5)
    highscore_surface = font.render(formatted_highscore, False, YELLOW)
    screen.blit(highscore_surface, (1175, 40, 50, 50))

    py.display.update()
    clock.tick(60)

    #not doing obstacle cus gay