import pygame
import json
from inventario import matriz_inventario
from objetos import OBJETOS

# === MATRIZ DE FABRICACIÓN ===
mesa_fabricacion = [
    [None, None, None],
    [None, None, None],
    [None, None, None]
]

# Resultado de la mesa (1x1)
resultado = [[None]]


def pantalla_fabricacion(pantalla):
    """Muestra la mesa de crafteo y el inventario sobre el fondo."""
    fuente = pygame.font.SysFont("Minecraft", 16)
    reloj = pygame.time.Clock()

    # Fondo (tablero invisible)
    tablero_img = pygame.image.load("juegominecraft\\botones y fondos\\Tablero.png").convert_alpha()
    ancho_tablero, alto_tablero = 532, 499
    tablero_img = pygame.transform.scale(tablero_img, (ancho_tablero, alto_tablero))
    rect_tablero = tablero_img.get_rect(center=(pantalla.get_width() // 2, pantalla.get_height() // 2))

    # Coordenadas base
    tam_celda = 40
    inicio_fab_x, inicio_fab_y = rect_tablero.left + 85, rect_tablero.top + 45
    inicio_result_x, inicio_result_y = rect_tablero.left + 255, rect_tablero.top + 85
    inicio_inv_x, inicio_inv_y = rect_tablero.left + 28, rect_tablero.top + 170

    en_juego = True
    while en_juego:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                en_juego = False
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                en_juego = False

        # Dibujar fondo
        pantalla.blit(tablero_img, rect_tablero)

        # Dibujar la mesa de crafteo
        for f in range(3):
            for c in range(3):
                objeto = mesa_fabricacion[f][c]
                if objeto:
                    pantalla.blit(objeto, (inicio_fab_x + c * tam_celda, inicio_fab_y + f * tam_celda))

        # Dibujar resultado
        if resultado[0][0]:
            pantalla.blit(resultado[0][0], (inicio_result_x, inicio_result_y))

        # Dibujar inventario (3x8)
        for f in range(3):
            for c in range(8):
                objeto = matriz_inventario[f][c]
                if objeto:
                    pantalla.blit(objeto, (inicio_inv_x + c * tam_celda, inicio_inv_y + f * tam_celda))

        # Título
        texto = fuente.render("Mesa de Crafteo", True, (255, 255, 255))
        pantalla.blit(texto, (pantalla.get_width()//2 - texto.get_width()//2, 15))

        pygame.display.flip()
        reloj.tick(60)



def cargar_recetas_desde_json(ruta_archivo: str) -> dict:
    """
    Carga un archivo JSON con las recetas de fabricación y
    las convierte al formato de diccionario con tuplas como claves.
    """
    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        data = json.load(archivo)

    recetas = {}
    for resultado, matriz in data.items():
        clave = tuple(tuple(fila) for fila in matriz)
        recetas[clave] = resultado
    return recetas

# === CARGA DE RECETAS DESDE JSON ===
recetas = cargar_recetas_desde_json("juegominecraft\\recetas.json")


# === FUNCIÓN PARA FABRICAR ===
def fabricar_objeto(nombre_objeto: str):
    objeto = OBJETOS.get(nombre_objeto)
    if objeto:
        return objeto["sprite"]
    return None


# === FUNCIÓN PARA VERIFICAR SI LA MESA COINCIDE CON ALGUNA RECETA ===
def verificar_receta():
    """
    Compara la mesa de fabricación actual con todas las recetas cargadas.
    Si encuentra coincidencia, actualiza el resultado con el sprite del objeto fabricado.
    """
    # Convertimos la mesa a tuplas (para poder comparar con las claves del diccionario)
    patron_actual = tuple(tuple(fila) for fila in mesa_fabricacion)

    for patron, nombre_objeto in recetas.items():
        if patron_actual == patron:
            resultado[0][0] = fabricar_objeto(nombre_objeto)
            print(f"✅ Se fabricó: {nombre_objeto}")
            return nombre_objeto

    # Si no hay coincidencia
    resultado[0][0] = None
    print("Ninguna receta coincide.")
    return None


# === FUNCIÓN PARA LIMPIAR LA MESA ===
def limpiar_mesa():
    """Reinicia la mesa de fabricación."""
    for i in range(3):
        for j in range(3):
            mesa_fabricacion[i][j] = None
    resultado[0][0] = None