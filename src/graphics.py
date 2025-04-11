
import pygame
import math
import config

# ## Circulos

def draw_circle (color, numero, relleno, carta, window):
    #carta = 120*184
    #circulo = 60*24

    circle_rect = carta.inflate(-60,-160)
    circulos = []
    radio = int (min (circle_rect.width,circle_rect.height)/2)
    w = 0 if relleno == config.F else 2  # Define grosor del borde
    offset = 20 if numero == 2 else 40  # Define desplazamiento

    if (numero % 2 == 1): 
        circulos.append (pygame.draw.rect(window, color, circle_rect,width=w, border_radius=radio))

    if (numero > 1): 
        circulos.append (pygame.draw.rect(window, color, circle_rect.move(0,-offset),width=w, border_radius=radio))
        circulos.append (pygame.draw.rect(window, color, circle_rect.move(0,offset),width=w, border_radius=radio))

    if (relleno == S): 
        draw_lines_circle (color,circulos,radio, window)

def rounded_border_profile(radius, x):
    if abs(x) > radius:
        return None  # Devuelve None si x está fuera del rango del semicírculo

    # Calcula y en función de x en el semicírculo
    return math.sqrt(radius**2 - x**2)

def draw_lines_circle(color, circulos, radio, window):
    # Esta version no dibuja sobre la ventana. Dibuja las lineas de un circulo
    # sobre una superficie auxiliar y luego dibuja esta en la ventana --> mas eficiente

    surface_lines = pygame.Surface((config.width, config.height),pygame.SRCALPHA)

    for c in circulos:
        borde_izq = c.left + radio
        borde_dr = c.right - radio
        centro_v = c.centery - c.top

        for x in range(c.left, c.right, 5):
            if x < borde_izq:
                y = rounded_border_profile(radio, borde_izq - x)
                start_pos = (x - c.left, centro_v - y)
                end_pos = (x - c.left, centro_v + y)
            elif x <= borde_dr:
                start_pos = (x - c.left, 0 )
                end_pos = (x - c.left, c.bottom - c.top - 3)
            else:
                y = rounded_border_profile(radio, x - borde_dr)
                start_pos = (x - c.left, centro_v - y + 2)
                end_pos = (x - c.left, centro_v + y - 2)
            pygame.draw.line(surface_lines, color , start_pos, end_pos, 2)

        window.blit(surface_lines, (c.left,c.top))

# ## Onda
def draw_wave_2(movement,wave_rect,relleno,color, window):
    # Parámetros de la onda senoidal
    amplitud = 8  # Altura de la onda
    frecuencia = 0.09  # Frecuencia de la onda (ajusta para más o menos repeticiones)
    dif = 7

    wave_rect = wave_rect.move(0,movement)
    desfase = wave_rect.centery  # Posición vertical
    r = wave_rect.right
    l = wave_rect.left

    surface_lines = pygame.Surface((config.width, config.height), pygame.SRCALPHA)

    #Calcula y dibuja puntos superiores
    points1 = [(x, int(desfase + dif + amplitud * math.sin(frecuencia * (x-l)))) for x in range(l, r)]
    points2 = [(x, (y - 2 * dif)) for (x, y) in points1]

    pygame.draw.lines(surface_lines, color, False, points1 , 2)
    pygame.draw.lines(surface_lines, color, False, points2 , 2)
    pygame.draw.line(surface_lines, color, (points1[0][0],points1[0][1]-1), points2[0], 2)
    pygame.draw.line(surface_lines, color, (points1[-1][0],points1[-1][1]-1), points2[-1],2)

    if relleno in (config.F, config.S):
        step = 1 if relleno == config.F else 5
        for i in range(0, len(points1), step):
            pygame.draw.line(surface_lines, color, points1[i], points2[i], 2)

    window.blit(surface_lines, (0, 0))

def draw_wave (color, numero, relleno, carta, window):
    wave_rect = carta.inflate (-60,-160) 

    offset = 20 if numero == 2 else 40  # Define desplazamiento
    # Generar puntos usando la función seno
    if (numero % 2 == 1):
        draw_wave_2(0,wave_rect,relleno,color, window)

    if (numero > 1):
        draw_wave_2(offset,wave_rect,relleno,color, window)
        draw_wave_2(-offset,wave_rect,relleno,color, window)

    for movement in ([0] if numero % 2 == 1 else []) + ([-offset, offset] if numero > 1 else []):
        draw_wave_2(movement, wave_rect, relleno, color, window)

# ## Rombos
def draw_diamond (color, numero, relleno, carta, window):
    rombo_rect = carta.inflate (-60,-160)
    diamonds = []

    w = 0 if relleno == F else 2  # Define grosor del borde
    offset = 20 if numero == 2 else 40  # Define desplazamiento

    if (numero % 2 == 1) :
        diamonds.append (pygame.draw.polygon(window, color, get_vertex(rombo_rect), width=w))

    if (numero > 1):      
        diamonds.append (pygame.draw.polygon(window, color, get_vertex(rombo_rect.move(0,-offset)), width=w))
        diamonds.append (pygame.draw.polygon(window, color, get_vertex(rombo_rect.move(0,offset)), width=w))

    if (relleno == config.S ) : draw_lines_diamond (diamonds,color, window)

def get_vertex (r):
    return [(r.centerx, r.top), 
            (r.right, r.centery), 
            (r.centerx, r.bottom), 
            (r.left, r.centery)]

def draw_lines_diamond (diamonds, color, window):
    for d in diamonds:
        m = ((d.height)/2)/((d.width)/2)

        surface_lines = pygame.Surface((d.width, d.height),pygame.SRCALPHA)
        #A todo se le resta d.left y d.top para conseguir las coordenadas relativas.

        #Linea central
        pygame.draw.line(surface_lines, color, (d.centerx - 1 - d.left,1), (d.centerx-1 - d.left, d.bottom - 1 - d.top), 2)

        #Lineas izq
        for x in range (d.centerx-1, d.left,-5):
            desfase = (x - d.left) * m
            start_pos = (x - d.left , d.centery + desfase - 1 -d.top)
            end_pos = (x - d.left, d.centery - desfase + 1 -d.top)
            pygame.draw.line(surface_lines, color, start_pos, end_pos, 2)
        #Lineas der
        for x in range (d.centerx-1,d.right,5):
            desfase = (d.right - x) * m
            start_pos = (x - d.left, d.centery + desfase - 1 - d.top)
            end_pos = (x -d.left, d.centery - desfase + 1 - d.top)
            pygame.draw.line(surface_lines, color, start_pos, end_pos, 2)
        
        window.blit(surface_lines, (d.left,d.top))