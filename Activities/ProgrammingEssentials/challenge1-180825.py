# 1)
print(f"Reto 1: {list(range(-2, 3))}")

# 2)
print(f"Reto 2: {list(range(1, 10, 2))}")
# secuencia = [1]
# diferencia = 2
# for _ in range(6):
#     secuencia.append(secuencia[-1] + diferencia)

# print(f"Reto 2: {secuencia}")

# 3)
examples = [range(1, 9)]

for example in examples:
    for num in example:
        if num % 2 != 0:
            print(f"\nEl numero {num} no es par")
        else:
            print(f"\nEl numero {num} es par")

    print(f"\nEjemplo terminado: {list(example)}!")

# 4)

secuencia = [1]
diferencia = 1

for _ in range(6):
    diferencia += 1
    secuencia.append(secuencia[-1] + diferencia)

print(f"Reto 4: {secuencia}")
