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
        self.velocidad_salto = 0
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
        self.ancho = self.imagen.get_width()
        self.alto = self.imagen.get_height()

    def update(self):
        self.animacion()
        self.chequear_vida()

        #actualizar cadencia tiro
        if self.cadencia_tiro > 0:
            self.cadencia_tiro -= 1


    def movimiento(self, mov_izquierda, mov_derecha, lista_obstaculos, ANCHO_PANTALLA, DESLIZAR_HORIZONTAL, fondo_deslizamiento,largo_nivel,grupo_agua):

        deslizamiento_pantalla = 0
        dx = 0
        dy = 0

        if mov_izquierda:
            dx = -self.velocidad
            self.flip = True
            self.direccion = -1
        elif mov_derecha:
            dx = self.velocidad
            self.flip = False
            self.direccion = 1


        
        #print(f'dx: {dx}')

        #salto
        if self.salto == True and self.en_aire == False:
            self.velocidad_salto = -11
            self.salto = False
            self.en_aire = True
            
        
        #aplicamos gravedad
        self.velocidad_salto += GRAVEDAD
        if self.velocidad_salto >10:
            self.velocidad_salto
        
        dy += self.velocidad_salto

        
        
        #chequeamos colision con el suelo
        for bloque in lista_obstaculos:
            #la colision agrego dx, dy para determinar la colision antes de que ocurra. dx,dy cambian antes de cambiar la pos del rectangulo
            if bloque[1].colliderect(self.rect.x + dx, self.rect.y, self.ancho, self.alto):
                dx = 0 # dejara de moverse en x

                #si la IA colisiona con un muro cambia de dir
                if self.tipo == "enemigo":
                    self.direccion *= -1
                    self.contador_movimiento = 0

            if bloque[1].colliderect(self.rect.x, self.rect.y + dy, self.ancho, self.alto):
#---> no entiendo   #chekeamos si esta comenzando a saltar
                if self.velocidad_salto < 0:
                    self.velocidad_salto = 0
                    dy = bloque[1].bottom - self.rect.top
                #chequeamos cuando cae
                elif self.velocidad_salto >= 0:
                    self.velocidad_salto = 0
                    self.en_aire = False
                    dy = bloque[1].top - self.rect.bottom

        #colision jugador con el agua radiactiva
        if pygame.sprite.spritecollide(self, grupo_agua, False):
            self.salud -= 15

        #chequear si el jugador cae del mapa
        if self.rect.top > ALTO_PANTALLA:
            self.salud = 0
            self.kill()

        
        #limito el movimiento del personaje en los bordes del nivel
        if self.tipo == "jugador":
            if self.rect.left + dx < 0 or self.rect.right + dx > ANCHO_PANTALLA:
                dx = 0
        
        self.rect.x += dx
        self.rect.y += int(dy)
        #actualizo el paneo dependiendo la posicion
#Estudiar--->        
        if self.tipo == "jugador":
            if self.salud > 0:
                if (self.rect.right > ANCHO_PANTALLA - DESLIZAR_HORIZONTAL and fondo_deslizamiento<(largo_nivel*BLOQUE_TAMANIO)-ANCHO_PANTALLA) or (self.rect.left < DESLIZAR_HORIZONTAL and fondo_deslizamiento> abs(dx)):
                    self.rect.x -= dx
                    deslizamiento_pantalla = -dx
            else:
                deslizamiento_pantalla = 0

        return deslizamiento_pantalla


    def disparar(self, Bala, grupo_balas):
        if self.cadencia_tiro == 0 and self.municion > 0:
            self.cadencia_tiro = 20
            bala = Bala(self.rect.centerx + (0.8* self.rect.size[0]*self.direccion), self.rect.centery, self.direccion)
            grupo_balas.add(bala)
            #reducir municion
            self.municion -=1

    def ia(self, jugador, Bala, grupo_balas,lista_obstaculos, ANCHO_PANTALLA, DESLIZAR_HORIZONTAL,deslizamiento_pantalla,fondo_deslizamiento,largo_nivel,grupo_agua):
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

                    self.movimiento(ia_mover_izquierda, ia_mover_derecha,lista_obstaculos, ANCHO_PANTALLA, DESLIZAR_HORIZONTAL,fondo_deslizamiento,largo_nivel,grupo_agua)
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
        
        self.rect.x += deslizamiento_pantalla


    
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