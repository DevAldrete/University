total = 0

while True:
    distancia = float(input("Que distancia recorriste hoy?"))

    if distancia == 0:
        break
    elif distancia < 0:
        continue
    else:
        unidades = input("Millas (m) o kilometros (k)")
        if unidades == "m":
            distancia *= 1.609
    total += distancia

print("La distancia total en kilometros es ", total)
