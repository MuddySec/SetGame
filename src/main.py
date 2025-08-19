
# %%
#Imports necesarios para el programa
import pygame

import pickle
import sys
import os
import subprocess

import game_logics
import config
import game_state

def restart_program():
    print ("restart")
    python = sys.executable
    script = os.path.abspath(sys.argv[0])        # Ruta completa del script actual
    print (script)
    subprocess.Popen([python, script])
    os._exit(0)                                 # Termina el proceso actual



# Inicializa Pygame
pygame.init()


#global window
window = pygame.display.set_mode((config.WIDTH, config.HEIGHT))

pygame.display.set_caption("Set Game")
partida = game_logics.new_game()
running = True
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
surface_lines.fill(config.R)
window.blit(surface_lines,(100,100))

#Buttons
button_check = pygame.Rect(65,830,150,60)
game_logics.draw_button(button_check,"Check", window)

button_change_three = pygame.Rect(235,830,150,60)
game_logics.draw_button(button_change_three,"Change 3", window)

button_hint = pygame.Rect(65,910,150,60)
game_logics.draw_button_hint(button_hint,partida.hint, window)

button_newgame = pygame.Rect(235,910,150,60)
game_logics.draw_button(button_newgame,"New Game", window)

#Textos
text_output_window = pygame.Surface((320,60))
text_output_window.fill((255,255,255))
window.blit(text_output_window,(420,830))

text_points_window = pygame.Surface((320,60))
text_points_window.fill((255,255,255))
window.blit(text_points_window,(420,910))

elapsed_time = (pygame.time.get_ticks() - partida.time) //  1000
partida.minutes = elapsed_time // 60
partida.seconds = elapsed_time % 60
game_logics.write_points (text_points_window, window, partida.points, partida.minutes, partida.seconds)
ret = game_logics.init_tablero(partida.list_cartas, window)
partida.cartas = ret[0]
partida.sets = ret[1]
partida.selected = ret [2]
partida.list_tablero = ret[3]
partida.list_cartas = game_logics.eliminar_seleccionadas(partida.list_tablero, partida.list_cartas)

