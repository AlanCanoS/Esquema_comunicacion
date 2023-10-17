
def delta_encode(data):
    # Inicializamos una lista para almacenar las diferencias
    encoded_data = [data[0]]

    # Iteramos a través de los datos y calculamos las diferencias
    for i in range(1, len(data)):
        difference = data[i] - data[i - 1]
        encoded_data.append(difference)

    return encoded_data