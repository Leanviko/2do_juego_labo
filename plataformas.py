import pygame 
from personaje import Personaje
import json

with open("variables.json","r") as var:
    variables = json.load(var)

GRAVEDAD = variables["GRAVEDAD"]


ANCHO_PANTALLA = variables["ANCHO_PANTALLA"]
ALTO_PANTALLA = variables["ALTO_PANTALLA"]
FPS = variables["FPS"]
COLOR_FONDO = variables["COLOR_FONDO"]
ROJO = variables["ROJO"]

def dibujo_piso():
    pantalla.fill(COLOR_FONDO)
    pygame.draw.line(pantalla, ROJO, (0, 300), (ANCHO_PANTALLA, 300))



pygame.init()
pantalla = pygame.display.set_mode((ANCHO_PANTALLA,ALTO_PANTALLA))
pygame.display.set_caption('2do juego')
reloj = pygame.time.Clock()

#variables juegow
GRAVEDAD = 0.75

#variables jugador
jugador_mov_izquierda = False
jugador_mov_derecha = False


#Grupos
grupo_balas = pygame.sprite.Group()



jugador = Personaje('jugador',200,200,2,5)



#* bucle principal -----------------------------
corriendo = True
while corriendo:
    reloj.tick(FPS)
    dibujo_piso()


    jugador.animacion()
    jugador.dibujado(pantalla)
    if jugador.vive:
        if jugador_mov_izquierda or jugador_mov_derecha:
            jugador.actualizar_accion(1)
        else:
            jugador.actualizar_accion(0)
        jugador.movimiento(jugador_mov_izquierda,jugador_mov_derecha)
    


    for evento in pygame.event.get():
        
        if evento.type == pygame.QUIT:
            corriendo = False
        
        #movimiento
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_a:
                jugador_mov_izquierda = True
            if evento.key == pygame.K_d:   
                jugador_mov_derecha = True
            if evento.key == pygame.K_w and jugador.vive:
                jugador.salto = True 
            if evento.key == pygame.K_ESCAPE:
                corriendo = False
        
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_a:
                jugador_mov_izquierda = False
            if evento.key == pygame.K_d:   
                jugador_mov_derecha = False
            
    
    pygame.display.update()