while running:
    if (not partida.ended):
        elapsed_time = (pygame.time.get_ticks() - partida.time) //  1000
        partida.minutes = elapsed_time // 60
        partida.seconds = elapsed_time % 60
        game_logics.write_points (text_points_window, window, partida.points, partida.minutes, partida.seconds)
    for event in pygame.event.get():
        if (not partida.ended):
            if event.type == pygame.QUIT:
                running = False
        
            if event.type == pygame.MOUSEBUTTONDOWN:  # Se activa cuando se presiona un botón del ratón

                ##### CHECk ####
                if button_check.collidepoint(event.pos):
                    window.blit(text_output_window,(420,830))
                    if (len(partida.selected)==3) :
                        if (game_logics.check(partida.list_tablero[partida.selected[0]],
                                partida.list_tablero[partida.selected[1]],
                                partida.list_tablero[partida.selected[2]])): 
                            game_logics.draw_output_text(text_output_window,"SET CORRECTO!",config.G, window)
                            partida.points = partida.points + 1
                            game_logics.write_points(text_points_window, window, partida.points, partida.minutes, partida.seconds)
                            if partida.hint :
                                partida.hint = False
                                game_logics.draw_button_hint(button_hint,partida.hint, window)
                                if (partida.hint_card is not FileNotFoundError): #realmente este caso no se puede dar, porque si hay un set, hint_card no es None
                                    partida.mark = game_logics.mark_hint(partida.cartas[partida.list_tablero.index(h)],False,window)
                            new = game_logics.select_three_list_cartas(partida.list_cartas)

                            if (new == "NULL"):
                                ret = game_logics.change_three(partida.selected, ('NULL','NULL','NULL'), partida.selected, partida.list_tablero, window)
                                partida.cartas = ret[0]
                                partida.sets = ret[1]
                                partida.selected = ret[2]
                                partida.list_tablero = ret[3]
                                game_logics.draw_output_text(text_output_window,"NO QUEDAN CARTAS!",config.R, window)
                            else:
                                partida.list_cartas = game_logics.eliminar_seleccionadas(new, partida.list_cartas)
                                ret = game_logics.change_tablero(new, partida.selected, partida.list_tablero, window)
                                partida.cartas = ret[0]
                                partida.sets = ret[1]
                                partida.selected = ret[2]
                                partida.list_tablero = ret[3]

                                print ("Cartas en la baraja restantes:", partida.list_cartas.__len__())
                            if (partida.list_cartas.__len__() + 12 < 21):
                                combinaciones_restantes = game_logics.generar_combinaciones(partida.list_tablero+partida.list_cartas)  
                                sets_still = game_logics.check_table (combinaciones_restantes)  
                                if len(sets_still) == 0:
                                    print ("NO QUEDAN SETS POSIBLES!")
                                    button_gameover = game_logics.load_end(partida, window)
                                    partida.ended = True
                        else : 
                            game_logics.draw_output_text(text_output_window,"ESO NO ES UN SET!",config.R, window)
                            partida.error_counts += 1
                    else : game_logics.draw_output_text(text_output_window,"LOS SETS SON DE 3 CARTAS!",config.R, window)

                #### NEW GAME ####
                if button_newgame.collidepoint(event.pos):
                    if partida.hint :
                        partida.hint = False
                        game_logics.draw_button_hint(button_hint,partida.hint, window)
                        if (h!= "NULL"):
                            partida.mark = game_logics.mark_hint(partida.cartas[partida.list_tablero.index(h)],False,window)
                     
                    partida = game_logics.new_game()
                    ret = game_logics.init_tablero(partida.list_cartas, window)
                    partida.cartas, partida.sets, partida.selected, partida.list_tablero = ret
                    partida.list_cartas = game_logics.eliminar_seleccionadas(partida.list_tablero, partida.list_cartas) 

                    game_logics.write_points(text_points_window, window, partida.points, partida.minutes, partida.seconds)
                    game_logics.draw_output_text(text_output_window,"PARTIDA NUEVA",(0,0,0), window)

                #### CHANGE THREE ####
                if button_change_three.collidepoint(event.pos):
                    partida.hint_card = game_logics.show_hint(partida.sets)
                    if partida.hint :
                        partida.hint = False
                        game_logics.draw_button_hint(button_hint,partida.hint, window)
                        if (partida.hint_card is not None):
                            partida.mark = game_logics.mark_hint(partida.cartas[partida.list_tablero.index(partida.hint_card)],False,window)
                    
                    if (partida.hint_card is None):
                        game_logics.draw_output_text(text_output_window,"NO HABÍA NINGUN SET!",config.R, window)
                    else : 
                        partida.change3_counts += 1
                        game_logics.draw_output_text(text_output_window,"Cambio usado",config.R, window)

                    #Debe escoger 3 cartas del tablero, guardarlas de nuevo en la lista de cartas, y sacar 3.
                    old_three = game_logics.select_three_list_tablero(partida.list_tablero)
                    new_three = game_logics.select_three_list_cartas(partida.list_cartas)
                    if (new_three == "NULL"):
                        game_logics.draw_output_text(text_output_window,"NO QUEDAN CARTAS!",config.R, window)
                    else:
                        #Saca de list_cartas las 3 nuevas cartas. Vuelve a meter las cartas que estaban en el tablero
                        ret = game_logics.change_three(old_three,new_three,partida.selected, partida.list_tablero, window)
                        partida.cartas = ret[0]
                        partida.sets = ret[1]
                        partida.selected = ret[2]
                        partida.list_tablero = ret[3]
                        partida.list_cartas = game_logics.change_lista_cartas(old_three,new_three, partida.list_cartas)
                    partida.hint_card = game_logics.show_hint(partida.sets)


                #### HINT ####
                if button_hint.collidepoint(event.pos):
                    window.blit(text_output_window,(420,830))
                    partida.hint = not partida.hint
                    game_logics.draw_button_hint(button_hint,partida.hint, window)
                    if partida.hint : 
                        partida.hint_card = game_logics.show_hint(partida.sets)
                        if (partida.hint_card is None):
                            game_logics.draw_output_text(text_output_window,"NO HAY NINGUN SET!",config.R, window)
                        else : 
                            partida.mark = game_logics.mark_hint(partida.cartas[partida.list_tablero.index(partida.hint_card)],True, window)
                            partida.hint_counts += 1
                        
                    else: game_logics.mark_selection(partida.mark,config.GREY,False, window)

                #### CLICKS ####
                mouse_buttons = pygame.mouse.get_pressed()  # Obtener estado de los botones
                # Comprobar qué botón fue presionado
                if mouse_buttons[0]:
                    partida.selected = game_logics.check_position(event.pos, window, text_output_window, partida.cartas, partida.selected)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    button_gameover = game_logics.load_end(partida, window)
                    partida.ended = True       
                if event.key == pygame.K_s: #Save estado
                    partida.save()
                    game_logics.draw_output_text(text_output_window,"ESTADO GUARDADO",(0,0,0), window)

                if event.key == pygame.K_l: #Load estado
                    partida = game_state.GameState.load()
                    
                    partida.cartas = game_logics.draw_table(800,800, window)

                    game_logics.write_points(text_points_window, window, partida.points, partida.minutes, partida.seconds)
                    game_logics.draw_tablero(partida.list_tablero,partida.cartas, window)
                    for idx in partida.selected:
                        game_logics.mark_selection(partida.cartas[idx],(255,255,100), False, window)
                    game_logics.draw_output_text(text_output_window,"ESTADO CARGADO",(0,0,0), window)
                    if partida.hint : 
                        partida.hint_card = game_logics.show_hint(partida.sets)
                        if (partida.hint_card is None):
                            game_logics.draw_output_text(text_output_window,"NO HAY NINGUN SET!",config.R, window)
                        else : 
                            partida.mark = game_logics.mark_hint(partida.cartas[partida.list_tablero.index(partida.hint_card)],True, window)

                    else:
                        game_logics.mark_selection(partida.mark,config.GREY,False, window)
                    

        else:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:  # Se activa cuando se presiona un botón del ratón
                mouse_buttons = pygame.mouse.get_pressed()  # Obtener estado de los botones
                if mouse_buttons[0]:
                    if button_gameover.collidepoint(event.pos):
                        restart_program()
    pygame.display.flip()
pygame.quit()


