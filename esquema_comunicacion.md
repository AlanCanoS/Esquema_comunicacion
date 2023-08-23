1. FUENTE DE INFORMACION

    Consta de una API de Ricky y Morty 'https://rickandmortyapi.com' en la cual regresa una imagen en forma de secuencia de bytes codificada en hexadecimal.

2. TRANSMISOR

    La secuencia hexadecimal se codifica en un arreglo de pixeles.

    No se implementa el empaquetamiento!

3. Canal

    El arreglo de pixeles se va enviando al receptor con un retraso de 2s para simular la velocidad.

    Ruido

        El ruido se provoca por transformacion de los datos. Se crea un arreglo de datos enteros aleatorios de las cuales se modifican de 
        manera aleatoria valores del arreglo de pixeles.

4. Receptor

    Decodifica el arreglo de pixeles a formato imagen.

5. Destino

    Se visualiza la imagen.


