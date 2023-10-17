def rle_encode(data):
    encoded_data = []
    i = 0

    while i < len(data):
        count = 1
        while i < len(data) - 1 and (data[i] == data[i + 1]).all():
            count += 1
            i += 1

        encoded_data.append((data[i], count))
        i += 1

    return encoded_data