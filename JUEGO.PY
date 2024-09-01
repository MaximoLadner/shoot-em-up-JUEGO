import pygame
import random
import math
from pygame import mixer

# Inicializar pygame
pygame.init()

# Crear la pantalla
pantalla = pygame.display.set_mode((800, 600))

# Título e icono
pygame.display.set_caption("Invasion Espacial")
icono = pygame.image.load("ovnis.png")
pygame.display.set_icon(icono)

# Música de fondo
# mixer.music.load("musica_fondo.mp3")
# mixer.music.play(-1)

# Variables Jugador
img_jugador = pygame.image.load("transbordador-espacial.png")
jugador_x = 368
jugador_y = 500
jugador_x_cambio = 0

# Variables Enemigo
img_enemigo = []
enemigo_x = []
enemigo_y = []
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_enemigos = 6

for i in range(cantidad_enemigos):
    img_enemigo.append(pygame.image.load("ovni.png"))
    enemigo_x.append(random.randint(0, 736))
    enemigo_y.append(random.randint(50, 200))
    enemigo_x_cambio.append(1.5)
    enemigo_y_cambio.append(30)

# Variables Bala
img_bala = pygame.image.load("bullet.png")
bala_x = 0
bala_y = 500
bala_x_cambio = 0
bala_y_cambio = 3.5
bala_visible = False

# Puntaje
puntaje = 0
fuente = pygame.font.Font("freesansbold.ttf", 32)
texto_x = 10
texto_y = 10

# Texto Final
fuente_final = pygame.font.Font("freesansbold.ttf", 40)

def texto_final():
    mi_fuente_final = fuente_final.render("JUEGO TERMINADO", True, (255, 255, 255))
    pantalla.blit(mi_fuente_final, (200, 250))

# Función mostrar puntaje
def mostrar_puntaje(x, y):
    texto = fuente.render(f"Puntaje: {puntaje}", True, (255, 255, 255))
    pantalla.blit(texto, (x, y))

# Función jugador
def jugador(x, y):
    pantalla.blit(img_jugador, (x, y))

# Función enemigo
def enemigo(x, y, i):
    pantalla.blit(img_enemigo[i], (x, y))

# Función disparar bala
def disparar_bala(x, y):
    global bala_visible
    bala_visible = True
    pantalla.blit(img_bala, (x + 16, y + 10))

# Función detectar colisiones
def hay_colision(x1, y1, x2, y2):
    distancia = math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))
    return distancia < 27

# Loop del juego
se_ejecuta = True
game_over = False

while se_ejecuta:

    # Fondo de pantalla
    pantalla.fill((0, 0, 0))

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            se_ejecuta = False

        # Movimientos del jugador
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                jugador_x_cambio = -3
            if evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 3
            if evento.key == pygame.K_SPACE:
                if not bala_visible:
                    bala_x = jugador_x
                    disparar_bala(bala_x, bala_y)

        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0

    # Actualizar la posición del jugador
    jugador_x += jugador_x_cambio
    if jugador_x <= 0:
        jugador_x = 0
    elif jugador_x >= 736:
        jugador_x = 736

    # Actualizar la posición del enemigo
    for i in range(cantidad_enemigos):

        # Fin del juego
        if enemigo_y[i] > 440:
            for j in range(cantidad_enemigos):
                enemigo_y[j] = 2000  # Mueve los enemigos fuera de la pantalla
            game_over = True
            break

        enemigo_x[i] += enemigo_x_cambio[i]
        if enemigo_x[i] <= 0:
            enemigo_x_cambio[i] = 1.5
            enemigo_y[i] += enemigo_y_cambio[i]
        elif enemigo_x[i] >= 736:
            enemigo_x_cambio[i] = -1.5
            enemigo_y[i] += enemigo_y_cambio[i]

        # Colisión
        colision = hay_colision(enemigo_x[i], enemigo_y[i], bala_x, bala_y)
        if colision:
            bala_y = 500
            bala_visible = False
            puntaje += 1
            enemigo_x[i] = random.randint(0, 736)
            enemigo_y[i] = random.randint(50, 200)

        enemigo(enemigo_x[i], enemigo_y[i], i)

    # Movimiento de la bala
    if bala_y <= -64:
        bala_y = 500
        bala_visible = False

    if bala_visible:
        disparar_bala(bala_x, bala_y)
        bala_y -= bala_y_cambio

    jugador(jugador_x, jugador_y)
    mostrar_puntaje(texto_x, texto_y)

    if game_over:
        texto_final()

    pygame.display.update()