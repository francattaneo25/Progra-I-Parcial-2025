import pygame
from objetos import spawnear_objetos_iniciales

# === MATRIZ DE INVENTARIO ===
matriz_inventario = [
    [None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None]
]

# Al iniciar el inventario, spawneamos objetos iniciales
spawnear_objetos_iniciales(matriz_inventario)

# --- DIBUJAR INVENTARIO ---
def dibujar_inventario(pantalla, matriz, x_inicial, y_inicial, tam_celda):
    """Dibuja la cuadrícula del inventario y coloca los sprites dentro de cada celda."""
    for fila in range(len(matriz)):
        for col in range(len(matriz[fila])):
            x = x_inicial + col * tam_celda
            y = y_inicial + fila * tam_celda

            # Dibujar recuadro de la celda
            rect = pygame.Rect(x, y, tam_celda, tam_celda)
            pygame.draw.rect(pantalla, (80, 80, 80), rect, 2)

            # Si hay un objeto en esa celda, lo dibuja centrado
            if matriz[fila][col] is not None:
                sprite = matriz[fila][col]
                sprite_rect = sprite.get_rect(center=rect.center)
                pantalla.blit(sprite, sprite_rect)
