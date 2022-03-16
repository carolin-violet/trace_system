with open('424ad012-a472-11ec-ab03-1cbfc0eb0cdb.txt', 'rb') as fp:
    text = fp.read()
    cipher_list = []
    i = 0
    while i < 960:
        cipher_list.append(text[i: i+64])
        i += 64
    print(cipher_list)