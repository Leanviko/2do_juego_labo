import pygame 
from personaje import Personaje 


ANCHO_PANTALLA = 800
ALTO_PANTALLA = int(ANCHO_PANTALLA *0.8)
FPS = 60
COLOR_FONDO = (144,201,120)

pantalla = pygame.display.set_mode((ANCHO_PANTALLA,ALTO_PANTALLA))
pygame.display.set_caption('2do juego')
reloj = pygame.time.Clock()

jugador_mov_izquierda = False
jugador_mov_derecha = False


jugador = Personaje('jugador',200,200,2,5)



#* bucle principal -----------------------------
corriendo = True
while corriendo:
    reloj.tick(FPS)
    pantalla.fill(COLOR_FONDO)


    jugador.animacion()
    jugador.dibujado(pantalla)
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
            if evento.key == pygame.K_ESCAPE:
                corriendo = False
        
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_a:
                jugador_mov_izquierda = False
            if evento.key == pygame.K_d:   
                jugador_mov_derecha = False
            
    
    pygame.display.update()