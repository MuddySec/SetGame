
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
# # Logica tablero y cartas

# %%
def generar_list_cartas():
    global list_cartas 
    list_cartas = []
    #Rellenamos list_cartas con todas las cartas posibles con esas caracteristicas
    for i in range (0, len(Numero)):
        for j in range (0, len(Forma)):
            for k in range (0, len(Color)):
                for l in range (0, len(Relleno)):
                    list_cartas.append(str(Numero[i])+ str(Forma[j])+str(Color[k])+str(Relleno[l]))



# %%
#Comprobar caracteristicas de tres cartas.
#Comprueba si las 3 cartas seleccionadas son set o no.
#Recordemos que un set es un conjunto de 3 cartas donde cada una
#de las 4 características (Numero,Forma,Color y Relleno) son iguales en las 3, o son distintas en las 3.

#En el momento en el que dos cartas tienen una característica igual, pero la tercera carta no, se devuelve False. 
def check(a,b,c):
    #Cada carta tiene 4 caracteristicas = 4 Caracteres, por eso el rango va de 0 a 4
    for i in range (0,4):
        if (a[i] == b[i]):
            if (a[i] != c[i]): 
                return False    
        elif (a[i] == c[i]):
            if (a[i] != b[i]):
                return False 
        elif (c[i] == b[i]):
            if (a[i] != c[i]):
                return False
    return True

# %%
#Genera un tablero de 12 cartas aleatorias de las 81 posibles. No hay repeticiones
def generar_tablero():
    global list_tablero
    list_tablero = []
    list_tablero = random.sample(list_cartas, N_cartas)
    

# %%
def change_tablero(new):
    global list_tablero
    global selected 
    #selected debe ser [] al terminar
    #list_tablero debe ser list_tablero, quitando las seleccionadas y añadiendo las 3 nuevas
    
    list_tablero[selected[0]] = new[0]
    list_tablero[selected[1]] = new[1]
    list_tablero[selected[2]] = new[2]
    

    selected = []
    cartas = draw_table(800,800)
    generar_combinaciones()
    check_table()
    i = 0
    for c in list_tablero:
        deal_cards(c,cartas[i])
        i = i + 1
    return (cartas)




# %%
def change_three(old, new):
    p = True
    if (new[0] == 'NULL'): p=False
    global list_tablero
    global selected
    selected = []
    if p:
        for carta in old:
            selected.append(list_tablero.index(carta))
        list_tablero[selected[0]] = new[0]
        list_tablero[selected[1]] = new[1]
        list_tablero[selected[2]] = new[2]
    else :
        list_tablero[old[0]] = new[0]
        list_tablero[old[1]] = new[1]
        list_tablero[old[2]] = new[2]

    
    
    selected = []
    cartas = draw_table(800,800)
    generar_combinaciones()
    check_table()
    i = 0
    for c in list_tablero:
        deal_cards(c,cartas[i])
        i = i + 1
    return (cartas)


# %%
def eliminar_seleccionadas(eliminar):
    #Elimina las cartas pasadas como parametro de la list_cartas
    global list_cartas
    for carta in eliminar:
        list_cartas.remove(carta)

# %%
def generar_combinaciones():
    #Genera todas las combinaciones posibles de 3 cartes con las 12 cartas presentes en el tablero.
    global combinaciones
    list_tablero_copy = list_tablero.copy()
    combinaciones = []
    for c in list_tablero:
        if (c == "NULL") : 
            list_tablero_copy.remove(c)
    combinaciones = list(combinations(list_tablero_copy, 3))

# %%
def check_table():
    #Comprueba las combinaciones de cartas existentes en la variable combinaciones. 
    #Este variable contiene todas las combinaciones de 3 cartas posibles con las 12 cartas del tablero

    #Almacena en sets las combinaciones validas como set
    global sets
    sets = []
    for i in range (0, len(combinaciones)):
        if check(combinaciones[i][0], combinaciones[i][1],combinaciones[i][2]):
            sets.append(combinaciones[i])

    #Prints para debugging
    print (sets)
    print (len(list_cartas))

# %%
def select_three_list_cartas():
    #Comprueba si la list_cartas tiene alguna carta
    #Si tiene, las devuelve
    #Si no, devuelve NULL
    if (len(list_cartas) > 0) :
        new_three = random.sample(list_cartas, 3)
        return new_three
    else :
        return "NULL"

# %%
def select_three_list_tablero():
    #Devuelve 3 cartas aleatorias de la lista del tablero
    back_three = []
    back_three = random.sample(list_tablero, 3)
    return back_three
    

# %%
def change_lista_cartas(old,new):
    #Recibe 6 cartas. 
    #Las 3 cartas old (que estaban en el tablero) se añaden de nuevo en la lista de cartas
    #Las 3 cartas new (que se acaban de obtener de la lista de cartas) se eliminan de la lista de cartas
    global list_cartas
    
    for carta_new in new:
        list_cartas.remove(carta_new)

    for carta_old in old:
        list_cartas.append(carta_old)

# %%
def deal_cards(c,pos):
    #Si la carta es 'NULL', hace un return
    #Si no, llama a las funciones de dibujar formas con los valores de la carta pasada
    if (c == 'NULL'):
        return
        
    numero = int (c[0])
    forma = c[1]
    color = c[2]
    relleno = c[3]

    match color:
        case "R": color = R
        case "G": color = G
        case "P": color = P
            
    match forma:
        case "W":
            draw_wave(color,numero,relleno,pos)
        case "C":
            draw_circle(color,numero,relleno,pos)
        case "D":
            draw_diamond(color,numero,relleno,pos)   

