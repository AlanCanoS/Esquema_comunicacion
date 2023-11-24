import requests
import numpy as np
from PIL import Image
import pandas as pd
from io import BytesIO
import matplotlib.pyplot as plt
import time
import random
import hashlib
import math
from decimal import Decimal, getcontext
from huffman_codi import huffman 
from shannon_fano import shannon_fano_codificacion
from run_length import rle_encode
from delta import delta_encode


# -----------------------Funciones-------------------------------------
def busqueda_binaria(arr_hashes, arr_simbolos, elemento):
    izquierda, derecha = 0, len(arr_hashes) - 1

    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2
        if arr_hashes[medio] == elemento:
            return arr_simbolos[medio]  # Se encontró el elemento, devuelve el símbolo
        elif arr_hashes[medio] < elemento:
            izquierda = medio + 1
        else:
            derecha = medio - 1

    return None  # El elemento no fue encontrado

# Funcion fuente de informacion, obtenemos la imagen de una api
def fuente_informacion():
    print("Obteniendo la imagen....")
    api_url = 'https://rickandmortyapi.com/api/character/avatar/1.jpeg'
    response = requests.get(api_url)
    img_content = response.content
    img = Image.open(BytesIO(img_content))
    return img


def hash_receptor(codificacion_type,tipo_codificacion):

    hash_paquete = []

    if tipo_codificacion == 'Huffman' or tipo_codificacion == 'Shannon-Fano':

    # Obtener los códigos Huffman en una lista
        codigos_huffman_lista = list(codificacion_type.values())

        claves_huffman_lista = list(codificacion_type.keys())
        
        for val in codigos_huffman_lista:

        
            # Calcular el hash SHA-256
            hash_paquete.append(hashlib.sha256(val.encode()).hexdigest())

    elif tipo_codificacion == 'Run-Length':

        codigos_huffman_lista = [''.join(map(str, arr)) for arr, _ in codificacion_type]
        
        claves_huffman_lista = codificacion_type.keys()
        claves_huffman_lista = list(claves_huffman_lista)

        for val in codigos_huffman_lista:
            hash_paquete.append(hashlib.sha256(val.encode()).hexdigest())
    
    elif tipo_codificacion == 'Delta':

        codigos_huffman_lista = [''.join(map(str, arr)) for arr in codificacion_type]

        claves_huffman_lista = codificacion_type.keys()
        claves_huffman_lista = list(claves_huffman_lista)

        for val in codigos_huffman_lista:
            hash_paquete.append(hashlib.sha256(val.encode()).hexdigest())
        
    df = pd.DataFrame()

    df['Simbolos'] = claves_huffman_lista
    df['Codigos'] = codigos_huffman_lista
    df['Hash'] = hash_paquete

    return df

def hash_transmisor(img,tipo_codificacion):

    paquetes_hash = []

    if tipo_codificacion == 'Run-Length':
        paquetes = [''.join(map(str, val)) for val in img]
        paquetes_img = list(paquetes)
        for val in paquetes_img:
            paquetes_hash.append(hashlib.sha256(val.encode()).hexdigest())
    elif tipo_codificacion == 'Delta':
        paquetes = [''.join(map(str, val)) for val in img]
        paquetes_img = list(paquetes)
        for val in paquetes_img:
            paquetes_hash.append(hashlib.sha256(val.encode()).hexdigest())
    else:
        for val in img:
            paquetes_hash.append(hashlib.sha256(val.encode()).hexdigest())

    return paquetes_hash

# Funcion para ponerse de acuerdo con el receptor sobre la informacion 
def handshake(tipo_codificacion,codigo_data):

    n = 1
    print("Comunicacion con el receptor para conocer la codificacion de la informacion..")

    print("Informacion codificada con: "+tipo_codificacion)

    if tipo_codificacion == 'Huffman':
      
        for simbolo, codigo in codigo_data.items():
            print(f"Simbolo: {simbolo}, Codigo Huffman: {codigo}")
            n += 1
            if n > 20:
                break

    elif tipo_codificacion == 'Shannon-Fano':

        for simbolo, codigo in codigo_data.items():
            print(f"Simbolo: {simbolo}, Codigo Huffman: {codigo}")
            n += 1
            if n > 20:
                break
    
    elif tipo_codificacion == 'Run-Length':

        print("Codificacion Run-Length: ", codigo_data[:20])
    
    elif tipo_codificacion == 'Delta':
        
        print("Codificacion Delta: ",codigo_data[:20])


    return True

