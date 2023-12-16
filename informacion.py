import pygame
from assets import *


def dibujar_texto(pantalla, texto, fuente, texto_color, x, y):
    img = fuente.render(texto, True, texto_color)
    pantalla.blit(img, (x, y))

def temporizador_pantalla(pantalla, fuente, tiempo_total,estados,img,x,y,datos_pantalla):
        
        segundos = pygame.time.get_ticks()//1000

        
        tiempo_restante = max(tiempo_total - int(segundos), 0)


        
        temporizador_text = fuente.render(f"Tiempo",True,(0,0,0))
        temporizador_rect = temporizador_text.get_rect(center =(400,50))
        centesimas_text = fuente.render(f"{segundos}",True,(0,0,0))
        centesimas_rect = centesimas_text.get_rect(center =(400,70))

        if segundos >= 60 :
            estados["partida_perdida"] = True
            game_over_img = img
            game_over_rect = game_over_img.get_rect()
            game_over_rect.center = (x,y)
            pantalla.blit(game_over_img, game_over_rect)


        pantalla.blit(temporizador_text,temporizador_rect)
        pantalla.blit(centesimas_text,centesimas_rect)