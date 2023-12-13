import pygame
import json

pygame.font.init()

with open("variables.json","r") as var:
    variables = json.load(var)
ALTO_PANTALLA = variables["ALTO_PANTALLA"]
FILAS = variables["FILAS"]
BLOQUE_TAMANIO = ALTO_PANTALLA // FILAS


#fondo de pantalla
pinos1_img = pygame.image.load('img/fondo/pinos1.png')
pinos2_img = pygame.image.load('img/fondo/pinos2.png')
montanias_img = pygame.image.load('img/fondo/montanias.png')
cielo_img = pygame.image.load('img/fondo/cielo.png')

#botones imagenes
inicio_img = pygame.image.load('img/botones/inicio_btn.png')
reiniciar_img = pygame.image.load('img/botones/reiniciar_btn.png')
salid_img = pygame.image.load('img/botones/salidas_btn.png')

#armas imagenes
bala_img = pygame.image.load('img/iconos/bala.png')
granada_img =pygame.image.load('img/iconos/granada.png')
caja_salud_img =pygame.image.load('img/iconos/caja_salud.png')
caja_municion_img =pygame.image.load('img/iconos/caja_municion.png')
caja_granada_img =pygame.image.load('img/iconos/caja_granada.png')

#bloques
BLOQUES_TIPOS= 22
bloques_img_lista = []
for i in range(BLOQUES_TIPOS):
    img = pygame.image.load(f'img/bloques/{i}.png')
    img = pygame.transform.scale(img,(BLOQUE_TAMANIO,BLOQUE_TAMANIO))
    bloques_img_lista.append(img)

#fuentes
fuente = pygame.font.SysFont('Futura', 30)

#diccionario cajas
item_cajas = {
    'Salud':caja_salud_img,
    'Municion':caja_municion_img,
    'Granada':caja_granada_img,
}