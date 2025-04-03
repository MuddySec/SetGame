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


