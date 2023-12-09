import pygame
import json

from assets import *

with open("variables.json","r") as var:
    variables = json.load(var)

ANCHO_PANTALLA = variables["ANCHO_PANTALLA"]
GRAVEDAD = variables["GRAVEDAD"]
BLOQUE_TAMANIO = variables["BLOQUE_TAMANIO"]

class Bala(pygame.sprite.Sprite):
    def __init__(self,x,y,direccion):
        pygame.sprite.Sprite.__init__(self)
        self.velocidad = 10
        self.image = bala_img.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direccion = direccion

    def update(self,personaje,grupo_balas,grupo_enemigos):
        #mover balas
        self.rect.x += (self.direccion * self.velocidad)
        #chequear si las balas salen de la pantalla
        if self.rect.right < 0 or self.rect.left > ANCHO_PANTALLA:
            self.kill()
        
        for enemigo in grupo_enemigos:
            if pygame.sprite.spritecollide(enemigo, grupo_balas, False):
                if personaje.vive:
                    enemigo.salud -= 10
                    self.kill()


class Granada(pygame.sprite.Sprite):
    def __init__(self,x,y,direccion):
        pygame.sprite.Sprite.__init__(self)
        self.tiempo_explosion = 100
        self.velocidad_y = -11
        self.velocidad = 7
        self.image = granada_img.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direccion = direccion
        
    
    def update(self,grupo_explosiones,grupo_enemigos):
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
        
        #contador granada
        self.tiempo_explosion -= 1
        if self.tiempo_explosion <= 0:
            self.kill()
            explosion = Explosion(self.rect.centerx, self.rect.centery, 1)
            grupo_explosiones.add(explosion)

            #radio de daño
            for enemigo in grupo_enemigos:
                if abs(self.rect.centerx - enemigo.rect.centerx)< BLOQUE_TAMANIO //2 or \
                    abs(self.rect.centery - enemigo.rect.centery)< BLOQUE_TAMANIO //2:
                    enemigo.salud -= 50
                    print(enemigo.salud)

class Explosion(pygame.sprite.Sprite):
    def __init__(self,x,y,escala):
        pygame.sprite.Sprite.__init__(self)

        #animacion de explosion
        self.imagenes_exp = []
        for num in range(1,6):
            img = pygame.image.load(f'img/explosion/exp{num}.png').convert_alpha()
            img = pygame.transform.scale_by(img,escala)
            self.imagenes_exp.append(img)
        
        self.indice_frame = 0
        self.image = self.imagenes_exp[self.indice_frame]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.contador = 0 #controlar animacion

    def update(self):
        PAUSA_ANIMACION = 4
        self.contador += 1

        if self.contador >= PAUSA_ANIMACION:
            self.contador = 0
            self.indice_frame += 1
            
            if self.indice_frame >= len(self.imagenes_exp):
                self.kill() #elimino la animacion cuando se completa
            else:
                self.image = self.imagenes_exp[self.indice_frame]

