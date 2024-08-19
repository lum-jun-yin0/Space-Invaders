import pygame as py, random
from spaceship import Spaceship
from alien import Alien
from laser import Laser
from alien import MysteryShip

class Game:
    def __init__(self, screen_width, screen_height, offset):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.offset = offset
        self.spaceship_group = py.sprite.GroupSingle()
        self.spaceship_group.add(Spaceship(self.screen_width, self.screen_height, self.offset))
        self.aliens_group = py.sprite.Group()
        self.create_aliens()
        self.aliens_direction = 1
        self.alien_lasers_group = py.sprite.Group()
        self.mystery_ship_group = py.sprite.GroupSingle()
        self.lives = 3
        self.run = True
        self.score = 0
        self.highscore = 0
        self.explosion_sound = py.mixer.Sound("audio/explosion.ogg")
        self.load_highscore()
        py.mixer.music.load("audio/music.ogg")
        py.mixer.music.play(-1)

    def create_aliens(self):
        for row in range(5):
            for column in range(14):
                x = 75 + column * 55
                y = 110 + row * 55

                if row == 0:
                    alien_type = 3
                elif row in (1, 2):
                    alien_type = 2
                else:
                    alien_type = 1
                
                alien = Alien(alien_type, x + self.offset/2, y)
                self.aliens_group.add(alien)

    def move_aliens(self):
        self.aliens_group.update(self.aliens_direction)

        alien_sprites = self.aliens_group.sprites()
        for alien in alien_sprites:
            if alien.rect.right >= self.screen_width + self.offset/2:
                self.aliens_direction = -1
                self.alien_move_down(2)
            elif alien.rect.left <= self.offset/2:
                self.aliens_direction = 1
                self.alien_move_down(2)

    def alien_move_down(self, distance):
        if self.aliens_group:
            for alien in self.aliens_group.sprites():
                alien.rect.y += distance

    def alien_shoot_laser(self):
        if self.aliens_group.sprites():
            random_alien = random.choice(self.aliens_group.sprites())
            laser_sprite = Laser(random_alien.rect.center, -3, self.screen_height)
            self.alien_lasers_group.add(laser_sprite)

    def create_mystery_ship(self):
        self.mystery_ship_group.add(MysteryShip(self.screen_width, self.offset))

    def check_for_collisions(self):
        #Spaceship
        if self.spaceship_group.sprite.lasers_group:
            for laser_sprite in self.spaceship_group.sprite.lasers_group:
                
                aliens_hit =  py.sprite.spritecollide(laser_sprite, self.aliens_group, True)
                if aliens_hit:
                    self.explosion_sound.play()
                    for alien in aliens_hit:
                        self.score += alien.type*100
                        self.check_for_highscore()
                    laser_sprite.kill()
                if py.sprite.spritecollide(laser_sprite, self.mystery_ship_group, True):
                    self.score += 500
                    self.explosion_sound.play()
                    self.check_for_highscore()
                    laser_sprite.kill()

        #Alien's laser
        if self.alien_lasers_group:
            for laser_sprite in self.alien_lasers_group:
                if py.sprite.spritecollide(laser_sprite, self.spaceship_group, False):
                    laser_sprite.kill()
                    print("Tagged")
                    self.lives -= 1
                    if self.lives == 0:
                        self.game_over()

        if self.aliens_group:
            for alien in self.aliens_group:
                if py.sprite.spritecollide(alien, self.spaceship_group, False):
                    print("Downed")
                    self.lives -= 3
                    if self.lives == 0:
                        self.game_over()
    
    def game_over(self):
        self.run = False
        py.mixer.music.stop()

    def reset(self):
        self.run = True
        self.lives = 3
        self.spaceship_group.sprite.reset()
        self.aliens_group.empty()
        self.alien_lasers_group.empty()
        self.create_aliens()
        self.mystery_ship_group.empty()
        self.score = 0

    def check_for_highscore(self):
        if self.score > self.highscore:
            self.highscore = self.score

            with open("highscore.txt", "w") as file:
                file.write(str(self.highscore))

    def load_highscore(self):
        try:
            with open("highscore.txt", "r") as file:
                self.highscore = int(file.read())

        except FileNotFoundError:
            self.highscore = 0