# %%
def draw_void(pos):
    #NO FUNCIONA

    #DEBERIA DIBUJAR UN CUADRADO DEL COLOR DEL FONDO PARA TAPAR LA CARTA VACIA
    card = pygame.Rect (pos, pos, card_width, card_height)
    card = pygame.draw.rect (window, GREY, card, border_radius=5)

# %%
def check_position(event_pos):
    #Comprueba la posicion en la que se ha clicado
    i = 0
    for c in cartas:
        if c.collidepoint(event_pos):
            #Se ha clicado una carta
            window.blit(text_output_window,(420,830))
            if (i in selected):
                #Si la carta estaba seleccionada, la deselecciona
                selected.remove(i)
                mark_selection(c,(255,255,255),False)
            else :
                #Si no estaba seleccionada, comprueba cuantas habia seleccionadas
                if (len(selected)<3) : 
                    #Si habia menos de 3, la selecciona
                    selected.append(i)
                    mark_selection(c,(255,255,100),False)
                #Si hay 3 seleccionada, no selecciona la clicada e informa de que maximo se pueden seleccionar 3
                else : draw_output_text(text_output_window,"SOLO PUEDES SELECCIONAR 3!",R)
            #Devuelve selected (con las posiciones de 0 a 11 de las cartas seleccionadas)
            return selected
        i = i+1

# %%
def mark_selection(c,color,is_hint):
    new_c = c
    if is_hint : 
        print ("marca")
        new_c= c.inflate(25,25)
    mark = pygame.draw.rect(window, color, new_c, 9, border_radius=5)
    return mark

# %%
def mark_hint(carta,hint):
    if hint:
            return mark_selection (carta,(153,204,255),True)
    else : 
            return mark_selection (carta,GREY,True)


# %%
def show_hint():
    if not sets:
        return "NULL"
        
    card_freq = {}
    for s in sets:
        for c in s:
            if c in card_freq :
                card_freq[c] += 1
            else:
                card_freq[c] = 1
    card_hint = max (card_freq, key=card_freq.get)
    return card_hint



# %%
def tablero():
    
    #CARTAS
    global selected
    selected = []
    cartas = draw_table(800,800)
    generar_tablero()
    generar_combinaciones()
    check_table()
    i = 0
    for c in list_tablero:
        deal_cards(c,cartas[i])
        i = i+1
    return (cartas)

# %% [markdown]
# # Textos y botones

# %%
def draw_button(button,texto):
    pygame.draw.rect(window, WHITE, button, border_radius=4)
    font = pygame.font.Font(None, 36)
    text = font.render(texto, True, (0, 0, 0))
    text_rect = text.get_rect( center = button.center)
    window.blit(text, text_rect) 

# %%
def draw_button_hint(button,hint):
    pygame.draw.rect(window, WHITE, button, border_radius=4)
    font = pygame.font.Font(None, 36)
    if hint:
        color = (0,0,0)
        texto = "Hint : ON"
    else :
        color = (150,150,150)
        texto = "Hint : OFF"
    text = font.render(texto, True, color)
    text_rect = text.get_rect( center = button.center)
    window.blit(text, text_rect)

# %%
def draw_output_text(surface,text,color):
    surface.fill(WHITE)  # Fondo blanco para la ventana
    window.blit(surface, (420, 830))  # Mostrar la superficie del output en la parte inferior

    # Renderizar el texto y ponerlo en la superficie
    font = pygame.font.Font(None, 24)
    text_surface = font.render(text, True, color)

    text_width, text_height = text_surface.get_size()

    center_x = (surface.get_width() - text_width) // 2
    center_y = (surface.get_height() - text_height) // 2

    text_rect = text_surface.get_rect(topleft=(center_x+420, center_y+830))
    window.blit(text_surface, text_rect)  # Posición del texto

# %%
def write_points(surface):
    surface.fill(WHITE)  # Fondo blanco para la ventana
    window.blit(surface, (420, 910))  # Mostrar la superficie del output en la parte inferior

    font = pygame.font.Font(None, 32)
    text = "Points: " + str(points) 
    text_surface = font.render(text, True, (0,0,0))

    text_width, text_height = text_surface.get_size()

    center_x = (surface.get_width() - text_width) // 2
    center_y = (surface.get_height() - text_height) // 2

    text_rect = text_surface.get_rect(topleft=(center_x+420, center_y+910))
    window.blit(text_surface, text_rect)  # Posición del texto

# %% [markdown]
# # GRAFICOS

# %% [markdown]
# ## Cartas y Tablero

# %%
def draw_card (x,y):
    card = pygame.Rect (x, y, card_width, card_height)
    card = pygame.draw.rect (window, WHITE, card, border_radius=5)
    return card

def draw_table(width,height):
    cartas = []
    # Calcula la separación horizontal y vertical
    margen_x = (width - N_columnas * card_width) // (N_columnas + 1)
    margen_y = (height - N_filas * card_height) // (N_filas + 1)
    
    # Dibuja las cartas
    for i in range(0,3):
        for j in range(0,4):
            x = margen_x * (j + 1) + j * card_width
            y = margen_y * (i + 1) + i * card_height
            cartas.append (draw_card(x,y))
    return cartas


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

def get_vertex (r):
    return [(r.centerx, r.top), 
            (r.right, r.centery), 
            (r.centerx, r.bottom), 
            (r.left, r.centery)]


def draw_lines_diamond (diamonds, color):


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



