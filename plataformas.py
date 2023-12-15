import pygame 
from personaje import Personaje
from armas import *
from items import *
from informacion import *
from salud import *
from niveles import *
from interfaz import *

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
MAX_NIVELES = variables["MAX_NIVELES"]
BLOQUE_TAMANIO = ALTO_PANTALLA // FILAS




#grados = grados_img_lista[0]


def dibujo_fondo():
    pantalla.fill(COLOR_FONDO)
    ancho_fondos = cielo_img.get_width()
    for i in range(5):
        pantalla.blit(cielo_img,((ancho_fondos* i)-fondo_deslizamiento*0.5,0))
        pantalla.blit(montanias_img,((ancho_fondos* i)-fondo_deslizamiento*0.6,ALTO_PANTALLA - montanias_img.get_height()-300))
        pantalla.blit(pinos1_img,((ancho_fondos* i)-fondo_deslizamiento*0.7,ALTO_PANTALLA - pinos1_img.get_height()-150))
        pantalla.blit(pinos2_img,((ancho_fondos* i)-fondo_deslizamiento*0.8,ALTO_PANTALLA - pinos2_img.get_height()))

#funcion de reiniciar nivel
def borrar_datos_grupos():
    grupo_balas.empty()
    grupo_granadas.empty()
    grupo_explosiones.empty()
    grupo_enemigos.empty()
    grupo_cajas_items.empty()
    grupo_decoracion.empty()
    grupo_agua.empty()
    grupo_salidas.empty()


pygame.init()
pygame.font.init()
pantalla = pygame.display.set_mode((ANCHO_PANTALLA,ALTO_PANTALLA))
pygame.display.set_caption('2do juego')
reloj = pygame.time.Clock()


volumenes = {"volumen_musica" :4,"volumen_sonido" : 4,"presionado" :False}

estrellas = {"nivel_1" :1,"nivel_2" :1,"nivel_3" :2,"nivel_4" :3,} 

deslizamiento_pantalla = 0
fondo_deslizamiento = 0
nivel = 1

presionado = False

#variables jugador
jugador_mov_izquierda = False
jugador_mov_derecha = False
disparar = False
granada = False
granada_fue_lanzada = False

