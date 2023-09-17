import requests
import numpy as np
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
import time
import random
import math

def fuente_informacion():
    print("Obteniendo la imagen....")
    api_url = 'https://rickandmortyapi.com/api/character/avatar/1.jpeg'
    response = requests.get(api_url)
    img_content = response.content
    img = Image.open(BytesIO(img_content))
    return img

def transmisor(img_original):

    # Imagen a arreglo de numpy
    img_array = np.array(img_original)

    # Codificamos la imagen sumando 2 a cada valor
    img_codificada = img_array + 2
    print("Imágen codificada con exito!")
    
    # Obtener las dimensiones de la imagen
    alto, ancho, canales = img_codificada.shape

    # Tamaño de paquete (ejemplo)
    tamano_paquete = 100
  

    # Empaquetamiento de imagen
    img_empaq = []
    header = [1, 2, 3, 4]  # Header 
    tail = [5, 6, 7, 8]  # Tail

    for i in range(0, alto * ancho * canales, tamano_paquete):
        bloque = img_codificada.flat[i:i + tamano_paquete]
        paquete = np.concatenate((header, bloque, tail))
        img_empaq.append(paquete)
    

    print("Imágen empaquetada con exito y lista para su envio!")
    return img_empaq,alto,ancho, canales

def canal(paquetes):

    print("Enviando paquetes por el canal...")
    paquetes_recibidos = []
    numeros_prob = list(range(1, 51))
    umbrales = [11,12,13,14,15,41,42,43,44,45]
    entropia = 0

    print("Presencia de ruido en el canal...")
    for paquete in paquetes:
        numero_aleatorio = random.choice(numeros_prob)
        #print(numero_aleatorio)
        if numero_aleatorio in umbrales:
            probabilidad_evento = 1/10
            entropia += -probabilidad_evento * math.log2(probabilidad_evento)
            #Simular ruido cambiando algunos valores aleatorios en el paquete
            paquetes_recibidos.append(ruido(paquete))
        else:
            paquetes_recibidos.append(paquete)

        time.sleep(.01)

    return paquetes_recibidos,entropia

def ruido(paquete):

  ruido = 20

  #print("Presencia de ruido en el canal...")

  return np.clip(paquete + ruido, 0, 255).astype(np.uint8)

def receptor(paquetes_recibidos, alto, ancho, canales):

    print("Recibiendo paquetes y desempaquetando...")
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

def destino(img_final):

  print("Imágen llegada a su destino con exito!")

  # Mostramos la imagen final
  plt.imshow(img_final)
  plt.title("Imagen Final")
  plt.axis('off')
  plt.show()

# ---------------Codigo principal---------------------------
img_original = fuente_informacion()

plt.imshow(img_original)
plt.title("Imagen Original")
plt.axis('off')
plt.show()


# Empezamos el proceso de transmisión
paquetes,alto,ancho,canales = transmisor(img_original)


# Simulamos el canal de transmisión
paquetes_recibidos,entropia = canal(paquetes)
print("Entropia: ",entropia)

# Procedemos con la recepción y desempaquetado
img_final = receptor(paquetes_recibidos, alto, ancho, canales)

destino(img_final)