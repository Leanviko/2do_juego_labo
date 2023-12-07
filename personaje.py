import pygame
import json

with open("variables.json","r") as var:
    variables = json.load(var)

GRAVEDAD = variables["GRAVEDAD"]

class Personaje(pygame.sprite.Sprite):
    def __init__(self, tipo, x, y,scale, velocidad,municion):
        pygame.sprite.Sprite.__init__(self)
        self.tipo = tipo
        self.vive = True
        self.velocidad = velocidad
        #arma
        self.municion = municion
        self.municion_inicio = municion
        self.cadencia_tiro = 0
        #salto
        self.velocidad_y = 0
        self.salto = False
        self.en_aire = False
        #giro
        self.flip = False
        self.direccion = 1
        #animacion
        self.animacion_lista = []
        self.frame_indice = 0
        self.accion = 0
        self.tiempo_acto = pygame.time.get_ticks()
        lista_temporal = []
        for i in range(5):
            img = pygame.image.load(f'img/{tipo}/parado/{i}.png').convert_alpha()
            img = pygame.transform.scale_by(img, scale)
            lista_temporal.append(img)
        self.animacion_lista.append(lista_temporal)
        
        lista_temporal = []
        for i in range(6):
            img = pygame.image.load(f'img/{tipo}/corriendo/{i}.png')
            img = pygame.transform.scale_by(img, scale)
            lista_temporal.append(img)
        self.animacion_lista.append(lista_temporal)

        self.imagen = self.animacion_lista[self.accion][self.frame_indice]
        self.rect = self.imagen.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.animacion()
        #actualizar cadencia tiro
        if self.cadencia_tiro > 0:
            self.cadencia_tiro -= 1


    def movimiento(self, mov_izquierda, mov_derecha):
        dx = 0
        dy = 0
        if mov_izquierda:
            dx = -self.velocidad
            self.flip = True
            self.direccion = -1
        if mov_derecha:
            dx += self.velocidad
            self.flip = False
            self.direccion = 1
        
        #salto
        if self.salto == True and self.en_aire == False:
            self.velocidad_y = -11
            self.salto = False
            self.en_aire = True
        
        #aplicamos gravedad
        self.velocidad_y += GRAVEDAD
        if self.velocidad_y >10:
            self.velocidad_y
        dy += self.velocidad_y
        
        #chequeamos colision con el suelo
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.en_aire = False
        
        self.rect.x += dx
        self.rect.y += dy

    def disparar(self, Bala, grupo_balas):
        if self.cadencia_tiro == 0 and self.municion > 0:
            self.cadencia_tiro = 20
            bala = Bala(self.rect.centerx + (0.6* self.rect.size[0]*self.direccion), self.rect.centery, self.direccion)
            grupo_balas.add(bala)
            #reducir municion
            self.municion -=1
            print(self.municion)
    
    def animacion(self):
        RETRASO_ANIMACION = 100
        #actualiza imagen dependiento el tempo
        self.imagen = self.animacion_lista[self.accion][self.frame_indice]
        #chequeamos si paso el suficiente tiempo
        if pygame.time.get_ticks() - self.tiempo_acto > RETRASO_ANIMACION:
            self.tiempo_acto = pygame.time.get_ticks()
            self.frame_indice += 1
        #si la animacion es correr volvera al inicio de la secuencia    
        if self.frame_indice >= len(self.animacion_lista[self.accion]):
            self.frame_indice = 0

    def actualizar_accion(self, nueva_accion):
        if nueva_accion != self.accion:
            self.accion = nueva_accion
            self.frame_indice = 0
            self.tiempo_acto = pygame.time.get_ticks()

    def dibujado(self,pantalla):   
        pantalla.blit(pygame.transform.flip(self.imagen, self.flip, False), self.rect)