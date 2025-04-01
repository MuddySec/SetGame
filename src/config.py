#congig.py
# Este archivo contiene la configuracion del juego SET
# Variables

#TABLERO
#N_columnas -> numero de columnas del tablero
#N_filas -> numero de filas del tablero
#N_cartas -> numero total de cartas en el tablero
global N_columnas, N_filas, N_cartas
N_columnas = 4
N_filas = 3
N_cartas = 12

#numero posicional de las cartas seleccionadas por el usuario. 
#Entre 0 y 11. 
#Máximo se permite seleccionar 3 cartas
global selected
selected = []

# Total de cartas:
# Con estas caracteristicas, hay un total de 3⁴ = 3*3*3*3 = 81 cartas
global list_cartas
list_cartas = []

#Declaracion caracteristicas
global Numero, Forma, Color, Relleno
#Posibles numeros de las cartas. 1,2 o 3.
Numero = [1,2,3]
#Posibles formas de las cartas. Circle, Diamond o Wave
Forma = ['C', 'D', 'W']
#Posibles colores de las cartas. Red, Green o Purple
Color = ['R', 'G', 'P']
#Posibles rellenos de las cartas. Full, Stripped o Void
Relleno = ['F', 'S', 'V']


# Definir colores
global R, G, P, WHITE, GREY
R = (240, 0, 0)
G = (0, 220, 0)
P = (102, 0, 102)
WHITE = (255, 255, 255)
GREY = (64, 64, 64)

# Definir rellenos
F = "F"
S = "S"
V = "V"


#Configuracion de la ventana
# Configuración de la ventana
global width, height, card_width, card_height,points

width = 800
height = 1000
card_width = 120
card_height = 184 #120*1.5454
points = 0
