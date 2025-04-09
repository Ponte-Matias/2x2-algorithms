def invertir_alg(algoritmo):
    invertido = algoritmo.split(" ")
    # Chequear si tiene una rotación del tipo y al principio (para no imprimirla)
    if invertido[0][0] == 'y':
        invertido.pop(0)
    if invertido[1][0] == 'y':
        invertido.pop(1)

    # Limpiar de caracteres como espacios y ''
    invertido = list(filter(None, invertido))
    invertido = [x for x in invertido if x != ' ']
    # Invertir los moves (posicion)
    invertido = invertido[::-1]

    # Invertir movimientos (la notación)
    final=""
    for i in range(0,len(invertido)):
        if len(invertido[i])==1:
            final=final+invertido[i]+"' "
        elif invertido[i][len(invertido[i])-1]=="'":
            final=final+invertido[i][0]+" "    
        elif invertido[i][len(invertido[i])-1]=="2":
            final=final+invertido[i]+" "

    return final