import numpy as np
from PIL import Image
from copy import deepcopy

def encriptar_texto() -> list[str]:
    '''
    La funcion encriptar_texto() solicita al usuario que ingrese un numero 
    por pantalla para que luego, segun una lista enumerada de caracteres,
    pueda recorrer el string ingresado por el usuario y por cada caracter, vaya guardando en una lista
    el indice en el que se encuentra ese caracter en la lista de caracteres. Existen dos posibilidades:
        --> Si el indice es menor a 10, al indice se le suma 1 y se lo agrega a la lista, seguido de un -1
        --> Si el indice es mayor o igual a 10, al indice se lo separa en dos digitos, se le suma 1 a ambos digitos
            y se los agrega a la lista junto con el -1
    Una vez finalizado el recorrido del mensaje, se agrega a la lista de mensaje encriptado un 0.
    La funcion retora una lista con todo el mensaje encriptado con sus respectivos indices.
    Argumentos:
        -> None
    Return:
        -> mensaje_codificado 
    '''
    mensaje = str(input('Favor de ingresar un mensaje: '))
    lista_caracteres = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 
                        'y', 'z', ' ','.',',','?', '!', '¿', '¡', '(', ')', ':', ';', '-', '"', "'", 'á', 'é', 'í', 'ó', 'ú', 'ü', 'ñ']
    lista_enumerada = list(enumerate(lista_caracteres, 1))
    mensaje_codificado = []
    mensaje = mensaje.lower()
    lista_msg = list(mensaje)
    for i in lista_msg:
        for indice, letra in lista_enumerada:
            if i == letra:
                if indice < 10:
                    mensaje_codificado.append(indice + 1)
                    mensaje_codificado.append(-1)
                elif indice >= 10:
                    numeros_separados = str(indice)
                    separados_lista = numeros_separados[:]
                    for e in separados_lista:
                        mensaje_codificado.append(int(e) + 1)
                    mensaje_codificado.append(-1)
    mensaje_codificado.append(0)
    return mensaje_codificado

def filtro_imagen() -> np.array:
    '''
    La funcion filtro_imagen() solicita al usuario cargar una imagen. Una vez esta imagen es ingresada, se encarga de ponerle un filtro de suavizado.
    Este proceso para suavizar la imagen involucra introducirle un padding a la imagen de dos pixeles para cada lado. Una vez con la imagen con padding, la funcion
    recorre cada pixel de la imagen, en cada uno, genera una espacio 5x5 que divide en cuatro cuadrantes iguales 3x3 , cada espacio se hace tres veces, en cada canal del RGB.
    En estos cuadrantes se calcula la varianza de cada uno de los canales y se suman, el cuadrante con la menor varianza es el "ganador", en este, se calcula el
    el promedio de los pixeles del cuadrante y se reemplaza el valor del pixel original por ese numero.
    Argumentos:
        -> None
    Return:
        -> img_lista (Imagen filtrada)
    '''
    img_lista = cargar_imagen()
    padding = np.pad(img_lista, 2, 'edge')
    copia_padding = deepcopy(padding)
    red = copia_padding[:,:,0]
    green = copia_padding[:,:,1]
    blue = copia_padding[:,:,2]
    for i in range(2, - 2, -1):
        for j in range(2, - 2, -1):
            matriz_5x5_red = crear_submatriz(red, i, j)
            matriz_5x5_green = crear_submatriz(green, i, j)
            matriz_5x5_blue = crear_submatriz(blue, i, j)
            varianza_ganadora = varianzas(matriz_5x5_red, matriz_5x5_green, matriz_5x5_blue)
            promediorojo, promedioverde, promedioazul = promedios(varianza_ganadora, matriz_5x5_red, matriz_5x5_green, matriz_5x5_blue)
            img_lista[i,j,0] = promediorojo
            img_lista[i,j,1] = promedioverde
            img_lista[i,j,2] = promedioazul
    return img_lista

