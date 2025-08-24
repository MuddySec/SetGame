
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
import game_renderer

def restart_program():
    """
    Utilizada para reiniciar el programa completo tras finalizar la partida.
    Abre un nuevo proceso de Python para ejecutar el script actual 
    y cierra el proceso actual.
    """
    python = sys.executable
    script = os.path.abspath(sys.argv[0])  # Ruta completa del script actual
    subprocess.Popen([python, script])
    os._exit(0)                            # Termina el proceso actual.

# --- Código principal del programa ---
# Inicializa Pygame
pygame.init()

# Ventana Pygame
window = pygame.display.set_mode((config.WIDTH, config.HEIGHT))

# Inicializa la partida
partida = game_logics.new_game()

running = True

# Dibuja la ventana principal del juego y la ui 
ui = game_renderer.draw_main_window(window,partida)

# Inicializamos la gestión del tiempo
elapsed_time = partida.elapsed_time + ((pygame.time.get_ticks() - partida.start_ticks)) //  1000
partida.minutes = elapsed_time // 60
partida.seconds = elapsed_time % 60

# Inicializamos el tablero
cartas, sets, selected, list_tablero = game_logics.init_tablero(partida.list_cartas, window)
partida.cartas = cartas
partida.sets = sets
partida.selected = selected
partida.list_tablero = list_tablero
partida.list_cartas = game_logics.eliminar_seleccionadas(partida.list_tablero, partida.list_cartas)

# Actualizamos la UI
game_logics.write_points (ui ["text_points_window"], window, partida.points, partida.minutes, partida.seconds)

# Bucle principal que gestiona los eventos
while running:
    # Si la partida no ha acabado, actualizamos el temporizador y lo mostramos
    if (not partida.ended):
        elapsed_time = partida.elapsed_time + ((pygame.time.get_ticks() - partida.start_ticks)) //  1000
        partida.minutes = elapsed_time // 60
        partida.seconds = elapsed_time % 60
        game_logics.write_points (ui ["text_points_window"], window, partida.points, partida.minutes, partida.seconds)

    
    for event in pygame.event.get():
        # Si la partida no ha acabado, gestionamos los eventos
        if (not partida.ended):

            # Se activa cuando se presiona un botón del ratón
            if event.type == pygame.MOUSEBUTTONDOWN:  
                
                # --- CHECK ---
                if ui["button_check"].collidepoint(event.pos):
                    partida, button_gameover = game_logics.handle_check(partida, window, ui)
                # --- NEW GAME ---
                if ui["button_newgame"].collidepoint(event.pos):
                    partida = game_logics.handle_newgame(partida, window, ui)
                # --- CHANGE THREE ---
                if ui["button_change_three"].collidepoint(event.pos):
                    partida = game_logics.handle_change_three(partida, window, ui)
                # --- HINT ---
                if ui["button_hint"].collidepoint(event.pos):
                    partida = game_logics.handle_hint(partida, window, ui)

                # --- CLICKS ---
                mouse_buttons = pygame.mouse.get_pressed()
                if mouse_buttons[0]:
                    # Si no ha terminado la partida, comprobamos la posición
                    if not partida.ended:
                        partida.selected = game_logics.check_position(event.pos, window, ui["text_output_window"], partida.list_tablero, partida.cartas, partida.selected)
                    
            # Gestión de teclas. Uso para debugging
            if event.type == pygame.KEYDOWN:
                # --- GAME OVER ---
                if event.key == pygame.K_e:
                    button_gameover = game_renderer.draw_gameover_screen(partida, window)
                    partida.ended = True
                # --- GUARDAR ESTADO ---
                if event.key == pygame.K_s:
                    partida.save()
                    game_logics.draw_output_text(ui["text_output_window"],"ESTADO GUARDADO",(0,0,0), window)
                # --- CARGAR ESTADO ---
                if event.key == pygame.K_l: #Load estado
                    # Guardamos la marca anterior para desmarcarla
                    previous_mark = partida.mark
                    if (previous_mark is not None) : 
                        game_logics.mark_selection(previous_mark,config.GREY,False, window)     

                    # Cargamos el estado guardado
                    partida = game_state.GameState.load()
                    partida.start_ticks = pygame.time.get_ticks()  # Reiniciar el tiempo
                    partida.cartas = game_logics.draw_table(800,800, window)

                    game_logics.write_points(ui["text_points_window"], window, partida.points, partida.minutes, partida.seconds)
                    game_logics.draw_tablero(partida.list_tablero,partida.cartas, window)

                    # Recuperar cartas seleccionadas
                    for idx in partida.selected:
                        game_logics.mark_selection(partida.cartas[idx],(255,255,100), False, window)

                    game_logics.draw_output_text(ui["text_output_window"],"ESTADO CARGADO",(0,0,0), window)

                    # Recuperar pista seleccionada
                    if partida.hint : 
                        partida.hint_card = game_logics.show_hint(partida.sets)
                        if (partida.hint_card is None):
                            game_logics.draw_output_text(ui["text_output_window"],"NO HAY NINGUN SET!",config.R, window)
                        else : 
                            partida.mark = game_logics.mark_hint(partida.cartas[partida.list_tablero.index(partida.hint_card)],True, window)
                        game_logics.draw_button_hint(ui["button_hint"],partida.hint, window)
                    else:
                        if (partida.mark is not None) : game_logics.mark_selection(partida.mark,config.GREY,False, window)     

        # Si la partida ha acabado, solo hay que gestionar el fin de la partida
        else:
            # Comprobamos si se ha hecho clic en el botón de reinicio
            if event.type == pygame.MOUSEBUTTONDOWN:  
                mouse_buttons = pygame.mouse.get_pressed()
                if mouse_buttons[0]:
                    if button_gameover.collidepoint(event.pos):
                        restart_program()
        if event.type == pygame.QUIT: running = False
    pygame.display.flip()
pygame.quit()


