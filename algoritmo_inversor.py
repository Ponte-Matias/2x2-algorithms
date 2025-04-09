# obtenemos el alg
alg=input("Ingrese el algoritmo a invertir: ")
#alg="R U' L2 F D B' R2"
# invertimos
inv=alg.split(" ")
cadena=inv[::-1]

rta=""
for i in range(0,len(cadena)):
    if len(cadena[i])==1:
        rta=rta+cadena[i]+"' "
    elif cadena[i][1]=="w":
        print("Big cubes bruh")

#    elif cadena[i][1]=="+" or cadena[i][1]=="-":
#        print("Megaminx bruh")      
    elif cadena[i][len(cadena[i])-1]=="'":
        rta=rta+cadena[i][0]+" "    

    elif cadena[i][len(cadena[i])-1]=="2":
        rta=rta+cadena[i]+" "


# imprimir el algoritmo invertido
print("Algoritmo invertido:")
print(rta)