def encriptacion():
    '''
    la funcion encriptacion() toma el mensaje ya encriptado ingresado por el usuario y la imagen con el filtro kuwahara.
    en la matriz de la imagen toma secciones de 2x2, calcula la varianza de los tres canales de la submatriz y, de acuerdo
    con el canal de menor varianza, calcula el promedio de los tres primeros pixeles de la submatriz en el canal seleccionado.
    Acto seguido, se modifica el ultimo pixel de la submatriz 2x2 con el valor resultante de sumar el promedio con 
    el numero que representa el caracter del mensaje codificado, tomando el modulo 256.
    Al finalizar, crea una nueva imagen con el nombre imagen_codi.png con la imagen ya codificada.
    Argumentos:
        -> None
    Return:
        -> imagen filtrada y encriptada
    
    '''
    texto_codificado = encriptar_texto()
    imagen_filtrada = filtro_imagen()
    nombre_de_salida = str(input('Favor de ingresar el nombre del archivo de salida: '))
    xlim, ylim, zlim = np.shape(imagen_filtrada)
    posTexto = 0
    for i in range(0, xlim-1, 2):
        for j in range(0, ylim-1, 2):
            matriz2x2 = imagen_filtrada[i:i+2, j:j+2]
            matriz_2x2_red   = matriz2x2[:,:,0]
            matriz_2x2_green = matriz2x2[:,:,1]
            matriz_2x2_blue  = matriz2x2[:,:,2]
            var_rojo  = np.var([matriz_2x2_red[0,0],   matriz_2x2_red[0,1], matriz_2x2_red[1,0]])
            var_verde = np.var([matriz_2x2_green[0,0], matriz_2x2_green[0,1], matriz_2x2_green[1,0]])
            var_azul  = np.var([matriz_2x2_blue[0,0],  matriz_2x2_blue[0,1], matriz_2x2_blue[1,0]])
            lista_var = [var_rojo,var_verde,var_azul]
            varmin    = min(lista_var)
            posindex  = lista_var.index(varmin)
            if  posindex == 0:
                canal = [matriz_2x2_red[0][0], matriz_2x2_red[0][1], matriz_2x2_red[1][0]]
            elif  posindex == 1:
                canal = [matriz_2x2_green[0][0], matriz_2x2_green[0][1], matriz_2x2_green[1][0]]
            elif posindex == 2:
                canal = [matriz_2x2_blue[0][0], matriz_2x2_blue[0][1], matriz_2x2_blue[1][0]]
            promedio = int(sum(canal)/len(canal))
            letra = texto_codificado[posTexto]
            if letra == 0:
                img = imagen_filtrada.astype(np.uint8)
                Image.fromarray(img).save(nombre_de_salida)
                return -1
            else:
                suma = (int(promedio) + letra) % 256
                matriz2x2[1,1,posindex] = suma
            posTexto += 1
                        
def desencriptacion() -> str:
    '''
    la funcion desencriptacion() pide una imagen encriptada al usuario, luego la divide en secciones 2x2. 
    En esta secciones calcula el canal del color con menos varianza, sin utilizar el pixel de abajo a la derecha. 
    Con esta seccion calculada, saca el promedio de sus tres pixeles, este valor se resta al valor del pixel 
    inferior derecho, si queda un numero negativo distinto de -1 se le suma 256, y finalmente este valor se agrega 
    a una lista de numeros que comienza vacia. Este proceso se repite hasta que la resta del pixel con 
    el promedio sea 0. Una vez con esta lista, se aplica la funcion desencriptar_lista() y desencriptar_numeros(), 
    estas modifican la lista de numeros que obtuvo la desencriptacion, restandole uno a cada digito y 
    juntando los digitos entre cada -1 para luego pasarlos a un string con desencriptar_numeros(). 
    Este es el mensaje encriptado que poseia la imagen. 
    Argumentos:
        -> None
    Return:
        -> desencriptar_numeros(lista_desencriptada) (Cadena de texto ya desencriptada)
    '''
    path = str(input('Ingrese nombre de la imagen a utilizar como base: '))
    img = np.array(Image.open(path), dtype=np.int32)
    imagen_encriptada = img
    lista_encriptada = []
    xlim, ylim, zlim = np.shape(imagen_encriptada)
    for i in range(0, xlim-1, 2):
        for j in range(0, ylim-1, 2):
            matriz2x2 = imagen_encriptada[i:i+2, j:j+2]
            matriz_2x2_red   = matriz2x2[:,:,0]
            matriz_2x2_green = matriz2x2[:,:,1]
            matriz_2x2_blue  = matriz2x2[:,:,2]
            var_rojo  = np.var([matriz_2x2_red[0,0],   matriz_2x2_red[0,1], matriz_2x2_red[1,0]])
            var_verde = np.var([matriz_2x2_green[0,0], matriz_2x2_green[0,1], matriz_2x2_green[1,0]])
            var_azul  = np.var([matriz_2x2_blue[0,0],  matriz_2x2_blue[0,1], matriz_2x2_blue[1,0]])
            lista_var = [var_rojo,var_verde,var_azul]
            varmin = min(lista_var)
            pos_index = lista_var.index(varmin)
            promedio = (matriz2x2[0,0,pos_index]+matriz2x2[0,1,pos_index]+matriz2x2[1,0,pos_index])/3
            promedio = int(promedio) 
            matriz2x2[1,1,pos_index] -= promedio 
            if matriz2x2[1,1,pos_index] == 0:
                lista_encriptada.append(matriz2x2[1,1,pos_index])
                lista_desencriptada = desencriptar_lista(lista_encriptada)
                return desencriptar_numeros(lista_desencriptada)
            elif matriz2x2[1,1,pos_index] < 0:
                if matriz2x2[1,1,pos_index] == -1:
                    lista_encriptada.append(matriz2x2[1,1,pos_index])
                else:
                    lista_encriptada.append(matriz2x2[1,1,pos_index]+256)   
            else:
                lista_encriptada.append(matriz2x2[1,1,pos_index])

