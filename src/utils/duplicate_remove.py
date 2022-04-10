
def unique_data(data):
    info = []
    for item in data:
        if item not in info:
            info.append(item)
    return info

