import requests
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
import numpy as np

def fuente_informacion():

    print("Obteniendo la imagen....")

    api_url = 'https://rickandmortyapi.com/api/character/avatar/1.jpeg'

    # Hacer la solicitud a la URL de la imagen
    response = requests.get(api_url)

    # Obtener el contenido de la respuesta (datos binarios)
    img_content = response.content

    # Convertir los datos binarios a una imagen de PIL
    img = Image.open(BytesIO(img_content))

    return img


def transmisor(img):

  print("Convertir la imágen en un arreglo de píxeles para su envio....")

  # Convertir la imagen de PIL a un arreglo numpy de píxeles
  img_array = np.array(img)

  return img_array


def canal(img_ruido):
  
  print("Imágen enviandose al receptor....")

  return ruido(img_ruido)


def ruido(img_ruido):

  print("Presencia de ruido en el canal!")

  ruido = 20

  ruido_array = np.random.randint(ruido, ruido + 1, size=img_ruido.shape, dtype=int)

  return np.clip(img_ruido + ruido, 0, 255).astype(np.uint8)
 

def receptor(img_ruido):

  print("Imágen recibida por el receptor!")

  img_final = Image.fromarray(img_ruido)

  print("Imágen decodificada por el receptor!")

  return img_final


def destino(img_final):

  print("Imágen llegada al destino!")

  return img_final


# Codigo principal

img = fuente_informacion()

print("Imágen obtenida! -> ")

plt.imshow(img)
plt.axis('off') 
plt.show()

img_codificada =  transmisor(img)

print("Imágen codificada! ->", img_codificada[:2])

img_ruido = canal(img_codificada)

print("Imágen alterada por ruido ->", img_ruido[:2])

img_final = receptor(img_ruido)

img_final = destino(img_final)

print("Imágen final -> ")

plt.imshow(img_final)
plt.axis('off') 
plt.show()