def desencriptar_lista(lista_encriptada:list)->list:
    ''' 
    La funcion desencriptar_lista() es parte del proceso de la funcion desencriptacion. En este se toma la lista encriptada 
    obtenida a partir del proceso de desencriptacion y se la modifica para poder introducirla en desencriptar numeros y 
    obtener el texto encriptado.
    Esta funcion, para desencriptar, toma la lista encriptada y le resta 1 a cada numero exceptuando los -1 y 0, 
    luego, une todos los caracteres que esten entre los -1 y devuelve una lista con numeros separados con -1 que finaliza con un 0.
    Argumentos
        -> lista_encriptada: lista de numeros obtenida a partir de la desencriptacion 
    Return:
        -> lista_nueva: la lista encriptada con los el algoritmo necesario para progresar en su desencriptacion
    '''
    for i in lista_encriptada[:]:
        lista_encriptada[lista_encriptada.index(i)] = str(i)
    texto_unido = ''.join(lista_encriptada)
    lista_sep_menos1 = texto_unido.split('-1')
    lista_nueva = []
    for num in lista_sep_menos1:
        if num == '0':
            lista_nueva.append(0)
        if num == '10':
            lista_nueva.append(9)
        elif len(num) == 2:
            numeros_juntos = []
            numeros_juntos.append(str(int(num[0])-1))
            numeros_juntos.append(str(int(num[1])-1))
            lista_nueva.append(int(''.join(numeros_juntos)))
        elif len(num) == 3:
            numeros_juntos = []
            numeros_juntos.append(str(int(num[0])-1))
            numeros_juntos.append(str(int(num[1:3])-1))
            lista_nueva.append(int(''.join(numeros_juntos)))
        elif len(num) == 1:
            lista_nueva.append(int(num)-1)
        lista_nueva.append(-1)
    return lista_nueva


def desencriptar_numeros(lista:list) -> str:
    '''
    La funcion desencriptar_numeros() es el paso final del proceso de desencriptacion de 
    la imagen, esta se encarga de utilizar la lista previamente desencriptada y utilizando un 
    indice de una lista de caracteres, donde cada numero equivale a un caracter, cada -1 es un 
    salto de caracter a otro y el 0 es el fin del mensaje, y la utiliza para pasar esta lista a 
    un string con un mensaje previamente encriptado en la imagen.
    Argumentos:
        -> lista_desencriptada: lista de numeros que a partir de un algoritmo va a ser desencriptada
    Return:
        -> mensaje_lista: El mensaje detras de la lista encriptada
    '''
    lista_caracteres = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
                        'y', 'z', ' ','.',',','?', '!', '¿', '¡', '(', ')', ':', ';', '-', '"', "'", 'á', 'é', 'í', 'ó', 'ú', 'ü', 'ñ']
    lista_enumerada = list(enumerate(lista_caracteres, 1))
    mensaje_lista = []
    for i in lista:
        for indice, elemento in lista_enumerada:
            if indice == i:
                mensaje_lista.append(elemento)
            elif i == -1:
                continue
            elif i == 0:
                return ''.join(mensaje_lista)
    return ''.join(mensaje_lista)

 
