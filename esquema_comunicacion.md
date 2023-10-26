1. FUENTE DE INFORMACION

    Consta de una API de Ricky y Morty 'https://rickandmortyapi.com' en la cual regresa una imagen en forma de secuencia de bytes codificada en hexadecimal.

2. TRANSMISOR

    La secuencia hexadecimal se codifica en un arreglo de pixeles. 

    Se implementa el empaquetamiento. Colocando como header [1, 3, 5, 7] y tail [9, 11, 13, 15]. Tomamos en cuenta 100 como el tamaños de los paquetes.

    Se implemento 4 tipos de codificacion donde apartir de un menu se seleccionara ya sea Huffman, Shannon-Fano, Delta o Run-Length

    Handshake

        Se implemento la funcion handshake donde se establecera un acuerdo con el recepetor para saber como se enviara la informacion(codificacion)

3. Canal

    El canal se divide en 4 subcanales donde se mandaran los paquetes, de manera aleatoria se le aplicara ruido al canal el cual tendra que cambiar al siguiente canal la informacion y empezar con el paquete que se perdio gracias a la aplicacion de ruido.



4. Receptor

    Se desempaqueta quitando el header y tail. Ademas que se decodifica de acuerdo al tipo de codificacion que se selecciono.

5. Destino

    Se visualiza la imagen.

6. Entropia

    Actualmente no se calcula la entropia.

