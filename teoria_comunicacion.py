# Importamos librerias
import requests
import numpy as np
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
import time
import random
import math

# Funcion fuente de informacion, obtenemos la imagen de una api
def fuente_informacion():
    print("Obteniendo la imagen....")
    api_url = 'https://rickandmortyapi.com/api/character/avatar/1.jpeg'
    response = requests.get(api_url)
    img_content = response.content
    img = Image.open(BytesIO(img_content))
    return img

# Funcion transmisor convertimos la imagen en una arreglo, la codificamos sumando dos y realizamos el empaquetamiento
def transmisor(img_original):

    # Imagen a arreglo de numpy
    img_array = np.array(img_original)

    # Codificamos la imagen sumando 2 a cada valor
    img_codificada = img_array + 2
    print("Imágen codificada con exito!")
    
    # Obtener las dimensiones de la imagen
    alto, ancho, canales = img_codificada.shape

    # Tamaño de paquete
    tamano_paquete = 100
  

    # Empaquetamiento de imagen
    img_empaq = []
    header = [1, 3, 5, 7]  # Header 
    tail = [9, 11, 13, 15]  # Tail

    for i in range(0, alto * ancho * canales, tamano_paquete):
        bloque = img_codificada.flat[i:i + tamano_paquete]
        # Concatenamos el header y el tail a cada paquete
        paquete = np.concatenate((header, bloque, tail))
        img_empaq.append(paquete)
    

    print("Imágen empaquetada con exito y lista para su envio!")
    return img_empaq,alto,ancho, canales

# Funcion canal realizamos el envio por paquetes y llamamos de manera aletoria a la funcion de ruido y guardamos la probabilidad
def canal(paquetes):

    print("Enviando paquetes por el canal...")
    paquetes_recibidos = []
    numeros_prob = list(range(1, 51))
    umbrales = [11,12,13,14,15,41,42,43,44,45]
    entropia_valores = []

    print("Presencia de ruido en el canal...")
    #print(len(paquetes))
    for paquete in paquetes:
        numero_aleatorio = random.choice(numeros_prob)
        #print(numero_aleatorio)
        if numero_aleatorio in umbrales:
            # Obtenemos la probabilidad y la almacenamos en una lista
            probabilidad_evento = 1/len(paquetes)
            entropia_valores.append(probabilidad_evento)
            #Simular ruido cambiando algunos valores aleatorios en el paquete
            paquetes_recibidos.append(ruido(paquete))
        else:
            paquetes_recibidos.append(paquete)

        time.sleep(.01)

    return paquetes_recibidos,entropia_valores

# Funcio ruido aplicamos ruido al paquete que se recibio cambiando sus valores
def ruido(paquete):

  ruido = 20

  return np.clip(paquete + ruido, 0, 255).astype(np.uint8)

# Funcion receptor se aplica el desempaquetamiento  y la decodificacion, ademas que transformamos el arreglo a la forma de la imagen original
def receptor(paquetes_recibidos, alto, ancho, canales):

    print("Imágen recibida por el receptor y desempaquetando...")
    paquetes_desempaquetados = []

    for paquete in paquetes_recibidos:
        bloque = paquete[4:-4]  # Eliminar header y tail
        paquetes_desempaquetados.append(bloque)

    # Crear una matriz con los paquetes desempaquetados
    img_desempaquetada = np.concatenate(paquetes_desempaquetados)

    # Decodificar la imagen restandole el 2, que sumamos en la codificacion 
    img_decodificada = img_desempaquetada - 2

    # Ajustar la forma de la matriz a las dimensiones originales
    img_final = img_decodificada.reshape(alto, ancho, canales)

    return img_final

# Funcion destino se muestra la imagen final con el ruido que se aplico
def destino(img_final):

  print("Imágen lista para mostrarse!")

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


# Empezamos el proceso de transmisión
paquetes,alto,ancho,canales = transmisor(img_original)


# Simulamos el canal de transmisión
paquetes_recibidos,entropia_valores = canal(paquetes)

# Calculamos la entropia
entropia_final = entropia(entropia_valores)
print("Entropia: ",entropia_final)


# Procedemos con la recepción y desempaquetado
img_final = receptor(paquetes_recibidos, alto, ancho, canales)

# Se muestra la imagen
destino(img_final)