#crear botones
boton_inicio = Boton(ANCHO_PANTALLA//2,ALTO_PANTALLA//2-70, inicio_img, 1)
boton_salida = Boton(ANCHO_PANTALLA//2,ALTO_PANTALLA//2 + 70, salid_img, 1)
boton_reinicio = Boton(ANCHO_PANTALLA//2, ALTO_PANTALLA//2, reiniciar_img, 2)

#Grupos
grupo_balas = pygame.sprite.Group()
grupo_granadas = pygame.sprite.Group()
grupo_explosiones = pygame.sprite.Group()
grupo_enemigos = pygame.sprite.Group()
grupo_cajas_items = pygame.sprite.Group()
grupo_decoracion = pygame.sprite.Group()
grupo_agua = pygame.sprite.Group()
grupo_salidas = pygame.sprite.Group()
grupo_plataforma = pygame.sprite.Group()




#carga de niveles
data_niveles = cargar_niveles(FILAS,COLUMNAS,nivel)

mundo = Mundo()
jugador, caja_salud = mundo.procesamiento_datos(data_niveles,grupo_enemigos,grupo_cajas_items,grupo_decoracion, grupo_agua, grupo_salidas)





estados = {"iniciar_juego" : False,"partida_perdida" : False,"pausa_juego" :False,"configuracion_pantalla" : False,"ranking_pantalla" : False, "seleccion_nivel_pantalla" : False,"menu_pausa_principal" : True,"presionado" :False}

#boton_pausa = Boton(ANCHO_PANTALLA//2,ALTO_PANTALLA//2,)






#* bucle principal -----------------------------
corriendo = True
while corriendo:
    pos_x,pos_y = pygame.mouse.get_pos()
    print(nivel)
    


    if estados["iniciar_juego"] == False:
        pantalla.fill(COLOR_FONDO)
        if boton_inicio.dibujo(pantalla):
            print("inicio")
            estados["iniciar_juego"] = True
        if boton_salida.dibujo(pantalla):
            print("salida")
            estados["corriendo"] = False
    else:
        
        
        if estados["partida_perdida"]:
            pass
        else:
            if estados["pausa_juego"]:

                if estados["menu_pausa_principal"]:
                    funcion_menu_pausa(pantalla, menu_pausa, ANCHO_PANTALLA//2, ALTO_PANTALLA//2,pos_x,pos_y, estados)

                if estados["configuracion_pantalla"] == True:
                        menu_configuracion(pantalla, menu_configuracion_img, ANCHO_PANTALLA//2, ALTO_PANTALLA//2,pos_x,pos_y, estados,grados_img_lista,volumenes)
                if estados["seleccion_nivel_pantalla"]:
                    
                    nivel_nuevo = menu_niveles(pantalla, menu_niveles_img, ANCHO_PANTALLA//2, ALTO_PANTALLA//2, pos_x, pos_y, estados, estrellas_img_lista, estrellas, nivel)

                    if nivel != nivel_nuevo:
                        nivel = nivel_nuevo
                        fondo_deslizamiento = 0
                        borrar_datos_grupos()

                        if nivel <= MAX_NIVELES:
                            data_niveles = cargar_niveles(FILAS,COLUMNAS,nivel)
                            mundo = Mundo()
                            jugador, caja_salud = mundo.procesamiento_datos(data_niveles,grupo_enemigos,grupo_cajas_items,grupo_decoracion, grupo_agua,grupo_salidas)
                    
                if estados["ranking_pantalla"]:
                    pass
            else:
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
                    enemigo.ia(jugador, Bala, grupo_balas, mundo.lista_obstaculos,ANCHO_PANTALLA, DESLIZAR_HORIZONTAL,deslizamiento_pantalla,fondo_deslizamiento,mundo.largo_nivel,grupo_agua,grupo_salidas,pantalla,grupo_plataforma)
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
                grupo_plataforma.update(deslizamiento_pantalla,pantalla,jugador)
                grupo_balas.draw(pantalla)
                grupo_granadas.draw(pantalla)
                grupo_explosiones.draw(pantalla)
                grupo_cajas_items.draw(pantalla)
                grupo_decoracion.draw(pantalla)
                grupo_agua.draw(pantalla)
                grupo_salidas.draw(pantalla)
                grupo_plataforma.draw(pantalla)

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
                    deslizamiento_pantalla, nivel_completo = jugador.movimiento(jugador_mov_izquierda,jugador_mov_derecha, mundo.lista_obstaculos, ANCHO_PANTALLA, DESLIZAR_HORIZONTAL,fondo_deslizamiento,mundo.largo_nivel,grupo_agua,grupo_salidas,grupo_plataforma)

                    fondo_deslizamiento -= deslizamiento_pantalla
                    
                    if nivel_completo:
                        nivel += 1
                        fondo_deslizamiento = 0
                        borrar_datos_grupos()

                        if nivel <= MAX_NIVELES:
                            data_niveles = cargar_niveles(FILAS,COLUMNAS,nivel)
                            mundo = Mundo()
                            jugador, caja_salud = mundo.procesamiento_datos(data_niveles,grupo_enemigos,grupo_cajas_items,grupo_decoracion, grupo_agua,grupo_salidas)

                else:
                    deslizamiento_pantalla = 0
                    if boton_reinicio.dibujo(pantalla):
                        fondo_deslizamiento = 0

                        #borramos y volvemos a cargar el nivel
                        borrar_datos_grupos()
                        data_niveles = cargar_niveles(FILAS,COLUMNAS,nivel)
                        mundo = Mundo()
                        jugador, caja_salud = mundo.procesamiento_datos(data_niveles,grupo_enemigos,grupo_cajas_items,grupo_decoracion, grupo_agua,grupo_salidas)




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
            if evento.key == pygame.K_p:
                    if estados["pausa_juego"] == False:
                        estados["pausa_juego"] = True
                        estados["seleccion_nivel_pantalla"] = False
                        estados["menu_pausa_principal"] = True
                    else:
                        estados["pausa_juego"] = False
                        estados["menu_pausa_principal"] = False
                        estados["seleccion_nivel_pantalla"] = False
                        estados["configuracion_pantalla"] = False
            if evento.key == pygame.K_n:   
                nivel_nuevo +=1
        
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