def varianzas(rojo:np.array, verde:np.array, azul:np.array) -> int:  
    '''
    la funcion varianzas() se encarga de recibir 3 matrices 5x5 en el proceso de realizar el filtro de la imagen (roja, verde, azul).
    Esta funcion hara uso de la funcion calcular_varianza() para dividir esta submatriz en 4 secciones y, a cada una, calcularle
    la varianza en cada uno de sus canales. Luego, las tres varianzar se suman en una sola por cada seccion, poniendolas despues
    en una lista. Asi, con el uso de la funcion varianza_menor() se calculara cual varianza de las 4 es la menor y, de acuerdo a esto,
    la varianza menor sera el nuevo valor del pixel donde estamos parador en la matriz original.
    Esta funcion retorna un numero entero con el valor de la varianza menor
    Argumentos:
        -> rojo (matriz del canal rojo de una imagen)
        -> verde (matriz del canal verde de una imagen)
        -> azul (matriz del canal azul de una imagen)
        
    Return:
        -> varianza_ganadora (numero que indica el canal que tuvo menor varianza entre los tres)
    '''
    # seccion A
    rojo_A = calcular_varianza(rojo, 0, 3, 0, 3)
    verde_A = calcular_varianza(verde, 0, 3, 0, 3)
    blue_A = calcular_varianza(azul, 0, 3, 0, 3)
    # seccion B
    rojo_B = calcular_varianza(rojo, 0, 3, 2, 5)
    verde_B = calcular_varianza(verde, 0, 3, 2, 5)
    blue_B = calcular_varianza(azul, 0, 3, 2, 5)
    # seccion C
    rojo_C = calcular_varianza(rojo, 2,5,0,3)
    verde_C = calcular_varianza(verde, 2,5,0,3)
    blue_C = calcular_varianza(azul, 2,5,0,3)
    # seccion D
    rojo_D = calcular_varianza(rojo, 2,5,2,5)
    verde_D = calcular_varianza(verde, 2,5,2,5)
    blue_D = calcular_varianza(azul, 2,5,2,5)
    # Suma de canales
    varianzaA = rojo_A + verde_A + blue_A
    varianzaB = rojo_B + verde_B + blue_B
    varianzaC = rojo_C + verde_C + blue_C
    varianzaD = rojo_D + verde_D + blue_D
    varianza_ganadora = varianza_menor(varianzaA, varianzaB, varianzaC, varianzaD)  
    return varianza_ganadora

def promedios(varianza_ganadora:int, rojo:np.array, verde:np.array, azul:np.array) -> int:
    '''
    La función promedios() es utilizada en la funcion filtro_imagen() para, a partir de cual fue la 
    "varianza ganadora", sacar el promedio de ese cuadrante en cada canal de color. El proposito de esta 
    funcion es calcular el promedio que luego sera reemplazado en el pixel al que le corresponda para 
    poder aplicar el filtro Kuwahara exitosamente.
    Argumentos:
        -> varianza_ganadora: varianza a la cual se le sacara el promedio de ese cuadrante en cada canal de color
        -> rojo: uno de los array que seran utilizados para calcular el promedio del respectivo color
        -> verde: uno de los array que seran utilizados para calcular el promedio del respectivo color
        -> azul: uno de los array que seran utilizados para calcular el promedio del respectivo color
    Return:
        -> promedio_rojo,promedio_verde,promedio_azul: los promedios de los canales de cada color respectivamente 
    '''
    if varianza_ganadora == 0:
        promedio_rojo = calcular_promedio(rojo, 0, 3, 0, 3)
        promedio_verde = calcular_promedio(verde, 0, 3, 0, 3)
        promedio_azul = calcular_promedio(azul, 0, 3, 0, 3)
    elif varianza_ganadora == 1:
        promedio_rojo = calcular_promedio(rojo, 0, 3, 2, 5)
        promedio_verde = calcular_promedio(verde, 0, 3, 2, 5)
        promedio_azul = calcular_promedio(azul, 0, 3, 2, 5)
    elif varianza_ganadora == 2:
        promedio_rojo = calcular_promedio(rojo, 2,5,0,3)
        promedio_verde = calcular_promedio(verde, 2,5,0,3)
        promedio_azul = calcular_promedio(azul, 2,5,0,3)
    elif varianza_ganadora == 3:
        promedio_rojo = calcular_promedio(rojo, 2,5,2,5)
        promedio_verde = calcular_promedio(verde, 2,5,2,5)
        promedio_azul = calcular_promedio(azul, 2,5,2,5)
    return promedio_rojo,promedio_verde,promedio_azul
                           
