import numpy

print("Poner nombre")
print("Programa para resolver un problema de optimización por el método Simplex")
print("Ingrese el numero de restricciones que tiene el ejercicio")
restricciones=int(input())
print("Ingrese el numero variables estructurales más las variables de holgura que posee el ejercicio, restando una unidad")
variables=int(input())

def newMatrix(filas,columnas,n):
    M = []
    for i in range(filas):
        a = [n]*columnas
        M.append(a)
    return M

MA=newMatrix(restricciones+1,variables+2,0)

for j in range(0,restricciones+1):
    for k in range (0,variables+2):
        print("Ingrese el valor",j+1,k+1)
        MA[j][k]=float(input())
        
MA


ma= numpy.asarray(MA)
ma0 = numpy.copy(ma)
print("Coloque 1 si es maximizacion o 2 si es minimizacion")
metodo= int(input())

if metodo == 1:
    print("Eligio Maximización")
    while min(ma0[0])<0:
        print("--------------")
        print("--------------")
        print("Matriz ampliada")
        print(ma0)
        print("--------------")
        print("--------------")
        
        #Encontrando el pivote
        r=[]
        for l in range(0,restricciones):
            n= ma0[l+1][variables+1]
            d= ma0[l+1][numpy.argmin(ma0[0])]
            
            if d!=0 :
                t= n/d
            else:
                t=1000000000000000000
            if t<0:
                r.append(10000000000000000000)
            else:
                r.append(t)
        
        #Por lo tanto el pivote estatà ubicado por la fila del numero del minimo de r mas uno y en la columna en donde se encuentra el valor mas negativo de la fila 0
        pivote= ma0[numpy.argmin(r)+1][numpy.argmin(ma0[0])]
        print("el pivote es: ",pivote," que en este caso el pivote esta ubicado en fila: ",numpy.argmin(r)+1,"columna",numpy.argmin(ma0[0]))
        #comienza el algortitmo para la tranformacion de la matriz
        
        ma0[numpy.argmin(r)+1]=ma0[numpy.argmin(r)+1]/pivote
        print("-------------")
        print("-------------")
        print("-------------")
        #Bucle para la tranformacion de filas de la matriz
        print("------La matriz antes de usar el metodo Gaus Jordan pero haciendo el pivot 1--------")
        print("--------------")
        print(ma0)
        print("--------------")
        print("--------------")
        idf= numpy.argmin(ma0[0])
        for i in range(0,restricciones+1):
            #Condicional que evita transformar la fila del pivote
            if i != numpy.argmin(r)+1:
                
                print("Como i=",i," y es diferente de ",numpy.argmin(r)+1," se ejecuta")
                print("Proceso Gaus Jordan")
                print("Este es el paso",i,"a la fila ",ma0[i], "se la transforma multiplicando ",ma0[numpy.argmin(r)+1]," por ",-ma0[i][idf]," que esta en la  posicion",i," ",idf)
                print("--------------")
                print("--------------")
                print(ma0)
                print("--------------")
                print("--------------")
                ma0[i]= -(ma0[i][idf])*ma0[numpy.argmin(r)+1]+ma0[i]
                print("Teniendo ",ma0[i],"Asi la funcion objetivo se maximiza en un valor de ",ma0[0][variables+1])                
else:
    print("Eligio Minimización")
    while max(ma0[0])>0:
        print("--------------")
        print("--------------")
        print(ma0)
        print("--------------")
        print("--------------")
        
        #Creando al vector de interseccion para encontrar el pivote
        r=[]
        for l in range(0,restricciones):
            n= ma0[l+1][variables+1]
            d= ma0[l+1][numpy.argmax(ma0[0])]
            
            if d!=0 :
                t= n/d
            else:
                t=1000000000000000000
            if t<0:
                r.append(10000000000000000000)
            else:
                r.append(t)
        
        #Por lo tanto el pivote estatà ubicado por la fila del numero del minimo de r mas uno y en la columna en donde se encuentra el valor ams negativo de la fila 0
        pivote= ma0[numpy.argmin(r)+1][numpy.argmax(ma0[0])]
        print("el pivote es: ",pivote,"  en este caso el pivote esta ubicado en fila: ",numpy.argmin(r)+1,"columna",numpy.argmax(ma0[0]))
        #comienza el algortitmo para la tranformacion de la matriz
        
        ma0[numpy.argmin(r)+1]=ma0[numpy.argmin(r)+1]/pivote
        print("-------------")
        print("-------------")
        print("-------------")
        #Bucle para la tranformacion de filas de la matriz
        print("------La matriz antes de entrar en el proceso Gaus Jordan--------")
        print("--------------")
        print(ma0)
        print("--------------")
        print("--------------")
        idf= numpy.argmax(ma0[0])
        for i in range(0,restricciones+1):
            #Condicional que evita transformar la fila del pivote
            if i != numpy.argmin(r)+1:
                
                print("Como i ",i,"Es diferente de ",numpy.argmin(r)+1," se ejecuta")
                print("Proceso Gaus Jordan")
                print("Este es el paso",i,"a la fila ",ma0[i], "se la transforma multiplicando ",ma0[numpy.argmin(r)+1]," por ",-ma0[i][idf]," que esta en la  posicion",i," ",idf)
                print("--------------")
                print("--------------")
                print(ma0)
                print("--------------")
                print("--------------")
                ma0[i]= -(ma0[i][idf])*ma0[numpy.argmin(r)+1]+ma0[i]
                print("Teniendo ",ma0[i],"Asi la funcion objetivo se minimiza en un valor de ",ma0[0][variables+1])
