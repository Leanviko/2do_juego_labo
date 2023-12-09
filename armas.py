import pygame
import json
from assets import *

with open("variables.json","r") as var:
    variables = json.load(var)

ANCHO_PANTALLA = variables["ANCHO_PANTALLA"]
GRAVEDAD = variables["GRAVEDAD"]

class Bala(pygame.sprite.Sprite):
    def __init__(self,x,y,direccion):
        pygame.sprite.Sprite.__init__(self)
        self.velocidad = 10
        self.image = bala_img.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direccion = direccion

    def update(self,personaje,grupo_balas):
        #mover balas
        self.rect.x += (self.direccion * self.velocidad)
        #chequear si las balas salen de la pantalla
        if self.rect.right < 0 or self.rect.left > ANCHO_PANTALLA:
            self.kill()
        
        if pygame.sprite.spritecollide(personaje, grupo_balas, False):
            if personaje.vive:
                personaje.salud -= 10
                self.kill()

class Granada(pygame.sprite.Sprite):
    def __init__(self,x,y,direccion):
        pygame.sprite.Sprite.__init__(self)
        self.tiempo_explocion = 100
        self.velocidad_y = -11
        self.velocidad = 7
        self.image = granada_img.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direccion = direccion
    
    def update(self):
        self.velocidad_y += GRAVEDAD
        dy = self.velocidad_y
        dx = self.direccion * self.velocidad

        #colision con el suelo
        if self.rect.bottom + dy > 300:
            self.velocidad = 0
            dy = 300 - self.rect.bottom

        #rebote con el borde de pantalla
        if self.rect.left + dx < 0 or self.rect.right + dx > ANCHO_PANTALLA:
            self.direccion *= -1

        
        #actualizar posicion granada
        self.rect.centerx += dx
        self.rect.centery += dy

class Explosion(pygame.sprite.Sprite):
    def __init__(self,x,y,escala):
        pygame.sprite.Sprite.__init__(self)

        #animacion de explosion
        self.imagenes_exp =[]
        for num in range(1,6):
            img = pygame.image.load(f'img/explosion/exp{num}.png').convert_alpha()
            img = pygame.transform.scale_by(img,escala)
            self.imagenes_exp.append(img)
        
        self.indice_frame = 0
        self.image = imagenes_exp[self.indice_frame]
        self.rect = self.image.get_rect()
        self.contador = 0 #controlar animacion

