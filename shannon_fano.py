def shannon_fano_codificacion(probabilidades):
    # Ordena el diccionario de probabilidades en orden descendente
    probabilidades_ordenadas = dict(sorted(probabilidades.items(), key=lambda item: item[1], reverse=True))

    # Función recursiva para la codificación Shannon-Fano
    def codificar(simbolos, inicio, fin, prefix):
        if inicio == fin:
            return {simbolos[inicio]: prefix}
        
        # Calcula la suma de probabilidades para el rango actual
        suma_probabilidades = sum(probabilidades_ordenadas[s] for s in simbolos[inicio:fin + 1])
        
        # Encuentra la división que minimiza la diferencia de probabilidades
        acumulada = 0
        for i in range(inicio, fin + 1):
            acumulada += probabilidades_ordenadas[simbolos[i]]
            if 2 * acumulada >= suma_probabilidades:
                break
        
        # Realiza la codificación para ambas mitades
        codificacion = {}
        codificacion.update(codificar(simbolos, inicio, i, prefix + '0'))
        codificacion.update(codificar(simbolos, i + 1, fin, prefix + '1'))
        
        return codificacion

    simbolos = list(probabilidades_ordenadas.keys())
    inicio = 0
    fin = len(simbolos) - 1
    codificacion_sf = codificar(simbolos, inicio, fin, "")

    return codificacion_sf