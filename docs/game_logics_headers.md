# Cabeceras de funciones del módulo `game_logics`

## generar_list_cartas()
> Genera y guarda una lista de cartas únicas para comenzar el juego.

## check(card1: tuple, card2: tuple, card3: tuple) -> bool
> Comprueba si tres cartas forman un set válido según las reglas del juego.

## generar_tablero ()
> Añade a la variable global list_tablero 12 cartas aleatorias de list_cartas (combinación de cartas existentes)

## change_tablero(cartas: list, window: pygame.Surface) -> list
> Cambia las cartas mostradas en el tablero según una lista nueva. Devuelve el nuevo tablero y los sets existentes

## change_three(old: list, new: list, windwo: pygame.Surface) -> list
> Sustituye tres cartas del tablero por tres nuevas y devuelve el nuevo tablero y los sets existentes.

## eliminar_seleccionadas(cartas: list)
> Elimina del tablero las cartas seleccionadas (útil tras hacer un set).

## generar_combinaciones() -> list
> Genera todas las combinaciones posibles de 3 cartas con las 12 del tablero

## check_table(combinaciones: list) -> list
> Comprueba las combinaciones de cartas existentes en la variable combinaciones
> Almacena en sets los sets válidos y los devuelve

## select_three_list_cartas() -> list | str
> Selecciona tres cartas de la lista general de cartas. Si no hay suficientes, devuelve "NULL".

## select_three_list_tablero() -> list
> Elige tres cartas del tablero actual (usado al cambiar cartas).

## change_lista_cartas(old: list, new: list)
> Intercambia cartas entre el tablero y la lista general de cartas disponibles.

 ## deal_cards (card: str, posicion: Rect, window: pygame.Surface)
> Si la carta es NULL, no devuelve nada. Si no, llama a la funcion de dibujo de carta correspondiente.

## check_position(pos: tuple, window: pygame.Surface, text_output_window: pygame.Surface, cartas: list) -> list
> Verifica si se ha hecho clic en alguna carta y gestiona la selección.

## mark_selection(marca: tuple, color: tuple, is_hint: bool, window: pygame.Surface) -> Rect
> Marca o desmarca visualmente una selección en el tablero.

## mark_hint(carta: tuple, hint: bool, window: pygame.Surface) -> Rect
> Marca una carta como parte de un set (hint), opcionalmente la dibuja. Devuelve la posición marcada.

## show_hint(sets: list) -> tuple | str
> Muestra una pista de un set disponible. Devuelve la carta más repetida en los sets existentes o "NULL" si no hay.

## tablero(window: pygame.Surface) -> list
> Devuelve la lista de cartas que se colocan en el tablero (12 cartas) y los sets existentes.

## draw_button(boton: pygame.Rect, texto: str, window: pygame.Surface)
> Dibuja un botón con texto sobre el botón dado.

## draw_button_hint(boton: pygame.Rect, hint: bool, window: pygame.Surface)
> Dibuja un botón para el hint, con cambio visual si está activado o desactivado.

## draw_output_text(surface: pygame.Surface, texto: str, color: tuple, window: pygame.Surface)
> Muestra un mensaje de salida en la interfaz con color.

## write_points(surface: pygame.Surface, window: pygame.Surface)
> Escribe el marcador de puntos en la interfaz gráfica.

## draw_card (x: float, y: float, window: pygame.Surface) -> tuple
> Devuelve la carta dibujada (cuadrado blanco)

## draw_table (width: float, height: float, window: pygame.Surface) -> list
> Calcula la posicion de cada carta en el tablero y llama a draw_card para que las dibuje





















