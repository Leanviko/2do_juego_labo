import pygame
import csv
from assets import *
from personaje import *
from salud import *
from items import *


def cargar_niveles(FILAS,COLUMNAS,nivel):
    data_niveles = []

    for fila in range(FILAS):
        f = [-1]* COLUMNAS #llenamos por defecto con -1
        data_niveles.append(f)
    #carga del archivo de nivel
    with open(f'nivel{nivel}_data.csv', newline='') as csvfile:
        lectura = csv.reader(csvfile, delimiter=',')
        for x, fila in enumerate(lectura):
            for y, bloque in enumerate(fila):
                data_niveles[x][y] = int(bloque) #el numero del archivo se asigna a la posicion de la lista del juego
    
    return data_niveles

    #print(data_niveles)


class Mundo():
    def __init__(self):
        self.lista_obstaculos = []

    def procesamiento_datos(self, datos, grupo_enemigos, grupo_cajas_items,grupo_decoracion, grupo_agua,grupo_salidas):
        self.largo_nivel = len(datos[0])#datos[0]:cantidad de columnas
        for y, fila in enumerate(datos):
            for x, bloque in enumerate(fila):
                if bloque >= 0:
                    img = bloques_img_lista[bloque] #importado de assets
                    img_rect = img.get_rect()
                    img_rect.x = x*BLOQUE_TAMANIO
                    img_rect.y = y*BLOQUE_TAMANIO
                    bloque_data = (img, img_rect)

                    if bloque >=0 and bloque <= 8:#bloques de terreno
                        self.lista_obstaculos.append(bloque_data)
                    elif bloque >= 9 and bloque <=10:
                        #agua
                        agua = Agua(img, x*BLOQUE_TAMANIO, y*BLOQUE_TAMANIO)
                        grupo_agua.add(agua)
                    elif bloque >= 11 and bloque <= 14:
                        #decoracion
                        decoracion = Decoracion(img, x*BLOQUE_TAMANIO, y*BLOQUE_TAMANIO)
                        grupo_decoracion.add(decoracion)
                    elif bloque == 15: #jugador
                        jugador = Personaje('jugador', x*BLOQUE_TAMANIO, y*BLOQUE_TAMANIO,1.7,5,100,25,5)
                        caja_salud = BarraSalud(10,10,jugador.salud,jugador.salud_max)
                    elif bloque == 16:
                        enemigo = Personaje('enemigo',x*BLOQUE_TAMANIO, y*BLOQUE_TAMANIO,1.7,2,35,25,0)
                        grupo_enemigos.add(enemigo)
                    elif bloque == 17:
                        caja_municion = CajaItem('Municion', x*BLOQUE_TAMANIO, y*BLOQUE_TAMANIO)
                        grupo_cajas_items.add(caja_municion)
                    elif bloque == 18:
                        caja_granada = CajaItem('Granada', x*BLOQUE_TAMANIO, y*BLOQUE_TAMANIO)
                        grupo_cajas_items.add(caja_granada)
                    elif bloque == 19:
                        caja_salud = CajaItem('Salud', x*BLOQUE_TAMANIO, y*BLOQUE_TAMANIO)
                        grupo_cajas_items.add(caja_salud)
                    elif bloque == 20:
                        salida = Salida(img, x*BLOQUE_TAMANIO, y*BLOQUE_TAMANIO)
                        grupo_salidas.add(salida)
                    elif bloque == 21: #nuevo
                        enemigo2 = Personaje('jefe',x*BLOQUE_TAMANIO, y*BLOQUE_TAMANIO,3,3,300,25,0)
                        grupo_enemigos.add(enemigo2)
                    # elif bloque == 22:
                    #     plataforma = Plataforma(img, x*BLOQUE_TAMANIO, y*BLOQUE_TAMANIO)
                    #     grupo_plataforma.add(plataforma)
                        
        return jugador, caja_salud


    def dibujado(self,pantalla, deslizamiento_pantalla):
        for bloque in self.lista_obstaculos:
            bloque[1][0] += deslizamiento_pantalla
            pantalla.blit(bloque[0],bloque[1])

class Decoracion(pygame.sprite.Sprite):
    def __init__(self, imagen, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = imagen
        self.rect = self.image.get_rect()
        self.rect.midtop = (x+BLOQUE_TAMANIO//2, y+(BLOQUE_TAMANIO - self.image.get_height()))
    
    def update(self,deslizamiento_pantalla):
        self.rect.x += deslizamiento_pantalla

class Agua(pygame.sprite.Sprite):
    def __init__(self, imagen, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = imagen
        self.rect = self.image.get_rect()
        self.rect.midtop = (x+BLOQUE_TAMANIO//2, y+(BLOQUE_TAMANIO - self.image.get_height()))
    
    def update(self,deslizamiento_pantalla):
        self.rect.x += deslizamiento_pantalla

class Salida(pygame.sprite.Sprite):
    def __init__(self, imagen, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = imagen
        self.rect = self.image.get_rect()
        self.rect.midtop = (x+BLOQUE_TAMANIO//2, y+(BLOQUE_TAMANIO - self.image.get_height()))
    
    def update(self,deslizamiento_pantalla):
        self.rect.x += deslizamiento_pantalla

# class Plataforma(pygame.sprite.Sprite):
#     def __init__(self, imagen, x, y):
#         pygame.sprite.Sprite.__init__(self)
#         self.image = imagen
#         self.image = pygame.transform.scale(self.image,(self.image.get_width()*4,self.image.get_height()))
#         self.rect = self.image.get_rect()
#         self.rect.center = (x+BLOQUE_TAMANIO//2, y+(BLOQUE_TAMANIO - self.image.get_height()))
    
#     def update(self,deslizamiento_pantalla,pantalla,jugador):
#         self.rect.x += deslizamiento_pantalla
#         pantalla.blit(self.image, self.rect)
#         pygame.draw.rect(pantalla,ROJO,self.rect,2)

#         # if self.rect.top.colliderect(jugador.rect.bottom):
#         #     jugador.rect.bottom = self.rect.top

