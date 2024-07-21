import pygame as py, random

class Alien(py.sprite.Sprite):
    def __init__(self, type, x, y):
        super().__init__()
        self.type = type
        path = f"Graphics/alien_{type}.png"
        self.image = py.image.load(path)
        self.rect = self.image.get_rect(topleft = (x, y))
    
    def update(self, direction):
        self.rect.x += direction
    
class MysteryShip(py.sprite.Sprite):
    def __init__(self, screen_width, offset):
        super().__init__()
        self.screen_width = screen_width
        self.offset = offset
        self.image = py.image.load("Graphics/mystery.png")

        x =  random.choice([self.offset/2, screen_width + self.offset/2 - self.image.get_width()])
        if x == self.offset/2 :
            self.speed = 5
        else:
            self.speed  = -5

        self.rect = self.image.get_rect(topleft = (x, 90))

    def update(self):
        self.rect.x += self.speed
        if self.rect.right > self.screen_width + self.offset/2:
            self.kill()
        elif self.rect.left < self.offset/2:
            self.kill()