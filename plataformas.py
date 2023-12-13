import pygame 
from personaje import Personaje
from armas import *
from items import *
from informacion import *
from salud import *
from niveles import *
import json
import csv

with open("variables.json","r") as var:
    variables = json.load(var)



ANCHO_PANTALLA = variables["ANCHO_PANTALLA"]
ALTO_PANTALLA = variables["ALTO_PANTALLA"]
GRAVEDAD = variables["GRAVEDAD"]
DESLIZAR_HORIZONTAL = variables["DESLIZAR_HORIZONTAL"]
FPS = variables["FPS"]
COLOR_FONDO = variables["COLOR_FONDO"]
ROJO = variables["ROJO"]
BLANCO = variables["BLANCO"]
COLUMNAS = variables["COLUMNAS"]
FILAS = variables["FILAS"]
BLOQUE_TAMANIO = ALTO_PANTALLA // FILAS

deslizamiento_pantalla = 0
fondo_deslizamiento = 0
nivel = 1

def dibujo_fondo():
    pantalla.fill(COLOR_FONDO)
    ancho_fondos = cielo_img.get_width()
    for i in range(5):
        pantalla.blit(cielo_img,((ancho_fondos* i)-fondo_deslizamiento*0.5,0))
        pantalla.blit(montanias_img,((ancho_fondos* i)-fondo_deslizamiento*0.6,ALTO_PANTALLA - montanias_img.get_height()-300))
        pantalla.blit(pinos1_img,((ancho_fondos* i)-fondo_deslizamiento*0.7,ALTO_PANTALLA - pinos1_img.get_height()-150))
        pantalla.blit(pinos2_img,((ancho_fondos* i)-fondo_deslizamiento*0.8,ALTO_PANTALLA - pinos2_img.get_height()))
    



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
grupo_decoracion = pygame.sprite.Group()
grupo_agua = pygame.sprite.Group()
grupo_salidas = pygame.sprite.Group()




#carga de niveles
data_niveles = cargar_niveles(FILAS,COLUMNAS,nivel)

mundo = Mundo()
jugador, caja_salud = mundo.procesamiento_datos(data_niveles,grupo_enemigos,grupo_cajas_items,grupo_decoracion, grupo_agua,grupo_salidas)




#* bucle principal -----------------------------
corriendo = True
while corriendo:
    

    dibujo_fondo()
    #dibujar nivel
    mundo.dibujado(pantalla, deslizamiento_pantalla)
    
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
        enemigo.ia(jugador, Bala, grupo_balas, mundo.lista_obstaculos,ANCHO_PANTALLA, DESLIZAR_HORIZONTAL,deslizamiento_pantalla,fondo_deslizamiento,mundo.largo_nivel)
        enemigo.update()
        enemigo.dibujado(pantalla)
    

    #Actualizar y dibujar grupos
    grupo_balas.update(jugador,grupo_balas,grupo_enemigos,mundo.lista_obstaculos,deslizamiento_pantalla)
    grupo_balas.update(enemigo,grupo_balas,grupo_enemigos,mundo.lista_obstaculos,deslizamiento_pantalla)
    grupo_granadas.update(grupo_explosiones,grupo_enemigos,jugador,mundo.lista_obstaculos,deslizamiento_pantalla)
    grupo_explosiones.update(deslizamiento_pantalla)
    grupo_cajas_items.update(jugador, deslizamiento_pantalla)
    grupo_decoracion.update(deslizamiento_pantalla)
    grupo_agua.update(deslizamiento_pantalla)
    grupo_salidas.update(deslizamiento_pantalla)
    grupo_balas.draw(pantalla)
    grupo_granadas.draw(pantalla)
    grupo_explosiones.draw(pantalla)
    grupo_cajas_items.draw(pantalla)
    grupo_decoracion.draw(pantalla)
    grupo_agua.draw(pantalla)
    grupo_salidas.draw(pantalla)

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
        deslizamiento_pantalla = jugador.movimiento(jugador_mov_izquierda,jugador_mov_derecha, mundo.lista_obstaculos, ANCHO_PANTALLA, DESLIZAR_HORIZONTAL,fondo_deslizamiento,mundo.largo_nivel)
        fondo_deslizamiento -= deslizamiento_pantalla

        print(jugador.rect.y)
    


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
    reloj.tick(FPS)