# Funcion transmisor donde se codificara la imagen de acuerdo al tipo de codificacion que sea seleccionado
def transmisor(img_original):

    # Imagen a arreglo de numpy
    img_array = np.array(img_original)
    #print("Img en pixeles",img_array)

    alto, ancho, canales = img_array.shape


    img_binaria = []

    for dimension1 in img_array:
      for dimension2 in dimension1:
          #print(dimension2)
          img_binaria.append(np.unpackbits(dimension2.astype(np.uint8)))


    # Empaquetamiento de imagen
    img_empaq = []
    header = [0, 0]
    tail = [1, 1]

    repeticiones = {}

    for bloque in img_binaria:
        # Concatenamos el header y el tail a cada paquete
        paquete = np.concatenate((header, bloque, tail))
        img_empaq.append(paquete)

        paquete_tupla = tuple(paquete)

        # Contar repeticiones en el diccionario
        if paquete_tupla in repeticiones:
            repeticiones[paquete_tupla] += 1
        else:
            repeticiones[paquete_tupla] = 1
    
    print("Imagen empaquetada con exito!")

    # Calcula el total de repeticiones
    total_repeticiones = sum(repeticiones.values())
    print(img_empaq[:50])

    # Normaliza las probabilidades dividiendo por el total de repeticiones
    for paquete, repeticion in repeticiones.items():
        repeticiones[paquete] = repeticion / total_repeticiones

    #print("Suma de probabilidades:", sum(repeticiones.values()))


    # Menu para que se seleccione el tipo de codificacion
    print("------------------Tipo de codificacion------------------")
    print("Digite 1 para codificar en Huffman ")
    print("Digite 2 para codificar en Shannon-Fano")
    #print("Digite 3 para codificar en Run-Length")
    #print("Digite 4 para codificar en Delta")
    opcion = input("Ingrese el numero de la opcion deseada: ")
    paquetes_codificados = []

    if opcion == '1':

        codificacion_type = huffman(repeticiones)
        

        tipo_codificacion = 'Huffman'
        print("Codificacion huffman con exito!")

        for i in range(0,len(img_empaq)):
            paquetes_codificados.append(codificacion_type[tuple(img_empaq[i])])
    
    elif opcion == '2':
       
        codificacion_type = shannon_fano_codificacion(repeticiones)

        
       
        tipo_codificacion = 'Shannon-Fano'
        print("Codificacion Shannon-Fano con exito!")

        for i in range(0,len(img_empaq)):
            paquetes_codificados.append(codificacion_type[tuple(img_empaq[i])])

    elif opcion == '3':

        img_empaq_plana = [paquete.flatten() for paquete in img_empaq]

        # Aplicamos RLE a la lista plana
        codificacion_type = rle_encode(img_empaq_plana)

        

        tipo_codificacion = 'Run-Length'
        print("Codificacion Run-Length con exito!")

        paquetes_codificados = codificacion_type

    elif opcion == '4':

        codificacion_type = delta_encode(img_empaq)

        
        tipo_codificacion = 'Delta'
        print("Codificacion Delta con exito!")

        paquetes_codificados = codificacion_type
    

    if handshake(tipo_codificacion,codificacion_type):
      print("Entendimiento con el receptor exitoso!")
    else:
      print("Error al entenderse con el receptor!")
    
    paquetes_hash = hash_transmisor(paquetes_codificados,tipo_codificacion)
    
    print("Paquetes hasheados listos!")
    print(paquetes_hash[:20])


    #print("Imágen empaquetada con exito y lista para su envio!")
    return paquetes_hash, codificacion_type, alto, ancho, canales, tipo_codificacion

