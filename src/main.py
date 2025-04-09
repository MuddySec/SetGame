
# %%
#Imports necesarios para el programa
from itertools import combinations
import random
import math
import pygame
import sys
import tkinter as tk
import threading


# %% [markdown]
# # MAIN

# %%
# Inicializa Pygame
pygame.init()


hint = False
cartas = []
selected = []

#global window
window = pygame.display.set_mode((width, height))


pygame.display.set_caption("Set Game")

#Ventana
window.fill(GREY)




#Surfaces
control_surface = pygame.Surface((730, 180))
control_surface.fill((120,120,120))
window.blit(control_surface, (35, 800))

tablero_surface = pygame.Surface((800,780))
tablero_surface.fill(GREY)
window.blit(tablero_surface,(0,0))


surface_lines = pygame.Surface((60, 24))
surface_lines.fill(R)
window.blit(surface_lines,(100,100))




#Buttons
button_check = pygame.Rect(65,830,150,60)
draw_button(button_check,"Check")

button_change_three = pygame.Rect(235,830,150,60)
draw_button(button_change_three,"Change 3")

button_hint = pygame.Rect(65,910,150,60)
draw_button_hint(button_hint,hint)

button_newgame = pygame.Rect(235,910,150,60)
draw_button(button_newgame,"New Game")

#Textos
text_output_window = pygame.Surface((320,60))
text_output_window.fill((255,255,255))
window.blit(text_output_window,(420,830))

text_points_window = pygame.Surface((320,60))
text_points_window.fill((255,255,255))
window.blit(text_points_window,(420,910))




generar_list_cartas()
cartas = tablero()
eliminar_seleccionadas(list_tablero)

write_points (text_points_window)

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
                    if (check(list_tablero[selected[0]],
                              list_tablero[selected[1]],
                              list_tablero[selected[2]])): 
                        draw_output_text(text_output_window,"SET CORRECTO!",G)
                        points = points + 1
                        write_points(text_points_window)
                        if hint :
                            mark = mark_hint(cartas[list_tablero.index(h)],False)
                            hint = False
                            draw_button_hint(button_hint,hint)
                        new = select_three_list_cartas() 
                        if (new == "NULL"):
                            cartas = change_three(selected,('NULL','NULL','NULL'))
                            draw_output_text(text_output_window,"NO QUEDAN CARTAS!",R)
                        else:
                            eliminar_seleccionadas(new)
                            cartas = change_tablero(new)
                        
                    else : draw_output_text(text_output_window,"ESO NO ES UN SET!",R)
                else : draw_output_text(text_output_window,"LOS SETS SON DE 3 CARTAS!",R)

            #### NEW GAME ####
            if button_newgame.collidepoint(event.pos):
                if hint :
                    mark = mark_hint(cartas[list_tablero.index(h)],False)
                    hint = False
                    draw_button_hint(button_hint,hint)

                
                window.blit(tablero_surface,(0,0))
                window.blit(text_output_window,(420,830))
                generar_list_cartas()
                cartas = tablero()
                eliminar_seleccionadas(list_tablero)
                points = 0
                write_points(text_points_window)
                draw_output_text(text_output_window,"PARTIDA NUEVA",(0,0,0))

                
                
            #### CHANGE THREE ####
            if button_change_three.collidepoint(event.pos):
                
                h = show_hint()
                if hint :
                    mark = mark_hint(cartas[list_tablero.index(h)],False)
                    hint = False
                    draw_button_hint(button_hint,hint)

                if (h == "NULL"):
                    draw_output_text(text_output_window,"NO HABÍA NINGUN SET!",R)
                else : 
                    points = points - 1
                    write_points(text_points_window)
                    draw_output_text(text_output_window,"-1 punto por cambiar cartas",R)


                
                #Debe escoger 3 cartas del tablero, guardarlas de nuevo en la lista de cartas, y sacar 3.
                old_three = select_three_list_tablero()
                new_three = select_three_list_cartas()
                if (new_three == "NULL"):
                    draw_output_text(text_output_window,"NO QUEDAN CARTAS!",R)
                else:
                     #Saca de list_cartas las 3 nuevas cartas. Vuelve a meter las cartas que estaban en el tablero
                    cartas = change_three(old_three,new_three)
                    change_lista_cartas(old_three,new_three)
               

                
                

            #### HINT ####
            if button_hint.collidepoint(event.pos):
                window.blit(text_output_window,(420,830))
                hint = not hint
                draw_button_hint(button_hint,hint)
                if hint : 
                    h = show_hint()
                    if (h == "NULL"):
                        draw_output_text(text_output_window,"NO HAY NINGUN SET!",R)
                    else : 
                        mark = mark_hint(cartas[list_tablero.index(h)],True)
                       
                else: mark_selection(mark,GREY,False)

            #### CLICKS ####
            mouse_buttons = pygame.mouse.get_pressed()  # Obtener estado de los botones
            # Comprobar qué botón fue presionado
            if mouse_buttons[0]:
                check_position(event.pos)

    pygame.display.flip()
pygame.quit()

# %%



