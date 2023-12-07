import pygame
import json

with open("variables.json","r") as var:
    variables = json.load(var)

ANCHO_PANTALLA = variables["ANCHO_PANTALLA"]

class Bala(pygame.sprite.Sprite):
    def __init__(self,x,y,direccion):
        pygame.sprite.Sprite.__init__(self)
        self.velocidad = 10
        self.image = pygame.image.load('img/iconos/bala.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direccion = direccion

    def update(self):
        #mover balas
        self.rect.x += (self.direccion * self.velocidad)
        #chear si las balas salen de la pantalla
        if self.rect.right < 0 or self.rect.left > ANCHO_PANTALLA:
            self.kill()
        