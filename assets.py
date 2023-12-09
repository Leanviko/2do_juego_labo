import pygame
pygame.font.init()

bala_img = pygame.image.load('img/iconos/bala.png')
granada_img =pygame.image.load('img/iconos/granada.png')
caja_salud_img =pygame.image.load('img/iconos/caja_salud.png')
caja_municion_img =pygame.image.load('img/iconos/caja_municion.png')
caja_granada_img =pygame.image.load('img/iconos/caja_granada.png')

#fuentes
fuente = pygame.font.SysFont('Futura', 30)

#diccionario cajas
item_cajas = {
    'Salud':caja_salud_img,
    'Municion':caja_municion_img,
    'Granada':caja_granada_img,
}