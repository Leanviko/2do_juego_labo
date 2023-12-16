import pygame
import json

pygame.font.init()
pygame.mixer.init()

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

#menus
menu_pausa = pygame.image.load('img/menus/pausa.png')
menu_configuracion_img = pygame.image.load('img/menus/configuracion.png')
menu_niveles_img = pygame.image.load('img/menus/niveles.png')

#menus
game_over_img = pygame.image.load('img/mensajes/game_over.png')

#fuentes
fuente = pygame.font.Font(None, 36)

# Tiempo total del temporizador (60 segundos)
tiempo_total = 60
tiempo_actual = tiempo_total

#bloques
BLOQUES_TIPOS= 23
bloques_img_lista = []
for i in range(BLOQUES_TIPOS):
    img = pygame.image.load(f'img/bloques/{i}.png')
    img = pygame.transform.scale(img,(BLOQUE_TAMANIO,BLOQUE_TAMANIO))
    bloques_img_lista.append(img)

#fuentes
fuente = pygame.font.SysFont('Futura', 30)

#sonidos
salto = pygame.mixer.Sound('Sonidos/salto.wav')
disparo = pygame.mixer.Sound('Sonidos/disparo.wav')
sonidos ={"salto":salto, "disparo":disparo}

#diccionario cajas
item_cajas = {
    'Salud':caja_salud_img,
    'Municion':caja_municion_img,
    'Granada':caja_granada_img,
}

grados_img_lista = []
for i in range(8):
    img = pygame.image.load(f'img/menus/grados/{i}.png')
    grados_img_lista.append(img)


estrellas_img_lista = []
for i in range(4):
    img = pygame.image.load(f'img/menus/estrellas/{i}_estrellas.png')
    ancho = img.get_width()
    alto = img.get_height()
    img = pygame.transform.scale(img,(ancho*0.95,alto*0.7))
    estrellas_img_lista.append(img)

volumenes = {"volumen_musica" :4,"volumen_sonido" : 4,"presionado" :False}

estrellas = {"nivel_1" :1,"nivel_2" :1,"nivel_3" :2,"nivel_4" :3,} 