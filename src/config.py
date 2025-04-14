
#congig.py
# Este archivo contiene la configuracion del juego SET

from typing import Final

# Variables

#TABLERO
#N_columnas -> numero de columnas del tablero
#N_filas -> numero de filas del tablero
#N_cartas -> numero total de cartas en el tablero
N_COLUMNAS : Final = 4
N_FILAS : Final = 3
N_CARTAS : Final = 12


#Declaracion caracteristicas
#Posibles numeros de las cartas. 1,2 o 3.
NUMERO : Final = [1,2,3]
#Posibles formas de las cartas. Circle, Diamond o Wave
FORMA : Final = ['C', 'D', 'W']
#Posibles colores de las cartas. Red, Green o Purple
COLOR : Final = ['R', 'G', 'P']
#Posibles rellenos de las cartas. Full, Stripped o Void
RELLENO : Final = ['F', 'S', 'V']

# Definir colores
R : Final = (240, 0, 0)
G : Final = (0, 220, 0)
P : Final = (102, 0, 102)
WHITE : Final = (255, 255, 255)
GREY : Final = (64, 64, 64)

# Definir rellenos
F = "F"
S = "S"
V = "V"

#Configuracion de la ventana
# Configuración de la ventana
WIDTH : Final = 800
HEIGHT : Final = 1000
CARD_WIDTH : Final = 120
CARD_HEIGHT : Final = 184  #120*1.5454

# Puntos acumulados en una partida
points = 0



#numero posicional de las cartas seleccionadas por el usuario. 
#Entre 0 y 11. 
#Máximo se permite seleccionar 3 cartas
global selected
selected = []

# Total de cartas:
# Con estas caracteristicas, hay un total de 3⁴ = 3*3*3*3 = 81 cartas
global list_cartas
list_cartas = []
