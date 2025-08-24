import pygame
import config
import game_logics
import game_state

BUTTONS = [
    ("button_check", (65, 830, 150, 60), "Check"),
    ("button_change_three", (235, 830, 150, 60), "Change 3"),
    ("button_hint", (65, 910, 150, 60), "Hint"),
    ("button_newgame", (235, 910, 150, 60), "New Game"),
]

TEXTS = [
    ("text_output_window", (420, 830), (320, 60)),
    ("text_points_window", (420, 910), (320, 60)),
]

def draw_main_window(window, partida):
    ui = {}
    window.fill(config.GREY)
    pygame.display.set_caption("Set Game")

    # --- Superficies ---
    tablero_surface = pygame.Surface((800,780))
    tablero_surface.fill(config.GREY)
    window.blit(tablero_surface,(0,0))

    control_surface = pygame.Surface((730, 180))
    control_surface.fill((120,120,120))
    window.blit(control_surface, (35, 800))
    
    surface_lines = pygame.Surface((60, 24))
    surface_lines.fill(config.R)
    window.blit(surface_lines,(100,100))

    # --- Botones ---
    for key , rect_args, label in BUTTONS:
        ui[key] = pygame.Rect(rect_args)
        if key == "button_hint":
            game_logics.draw_button_hint(ui[key],partida.hint, window)
        else:
            game_logics.draw_button(ui[key], label, window)
    
    # --- Textos ---
    for key, pos, size in TEXTS:
        ui[key] = pygame.Surface(size)
        ui[key].fill((255,255,255))
        window.blit(ui[key], pos)

    return ui

def draw_gameover_screen(partida, window):
#gestion final
    print("gameover")
    x = config.WIDTH//2 - 250
    y = config.HEIGHT//2 - 250

    # Crea una superficie para el fondo del gameover
    gameover_surface = pygame.Surface((config.WIDTH, config.HEIGHT))
    gameover_surface.fill((120,120,120))
    window.blit(gameover_surface, (0, 0))

    # Crea una superficie para el cuadro de texto del gameover
    gameover_surface = pygame.Surface((450, 450))
    gameover_surface.fill((200,200,200))
    window.blit(gameover_surface, (x+25, y+25))

    # --- Definir Textos ---
    texts =  [
        (55, "PARTIDA TERMINADA", (x + 250, y + 75)),
        (30, "No quedan más sets por encontrar", (x + 250, y + 110)),
        (30, f"Sets obtenidos: {partida.points}", (x + 250, y + 175)),
        (30, f"Tiempo total: {partida.minutes:02}:{partida.seconds:02}", (x + 250, y + 200)),
        (30, f"Pistas:  {partida.hint_counts}", (x + 250, y + 225)),
        (30, f"Cambios: {partida.change3_counts}", (x + 250, y + 250)),
        (30, f"Errores: {partida.error_counts}", (x + 250, y + 275)),
        (30, f"Puntos finales: {partida.final_score()}", (x + 250, y + 325)),
    ]

    # --- Dibujar Textos ---
    for size, content, pos in texts:
        font = pygame.font.Font(None, size)
        text_surface = font.render(content, True, config.G)
        text_rect = text_surface.get_rect(center=pos)
        window.blit(text_surface, text_rect.topleft)

    # --- Botón de Reinicio ---
    button_gameover = pygame.Rect(x+150, y+370, 200, 60)
    game_logics.draw_button(button_gameover,"Volver a jugar", window)
    
    return button_gameover