# Reto para el tema de cadenas (tema 16)

import random

frase = {
    "Yo estudio en Tecmilenio porque": [
        "tiene buen nivel",
        "dan certificados",
        "me queda cerca",
        "estudio con amigos",
        "el ambiente esta padre",
    ]
}

selection = frase["Yo estudio en Tecmilenio porque"]
frase_completa = (
    f"{list(frase.keys())[0]} {selection[random.randint(0, len(selection) - 1)]}"
)


print(frase_completa)
print(frase_completa.lower())

counter = {"a": 0, "e": 0, "i": 0, "o": 0, "u": 0}
for char in frase_completa.lower():
    if char == "a":
        counter["a"] += 1
    elif char == "e":
        counter["e"] += 1
    elif char == "i":
        counter["i"] += 1
    elif char == "o":
        counter["o"] += 1
    elif char == "u":
        counter["u"] += 1


print("Caracteres de a, e, i, o, u: ", counter)

print(sorted(frase_completa.split(), reverse=True))
