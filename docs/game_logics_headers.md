# Cabeceras de funciones del módulo `game_logics`

## generar_list_cartas()
> Genera y guarda una lista de cartas únicas para comenzar el juego.

## tablero() -> list
> Devuelve la lista de cartas que se colocan en el tablero (12 cartas).

## eliminar_seleccionadas(cartas: list)
> Elimina del tablero las cartas seleccionadas (útil tras hacer un set).

## select_three_list_cartas() -> list | str
> Selecciona tres cartas de la lista general de cartas. Si no hay suficientes, devuelve "NULL".

## select_three_list_tablero() -> list
> Elige tres cartas del tablero actual (usado al cambiar cartas).

## change_three(old: list, new: list) -> list
> Sustituye tres cartas del tablero por tres nuevas y devuelve el nuevo tablero.

## change_tablero(cartas: list) -> list
> Cambia las cartas mostradas en el tablero según una lista nueva.

## change_lista_cartas(old: list, new: list)
> Intercambia cartas entre el tablero y la lista general de cartas disponibles.

## check(card1: tuple, card2: tuple, card3: tuple) -> bool
> Comprueba si tres cartas forman un set válido según las reglas del juego.

## show_hint() -> tuple | str
> Muestra una pista de un set disponible. Devuelve una carta de un set o "NULL" si no hay.

## mark_hint(carta: tuple, draw: bool) -> tuple
> Marca una carta como parte de un set (hint), opcionalmente la dibuja. Devuelve la posición marcada.

## draw_button(boton: pygame.Rect, texto: str)
> Dibuja un botón con texto sobre el botón dado.

## draw_button_hint(boton: pygame.Rect, hint: bool)
> Dibuja un botón para el hint, con cambio visual si está activado o desactivado.

## draw_output_text(surface: pygame.Surface, texto: str, color: tuple)
> Muestra un mensaje de salida en la interfaz con color.

## write_points(surface: pygame.Surface)
> Escribe el marcador de puntos en la interfaz gráfica.

## mark_selection(marca: tuple, color: tuple, draw: bool)
> Marca o desmarca visualmente una selección en el tablero.

## check_position(pos: tuple)
> Verifica si se ha hecho clic en alguna carta y gestiona la selección.