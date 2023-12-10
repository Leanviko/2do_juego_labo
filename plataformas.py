import pygame 
from personaje import Personaje
from armas import *
from items import *
from informacion import *
from salud import *
import json

with open("variables.json","r") as var:
    variables = json.load(var)

GRAVEDAD = variables["GRAVEDAD"]


ANCHO_PANTALLA = variables["ANCHO_PANTALLA"]
ALTO_PANTALLA = variables["ALTO_PANTALLA"]
FPS = variables["FPS"]
COLOR_FONDO = variables["COLOR_FONDO"]
ROJO = variables["ROJO"]
BLANCO = variables["BLANCO"]

def dibujo_piso():
    pantalla.fill(COLOR_FONDO)
    pygame.draw.line(pantalla, ROJO, (0, 300), (ANCHO_PANTALLA, 300))





pygame.init()
pygame.font.init()
pantalla = pygame.display.set_mode((ANCHO_PANTALLA,ALTO_PANTALLA))
pygame.display.set_caption('2do juego')
reloj = pygame.time.Clock()

#variables juegow
GRAVEDAD = 0.75

#variables jugador
jugador_mov_izquierda = False
jugador_mov_derecha = False
disparar = False
granada = False
granada_fue_lanzada = False



#Grupos
grupo_balas = pygame.sprite.Group()
grupo_granadas = pygame.sprite.Group()
grupo_explosiones = pygame.sprite.Group()
grupo_enemigos = pygame.sprite.Group()
grupo_cajas_items = pygame.sprite.Group()

caja_salud = CajaItem('Salud', 300, 260)
grupo_cajas_items.add(caja_salud)
caja_municion = CajaItem('Municion', 400, 260)
grupo_cajas_items.add(caja_municion)
caja_granada = CajaItem('Granada', 600, 260)
grupo_cajas_items.add(caja_granada)




jugador = Personaje('jugador',200,200,1.7,5,100,25,5)
caja_salud = BarraSalud(10,10,jugador.salud,jugador.salud_max)
enemigo = Personaje('enemigo',420,200,1.7,2,35,25,0)
enemigo2 = Personaje('enemigo',510,200,1.7,2,35,25,0)
grupo_enemigos.add(enemigo)
grupo_enemigos.add(enemigo2)



#* bucle principal -----------------------------
corriendo = True
while corriendo:
    reloj.tick(FPS)
    dibujo_piso()
    
    #mostrar salud/municion/granadas
    caja_salud.dibujar(pantalla, jugador.salud)

    dibujar_texto(pantalla, 'Municion: ', fuente, BLANCO, 10, 35)
    for num_bala in range(jugador.municion):
        pantalla.blit(bala_img,(110+(num_bala * 10),40))
    dibujar_texto(pantalla, 'Granadas: ', fuente, BLANCO, 10, 60)
    for num_granada in range(jugador.granadas):
        pantalla.blit(granada_img,(120+(num_granada * 15),63))
    dibujar_texto(pantalla, f'Salud: {jugador.salud}', fuente, BLANCO, 10, 85)




    jugador.update()
    jugador.dibujado(pantalla)
    
    for enemigo in grupo_enemigos:
        enemigo.ia(pantalla, jugador, Bala, grupo_balas)
        enemigo.update()
        enemigo.dibujado(pantalla)
    

    #Actualizar y dibujar grupos
    grupo_balas.update(jugador,grupo_balas,grupo_enemigos)
    grupo_balas.update(enemigo,grupo_balas,grupo_enemigos)
    grupo_granadas.update(grupo_explosiones,grupo_enemigos,jugador)
    grupo_explosiones.update()
    grupo_cajas_items.update(jugador)
    grupo_balas.draw(pantalla)
    grupo_granadas.draw(pantalla)
    grupo_explosiones.draw(pantalla)
    grupo_cajas_items.draw(pantalla)

    if jugador.vive:
        if disparar:
            jugador.disparar(Bala, grupo_balas)
        elif granada and granada_fue_lanzada == False and jugador.granadas > 0:
            granada = Granada(jugador.rect.centerx + (0.5*jugador.rect.size[0]*jugador.direccion),\
            jugador.rect.top, jugador.direccion)#lanzar granadas
            grupo_granadas.add(granada)
            jugador.granadas -= 1
            granada_fue_lanzada = True
        if jugador.en_aire:
            jugador.actualizar_accion(2) #saltar
        if jugador_mov_izquierda or jugador_mov_derecha:
            jugador.actualizar_accion(1)#correr
        else:
            jugador.actualizar_accion(0)#estar parado
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
            if evento.key == pygame.K_SPACE:   
                disparar = True
            if evento.key == pygame.K_g:   
                granada = True
            if evento.key == pygame.K_w and jugador.vive:
                jugador.salto = True 
            if evento.key == pygame.K_ESCAPE:
                corriendo = False
        
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_a:
                jugador_mov_izquierda = False
            if evento.key == pygame.K_d:   
                jugador_mov_derecha = False
            if evento.key == pygame.K_SPACE:   
                disparar = False
            if evento.key == pygame.K_g:   
                granada = False
                granada_fue_lanzada = False
            
    
    pygame.display.update()