def calcular_promedio(matriz:np.array, desde_y:int, hasta_y:int, desde_x:int, hasta_x:int) -> int:
    '''
    La funcion calcular_promedio() es parte de la funcion promedios() esta es la encargada de, 
    a partir de cada matriz introducida, calcular el promedio de los numeros dentro de esta y devolver un int con el promedio
    Argumentos:
        -> matriz: Submatriz de 5x5 en la cual se calculara el promedio de sus numeros
        -> desde_y: desde que coordenada de y se quiere recorrer la matriz
        -> hasta_y: hasta que coordenada de y se quiere recorrer la matriz
        -> desde_x: desde que coordenada de x se quiere recorrer la matriz
        -> hasta_x: hasta que coordenada de x se quiere recorrer la matriz
    Return:
        -> promedio_numero: promedio de los numeros en los valores de la matriz pedidos
    '''
    matriz = np.array(matriz)
    promedio_lista = matriz[desde_y:hasta_y,desde_x:hasta_x]
    promedio = sum(promedio_lista)/len(promedio_lista)
    promedio_numero = promedio[0]
    return int(promedio_numero)

def varianza_menor(varianzaA:int, varianzaB:int, varianzaC:int, varianzaD:int) -> int:
    '''
    La funcion varianza_menor(), toma como paramentro las varianzas, las mete en una lista y 
    elige de entre estas la que tiene el menor numero, luego devuelve el indice de donde se encuentra en la lista esa varianza.
    Argumentos:
        -> varianzaA: varianza a ser comparada
        -> varianzaB: varianza a ser comparada
        -> varianzaC: varianza a ser comparada
        -> varianzaD: varianza a ser comparada
    Return:
        -> indice donde se encuentra en la lista la menor varianza
    '''
    varianzas = [varianzaA, varianzaB, varianzaC, varianzaD]
    min_varianza = min(varianzas)
    return varianzas.index(min_varianza)
             
def calcular_varianza(matriz:np.array, desde_y:int, hasta_y:int, desde_x:int, hasta_x:int) -> int:
    '''
    La funcion calcular_varianza() toma una matriz y calcula la varianza de sus elementos metiendolos en 
    una lista y utilizando la funcion np.var de Numpy, luego devuelve la varianza de esa matriz
    Argumentos:
        -> matriz: array al cual se le calculara la varianza
        -> desde_y: desde que coordenada de y se quiere recorrer la matriz
        -> hasta_y: hasta que coordenada de y se quiere recorrer la matriz
        -> desde_x: desde que coordenada de x se quiere recorrer la matriz
        -> hasta_x: hasta que coordenada de x se quiere recorrer la matriz
    Return:
        -> varianza: la varianza de la matriz en el espacio pedido
    '''
    matriz = np.array(matriz)
    varianza_lista = matriz[desde_y:hasta_y,desde_x:hasta_x]
    varianza = np.var(varianza_lista)
    return varianza
        
def crear_submatriz(matriz:np.array, x:int, y:int) -> np.array:
    '''
    la funcion crear_submatriz() recibe una matriz, una posicion x y una posicion y. 
    Dado estos datos, esta funcion se encarga de crear una submatriz de 5x5 iniciando
    desde el pixel en donde estamos parados.
    Esta funcion devuelva un arreglo de numpy.
    Argumentos:
        -> matriz: matriz de n x m
        -> x: posicion x de determinado pixel de la matriz
        -> y: posicion y de determinado pixel de la matriz
    Return:
        -> submatriz: seccion 5x5 de la matriz dada las coordenadas del pixel
    '''
    submatriz = []
    for posy in range(-2, 3):
        fila = []
        for posx in range(-2, 3):
            fila.append(matriz[y + posy][x + posx])
        submatriz.append(fila)
    return submatriz
    
def cargar_imagen() -> np.array:
    '''
    La funcion cargar_imagen() se encarga de pedirle al usuario una imagen cualquiera y, a traves
    de la libreria Pillow, la convierte en una matriz.
    Argumentos:
        -> None
    Return:
        -> img: matriz de la imagen ingresada
    '''
    path = str(input('Ingrese nombre de la imagen a utilizar como base: '))
    img = np.array(Image.open(path))
    return img