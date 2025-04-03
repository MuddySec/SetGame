
# %% [markdown]
# ## Circulos

# %%
def draw_circle (color, numero, relleno, carta):
    #carta = 120*184
    #circulo = 60*24

    circle_rect = carta.inflate(-60,-160)
    circulos = []
    radio = int (min (circle_rect.width,circle_rect.height)/2)
    w = 0 if relleno == F else 2  # Define grosor del borde
    offset = 20 if numero == 2 else 40  # Define desplazamiento

    if (numero % 2 == 1): 
        circulos.append (pygame.draw.rect(window, color, circle_rect,width=w, border_radius=radio))

    if (numero > 1): 
        circulos.append (pygame.draw.rect(window, color, circle_rect.move(0,-offset),width=w, border_radius=radio))
        circulos.append (pygame.draw.rect(window, color, circle_rect.move(0,offset),width=w, border_radius=radio))

    if (relleno == S): 
        draw_lines_circle (color,circulos,radio)



def rounded_border_profile(radius, x):
    if abs(x) > radius:
        return None  # Devuelve None si x está fuera del rango del semicírculo

    # Calcula y en función de x en el semicírculo
    return math.sqrt(radius**2 - x**2)

def draw_lines_circle(color, circulos, radio):
    # Esta version no dibuja sobre la ventana. Dibuja las lineas de un circulo
    # sobre una superficie auxiliar y luego dibuja esta en la ventana --> mas eficiente

    surface_lines = pygame.Surface((width, height),pygame.SRCALPHA)

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

### OLD ###
def draw_lines_circle_old(color,circulos,radio): 
    for c in circulos:
        borde_izq = c.left + radio
        borde_dr = c.right - radio

        for x in range (c.left, c.right, 5):
            if x < borde_izq :
                y = rounded_border_profile (radio, borde_izq - x)
                start_pos = (x, c.centery - y)
                end_pos = (x, c.centery + y )
            elif x <= borde_dr :
                start_pos = (x, c.bottom - c.top )
                end_pos = (x, 0)
            else : #x > borde_dr
                y = rounded_border_profile(radio, x - borde_dr)
                start_pos = (x, c.centery - y + 2)
                end_pos = (x, c.centery + y - 2)

            pygame.draw.line(window, color, start_pos, end_pos, 2)



# %% [markdown]
# ## Onda

# %%
#ONDAS 2
def draw_wave_2(movement,wave_rect,relleno,color):
    # Parámetros de la onda senoidal
    amplitud = 8  # Altura de la onda
    frecuencia = 0.09  # Frecuencia de la onda (ajusta para más o menos repeticiones)
    dif = 7

    wave_rect = wave_rect.move(0,movement)
    desfase = wave_rect.centery  # Posición vertical
    r = wave_rect.right
    l = wave_rect.left

    surface_lines = pygame.Surface((width, height), pygame.SRCALPHA)

    #Calcula y dibuja puntos superiores
    points1 = [(x, int(desfase + dif + amplitud * math.sin(frecuencia * (x-l)))) for x in range(l, r)]
    points2 = [(x, (y - 2 * dif)) for (x, y) in points1]

    pygame.draw.lines(surface_lines, color, False, points1 , 2)
    pygame.draw.lines(surface_lines, color, False, points2 , 2)
    pygame.draw.line(surface_lines, color, (points1[0][0],points1[0][1]-1), points2[0], 2)
    pygame.draw.line(surface_lines, color, (points1[-1][0],points1[-1][1]-1), points2[-1],2)


    if relleno in (F, S):
        step = 1 if relleno == F else 5
        for i in range(0, len(points1), step):
            pygame.draw.line(surface_lines, color, points1[i], points2[i], 2)

    window.blit(surface_lines, (0, 0))


def draw_wave (color, numero, relleno, carta):
    wave_rect = carta.inflate (-60,-160) 

    offset = 20 if numero == 2 else 40  # Define desplazamiento
    # Generar puntos usando la función seno
    if (numero % 2 == 1):
        draw_wave_2(0,wave_rect,relleno,color)

    if (numero > 1):
        draw_wave_2(offset,wave_rect,relleno,color)
        draw_wave_2(-offset,wave_rect,relleno,color)

    for movement in ([0] if numero % 2 == 1 else []) + ([-offset, offset] if numero > 1 else []):
        draw_wave_2(movement, wave_rect, relleno, color)

# %% [markdown]
# ## Rombos

# %%
def draw_diamond (color, numero, relleno, carta):
    rombo_rect = carta.inflate (-60,-160)
    diamonds = []

    w = 0 if relleno == F else 2  # Define grosor del borde
    offset = 20 if numero == 2 else 40  # Define desplazamiento

    if (numero % 2 == 1) :
        diamonds.append (pygame.draw.polygon(window, color, get_vertex(rombo_rect), width=w))

    if (numero > 1):      
        diamonds.append (pygame.draw.polygon(window, color, get_vertex(rombo_rect.move(0,-offset)), width=w))
        diamonds.append (pygame.draw.polygon(window, color, get_vertex(rombo_rect.move(0,offset)), width=w))

    if (relleno == S ) : draw_lines_diamond (diamonds,color)