# Funcion canal
def canal(paquetes):


    listas_nueva = []
    for a in paquetes:
        listas_nueva.append(['0'])

    i = 0
    canal = 0
    paquetes_resagados = []

    while i < (len(paquetes)-2):

        if random.randint(1,3) == 3:
            if canal == 4:
                canal = 0
                print("Presencia de ruido, cambiando de canal a: ",canal)
                print("Paquete hasheado: ", i, "no enviado")
                paquetes_resagados = i
                print("Canal: ",canal, "Enviando paquetes hasheados: ",i+1, " ",i+2)
                listas_nueva[i+1] = paquetes[i+1]
                listas_nueva[i+2] = paquetes[i+2]
                i = i + 3
            else:
                canal = canal + 1
                print("Presencia de ruido, cambiando de canal a: ",canal)
                print("Paquete hasheado: ", i, "no enviado")
                paquetes_resagados = i
                print("Canal: ",canal, "Enviando paquetes hasheados: ",i+1, " ",i+2)
                listas_nueva[i+1] = paquetes[i+1]
                listas_nueva[i+2] = paquetes[i+2]
                i = i + 3
        else:
            print("Canal: ",canal, "Enviando paquetes hasheados: ", i," ",i+1," ",i+2)
            listas_nueva[i] = paquetes[i]
            listas_nueva[i+1] = paquetes[i+1]
            listas_nueva[i+2] = paquetes[i+2]
            i = i + 3

        if paquetes_resagados != []:
            print("Canal: ",canal, "Enviando paquete hasheados: ",paquetes_resagados)
            listas_nueva[paquetes_resagados] = paquetes[paquetes_resagados]
            paquetes_resagados = []


    return listas_nueva

# Funcion receptor se aplica el desempaquetamiento  y la decodificacion, ademas que transformamos el arreglo a la forma de la imagen original
def receptor(paquetes, codificacion_type, alto, ancho, canales,tipo_codificacion):

    df_receptor = hash_receptor(codificacion_type,tipo_codificacion)
    print("-------------------------------------------------")
    print(df_receptor)
    df_sorted_receptor = df_receptor.sort_values(by='Hash')
    # Paso 1: Ordena el DataFrame por la columna "Hash"
    #df_sorted_receptor = df_receptor.sort_values(by='Hash')

    simbolos_finales = [busqueda_binaria(df_sorted_receptor['Hash'].tolist(), df_sorted_receptor['Simbolos'].tolist(), paquete) for paquete in paquetes]

    print(simbolos_finales[:30])
    paquetes_desempaquetados = []
    for paquete in simbolos_finales:
            bloque = paquete[2:-2]  # Eliminar header y tail
            paquetes_desempaquetados.append(bloque)
    
    img_desempaquetada = [np.packbits(paquete) for paquete in paquetes_desempaquetados]

    img_desempaquetada = np.array(img_desempaquetada)

        #print(img_desempaquetada[:20])
        # Ajustar la forma de la matriz a las dimensiones originales
    img_final = img_desempaquetada.reshape(alto, ancho, canales)
    return img_final

# Funcion destino se muestra la imagen final 
def destino(img_final):

  print("Imagen lista para mostrarse!")

  # Mostramos la imagen final
  plt.imshow(img_final)
  plt.title("Imagen Final")
  plt.axis('off')
  plt.show()

# Funcion entropia se calcula la entropia de la probabilidad de todos los paquetes que recibieron ruido
def entropia(entropia):

    entropia_final = 0

    for val in entropia:

        entropia_final += -val * math.log2(val)

    return entropia_final


# ------------------------------------Codigo principal----------------------------------------

# Obtenemos la imagen
img_original = fuente_informacion()

# Mostramos la imagen original
plt.imshow(img_original)
plt.title("Imagen Original")
plt.axis('off')
plt.show()


# Empezamos el proceso de transmisión y por ende la codificacion
paquetes,codificacion_type,alto,ancho,canales,tipo_codificacion = transmisor(img_original)
#print("paquetes: ",paquetes[:20])
#print("tamaño paquetes: ",len(paquetes))

# Simulamos el canal de transmisión
paquetes_recibidos = canal(paquetes)


# Calculamos la entropia
#entropia_final = entropia(entropia_valores)
#print("Entropia: ",entropia_final)


# Procedemos con la recepción y desempaquetado
img_final = receptor(paquetes_recibidos,codificacion_type, alto, ancho, canales,tipo_codificacion)

# Se muestra la imagen
destino(img_final)