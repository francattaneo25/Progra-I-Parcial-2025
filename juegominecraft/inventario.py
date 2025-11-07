from objetos import OBJETOS

matriz_inventario= [
    [None, None, None, None, None, None, None, None],  
    [None, None, None, None, None, None, None, None],  
    [None, None, None, None, None, None, None, None]  
]

def mover_item(matriz, fila_origen, col_origen, fila_destino, col_destino):
    temp = matriz[fila_origen][col_origen]
    matriz[fila_origen][col_origen] = matriz[fila_destino][col_destino]
    matriz[fila_destino][col_destino] = temp

#odena los elemntos segun como lo quiera el jugador
