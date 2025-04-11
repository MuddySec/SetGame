
# %%
#Imports necesarios para el programa
from itertools import combinations
import random
import math
import pygame
import sys
import tkinter as tk
import game_logics
import config


# Inicializa Pygame
pygame.init()

hint = False
cartas = []
selected = []

#global window
window = pygame.display.set_mode((config.width, config.height))

pygame.display.set_caption("Set Game")

#Ventana
window.fill(config.GREY)

#Surfaces
control_surface = pygame.Surface((730, 180))
control_surface.fill((120,120,120))
window.blit(control_surface, (35, 800))

tablero_surface = pygame.Surface((800,780))
tablero_surface.fill(config.GREY)
window.blit(tablero_surface,(0,0))

surface_lines = pygame.Surface((60, 24))
surface_lines.fill(R)
window.blit(surface_lines,(100,100))

#Buttons
button_check = pygame.Rect(65,830,150,60)
game_logics.draw_button(button_check,"Check", window)

button_change_three = pygame.Rect(235,830,150,60)
game_logics.draw_button(button_change_three,"Change 3", window)

button_hint = pygame.Rect(65,910,150,60)
game_logics.draw_button_hint(button_hint,hint, window)

button_newgame = pygame.Rect(235,910,150,60)
game_logics.draw_button(button_newgame,"New Game", window)

#Textos
text_output_window = pygame.Surface((320,60))
text_output_window.fill((255,255,255))
window.blit(text_output_window,(420,830))

text_points_window = pygame.Surface((320,60))
text_points_window.fill((255,255,255))
window.blit(text_points_window,(420,910))

game_logics.generar_list_cartas()
cartas = game_logics.tablero(window)
game_logics.eliminar_seleccionadas(config.list_tablero)

game_logics.write_points (text_points_window, window)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
        if event.type == pygame.MOUSEBUTTONDOWN:  # Se activa cuando se presiona un botón del ratón

            ##### CHECk ####
            if button_check.collidepoint(event.pos):
                window.blit(text_output_window,(420,830))
                if (len(selected)==3) :
                    if (game_logics.check(config.list_tablero[selected[0]],
                              config.list_tablero[selected[1]],
                              config.list_tablero[selected[2]])): 
                        game_logics.draw_output_text(text_output_window,"SET CORRECTO!",config.G, window)
                        points = points + 1
                        game_logics.write_points(text_points_window, window)
                        if hint :
                            mark = game_logics.mark_hint(cartas[config.list_tablero.index(h)],False)
                            hint = False
                            game_logics.draw_button_hint(button_hint,hint, window)
                        new = game_logics.select_three_list_cartas() 
                        if (new == "NULL"):
                            cartas = game_logics.change_three(selected,('NULL','NULL','NULL'), window)
                            game_logics.draw_output_text(text_output_window,"NO QUEDAN CARTAS!",config.R, window)
                        else:
                            game_logics.eliminar_seleccionadas(new)
                            cartas = game_logics.change_tablero(new, window)
                        
                    else : game_logics.draw_output_text(text_output_window,"ESO NO ES UN SET!",config.R, window)
                else : game_logics.draw_output_text(text_output_window,"LOS SETS SON DE 3 CARTAS!",config.R, window)

            #### NEW GAME ####
            if button_newgame.collidepoint(event.pos):
                if hint :
                    mark = game_logics.mark_hint(cartas[config.list_tablero.index(h)],False)
                    hint = False
                    game_logics.draw_button_hint(button_hint,hint, window)

                window.blit(tablero_surface,(0,0))
                window.blit(text_output_window,(420,830))
                game_logics.generar_list_cartas()
                cartas = game_logics.tablero(window)
                game_logics.eliminar_seleccionadas(config.list_tablero)
                points = 0
                game_logics.write_points(text_points_window, window)
                game_logics.draw_output_text(text_output_window,"PARTIDA NUEVA",(0,0,0), window)

            #### CHANGE THREE ####
            if button_change_three.collidepoint(event.pos):
                
                h = game_logics.show_hint()
                if hint :
                    mark = game_logics.mark_hint(cartas[config.list_tablero.index(h)],False)
                    hint = False
                    game_logics.draw_button_hint(button_hint,hint, window)

                if (h == "NULL"):
                    game_logics.draw_output_text(text_output_window,"NO HABÍA NINGUN SET!",config.R, window)
                else : 
                    points = points - 1
                    game_logics.write_points(text_points_window, window)
                    game_logics.draw_output_text(text_output_window,"-1 punto por cambiar cartas",config.R, window)

                #Debe escoger 3 cartas del tablero, guardarlas de nuevo en la lista de cartas, y sacar 3.
                old_three = game_logics.select_three_list_tablero()
                new_three = game_logics.select_three_list_cartas()
                if (new_three == "NULL"):
                    game_logics.draw_output_text(text_output_window,"NO QUEDAN CARTAS!",config.R, window)
                else:
                     #Saca de list_cartas las 3 nuevas cartas. Vuelve a meter las cartas que estaban en el tablero
                    cartas = game_logics.change_three(old_three,new_three, window)
                    game_logics.change_lista_cartas(old_three,new_three)
               

            #### HINT ####
            if button_hint.collidepoint(event.pos):
                window.blit(text_output_window,(420,830))
                hint = not hint
                game_logics.draw_button_hint(button_hint,hint, window)
                if hint : 
                    h = game_logics.show_hint()
                    if (h == "NULL"):
                        game_logics.draw_output_text(text_output_window,"NO HAY NINGUN SET!",config.R, window)
                    else : 
                        mark = game_logics.mark_hint(cartas[config.list_tablero.index(h)],True)
                       
                else: game_logics.mark_selection(mark,config.GREY,False, window)

            #### CLICKS ####
            mouse_buttons = pygame.mouse.get_pressed()  # Obtener estado de los botones
            # Comprobar qué botón fue presionado
            if mouse_buttons[0]:
                game_logics.check_position(event.pos, window, text_output_window, cartas)

    pygame.display.flip()
pygame.quit()