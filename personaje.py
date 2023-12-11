import pygame
import json
import os
import random
from assets import *


with open("variables.json","r") as var:
    variables = json.load(var)

GRAVEDAD = variables["GRAVEDAD"]
ROJO = variables["ROJO"]

class Personaje(pygame.sprite.Sprite):
    def __init__(self, tipo, x, y, escala, velocidad, salud, municion, granadas):
        pygame.sprite.Sprite.__init__(self)
        self.tipo = tipo
        self.vive = True
        self.velocidad = velocidad
        self.salud = salud
        self.salud_max = salud
        #arma
        self.municion = municion
        self.municion_inicio = municion
        self.cadencia_tiro = 0
        self.granadas = granadas
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
        
        #variables para ia
        self.contador_movimiento = 0
        self.pausa_movimiento = False
        self.contador_pausa_movimiento = 0
        self.vision = pygame.Rect(0,0,150,20)
        
        #cargando todos los tipos de imagen
        animacion_tipos =['parado','corriendo','salto','muerte']
        for animacion in animacion_tipos:
            #resetea la lista temporal de imagenese
            lista_temporal = []
            num_de_frames = len(os.listdir(f'img/{tipo}/{animacion}'))
            for i in range(num_de_frames):
                img = pygame.image.load(f'img/{tipo}/{animacion}/{i}.png').convert_alpha()
                img = pygame.transform.scale_by(img, escala)
                lista_temporal.append(img)
            self.animacion_lista.append(lista_temporal)
        

        self.imagen = self.animacion_lista[self.accion][self.frame_indice]
        self.rect = self.imagen.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.animacion()
        self.chequear_vida()
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
            #self.actualizar_accion(1)#correr
        if mov_derecha:
            dx += self.velocidad
            self.flip = False
            self.direccion = 1
            #self.actualizar_accion(1)
        
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
            bala = Bala(self.rect.centerx + (0.8* self.rect.size[0]*self.direccion), self.rect.centery, self.direccion)
            grupo_balas.add(bala)
            #reducir municion
            self.municion -=1

    def ia(self, pantalla, jugador, Bala, grupo_balas):
        if self.vive and jugador.vive:

            #detenerse aleatoriamente
            if self.pausa_movimiento == False and random.randint(1,200) == 1:
                self.actualizar_accion(0)#parado
                self.pausa_movimiento = True
                self.contador_pausa_movimiento = 50
            #deternerse y disparar cuando ven al jugador
            if self.vision.colliderect(jugador.rect):
                self.actualizar_accion(0)#parado
                self.disparar(Bala, grupo_balas)
            else:
                #asocio flip() con la dirección de movimiento
                if self.pausa_movimiento == False:  
                    if self.direccion == 1:
                        ia_mover_derecha = True
                    else:
                        ia_mover_derecha = False
                    
                    #evitamos que la ia quiera moverse a ambos lados
                    ia_mover_izquierda = not ia_mover_derecha

                    self.movimiento(ia_mover_izquierda, ia_mover_derecha)
                    self.actualizar_accion(1)#correr
                    self.contador_movimiento += 1 #pasos hasta que de la vuelta

                    #actualizar vision de los enemigos
                    self.vision.center = (self.rect.centerx + 75 * self.direccion, self.rect.centery)
                    #pygame.draw.rect(pantalla, ROJO, self.vision)

                    if self.contador_movimiento > BLOQUE_TAMANIO:
                        self.direccion *= -1
                        self.contador_movimiento = 0
                else:
                    self.contador_pausa_movimiento -= 1
                    if self.contador_pausa_movimiento <= 0:
                        self.pausa_movimiento = False


    
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
            #En el caso de la muerte se detiene en el ultimo frame
            if self.accion == 3:
                self.frame_indice = len(self.animacion_lista[self.accion])-1
            else:
                self.frame_indice = 0

    def actualizar_accion(self, nueva_accion):
        if nueva_accion != self.accion:
            self.accion = nueva_accion
            self.frame_indice = 0
            self.tiempo_acto = pygame.time.get_ticks()

    def chequear_vida(self):
        if self.salud <= 0:
            self.salud = 0
            self.velocidad = 0
            self.vive = False
            self.actualizar_accion(3)

    def dibujado(self,pantalla):   
        pantalla.blit(pygame.transform.flip(self.imagen, self.flip, False), self.rect)