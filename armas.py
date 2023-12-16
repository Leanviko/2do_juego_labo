import pygame
import json

from assets import *

with open("variables.json","r") as var:
    variables = json.load(var)

ANCHO_PANTALLA = variables["ANCHO_PANTALLA"]
GRAVEDAD = variables["GRAVEDAD"]

class Bala(pygame.sprite.Sprite):
    def __init__(self,x,y,direccion,escala):
        pygame.sprite.Sprite.__init__(self)
        self.velocidad = 10
        self.image = bala_img.convert_alpha()
        self.image = pygame.transform.scale_by(self.image,escala)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direccion = direccion

    def update(self,personaje,grupo_balas,grupo_enemigos, lista_obstaculos,deslizamiento_pantalla):
        #mover balas
        self.rect.x += (self.direccion * self.velocidad) + deslizamiento_pantalla
        #chequear si las balas salen de la pantalla
        if self.rect.right < 0 or self.rect.left > ANCHO_PANTALLA:
            self.kill()
        #chequear si exite colision con los elementos de nivel
        for bloque in lista_obstaculos:
            if bloque[1].colliderect(self.rect):
                    self.kill()
        
        if pygame.sprite.spritecollide(personaje, grupo_balas, False):
                if personaje.vive:
                    personaje.salud -= 10
                    self.kill()
        
        for enemigo in grupo_enemigos:
            if pygame.sprite.spritecollide(enemigo, grupo_balas, False):
                if enemigo.vive:
                    enemigo.salud -= 10
                    print(enemigo.salud)
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
        self.ancho = self.image.get_width()
        self.alto = self.image.get_height()
        self.direccion = direccion
        
    
    def update(self,grupo_explosiones,grupo_enemigos,jugador, lista_obstaculos, deslizamiento_pantalla):
        self.velocidad_y += GRAVEDAD
        dy = self.velocidad_y
        dx = self.direccion * self.velocidad

        #chequeamos colision con en nivel
        for bloque in lista_obstaculos:
            if bloque[1].colliderect(self.rect.x + dx, self.rect.y, self.ancho, self.alto):
                self.direccion *= -1
                dx = self.direccion * self.velocidad

        #chequeamos colision con elementos nivel
        for bloque in lista_obstaculos:
            #la colision agrego dx, dy para determinar la colision antes de que ocurra. dx,dy cambian antes de cambiar la pos del rectangulo
            if bloque[1].colliderect(self.rect.x + dx, self.rect.y, self.ancho, self.alto):
                dx = 0 # dejara de moverse en x
            if bloque[1].colliderect(self.rect.x, self.rect.y + dy, self.ancho, self.alto):
                self.velocidad = 0
#---> no entiendo   
                #chekeamos si es lanzadar
                if self.velocidad_y < 0:
                    self.velocidad_y = 0
                    dy = bloque[1].bottom - self.rect.top
                #chequeamos cuando cae
                elif self.velocidad_y > 0:
                    self.velocidad_y = 0
                    dy = bloque[1].top - self.rect.bottom


        
        #actualizar posicion granada
        self.rect.centerx += dx + deslizamiento_pantalla
        self.rect.centery += int(dy)
        
        #contador granada
        self.tiempo_explosion -= 1
        if self.tiempo_explosion <= 0:
            self.kill()
            explosion = Explosion(self.rect.centerx, self.rect.centery, 1)
            grupo_explosiones.add(explosion)

        #radio de daño
            # if abs(self.rect.centerx - jugador.rect.centerx)< BLOQUE_TAMANIO //2 or \
            #         abs(self.rect.centery - jugador.rect.centery)< BLOQUE_TAMANIO //2:
            #         jugador.salud -= 25

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

    def update(self, deslizamiento_pantalla):

        self.rect.x += deslizamiento_pantalla
        PAUSA_ANIMACION = 4
        self.contador += 1

        if self.contador >= PAUSA_ANIMACION:
            self.contador = 0
            self.indice_frame += 1
            
            if self.indice_frame >= len(self.imagenes_exp):
                self.kill() #elimino la animacion cuando se completa
            else:
                self.image = self.imagenes_exp[self.indice_frame]

