1. FUENTE DE INFORMACION

    Consta de una API de Ricky y Morty 'https://rickandmortyapi.com' en la cual regresa una imagen en forma de secuencia de bytes codificada en hexadecimal.

2. TRANSMISOR

    La secuencia hexadecimal se codifica en un arreglo de pixeles. 

    La imágen se codifica sumando 2 a cada unos de los pixeles.

    Se implementa el empaquetamiento. Colocando como header [1,2,3,4] y tail [5,6,7,8]. Tomamos en cuenta 100 como el tamaños de los paquetes.

3. Canal

    Los paquetes se van enviando al receptor cada 0.01 segundos considerando una posibilidad de que el paquete se inserte ruido. Se creo una lista de números del 1 al 50 y una lista de umbrales del 11 al 15 y del 41 al 45 donde será el que detone el ruido si el valor aleatorio que va del 1 al 50 se enuentre en el umbral.

    Ruido

        El ruido se provoca por transformacion de los datos. Se modifica los valores de esos paquetes que fueron detonados por el ruido.

4. Receptor

    Se desempaqueta quitando el header y tail. Ademas que se decodifica restandole el 2 que se sumó en el transmisor.

5. Destino

    Se visualiza la imagen.


