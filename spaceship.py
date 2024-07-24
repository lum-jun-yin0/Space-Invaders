import pygame as py
from laser import Laser

class Spaceship(py.sprite.Sprite):
    def __init__ (self, screen_width, screen_height, offset):
        super().__init__()
        self.offset = offset
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.image = py.image.load("Graphics/spaceship.png")
        self.rect = self.image.get_rect(midbottom = ((self.screen_width + self.offset)/2, self.screen_height))
        #movement speed
        self.speed = 10
        self.lasers_group = py.sprite.Group()
        self.laser_ready = True
        self.laser_time = 0
        #firing speed
        self.laser_delay = 300
        self.laser_sound = py.mixer.Sound("audio/laser.ogg")
    
    def get_user_input(self):
        keys = py.key.get_pressed()

        if keys[py.K_RIGHT]:
            self.rect.x += self.speed
        elif keys[py.K_LEFT]:
            self.rect.x -= self.speed
        elif keys[py.K_a]:
            self.rect.x -= self.speed
        elif keys[py.K_d]:
            self.rect.x += self.speed
        
        if keys[py.K_SPACE] and self.laser_ready:
            self.laser_ready = False
            laser = Laser(self.rect.center, 5, self.screen_height)
            self.lasers_group.add(laser)
            self.laser_time = py.time.get_ticks()
            self.laser_sound.play()
    
    def update(self):
        self.get_user_input()
        self.constrain_movement()
        self.lasers_group.update()
        self.recharge_laser()

    def constrain_movement(self):
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width
        if self.rect.left < self.offset:
            self.rect.left = self.offset
        
    def recharge_laser(self):
        if not self.laser_ready:
            current_time = py.time.get_ticks()
            if current_time - self.laser_time >= self.laser_delay:
                self.laser_ready = True
    
    def reset(self):
        self.rect = self.image.get_rect(midbottom = ((self.screen_width + self.offset)/2, self.screen_height))
        self.lasers_group.empty()