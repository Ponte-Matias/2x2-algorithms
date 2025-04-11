def invertir_alg(algoritmo):
    invertido = algoritmo.split(" ")
    # Limpiar de caracteres como espacios y ''
    invertido = list(filter(None, invertido))
    invertido = [x for x in invertido if x != ' ']
    # Chequea si tiene una rotación del tipo y al principio (para no imprimirla)
    if invertido[0][0] == 'y':
        invertido.pop(0)
    if invertido[1][0] == 'y':
        invertido.pop(1)
    
    # Invertir los moves (posicion)
    invertido = invertido[::-1]

    # Invertir movimientos (la notación)
    final=""
    for move in invertido:
        if len(move) == 1:
            final = final + move+"' "
        elif move[1] == "'":
            final = final + move[0] + " "
        elif move[1] == "2":
            final = final + move[0:2] + " "     # No pongo move completo porque a veces usan R2' por ejemplo, de esta forma evito el '

    return final