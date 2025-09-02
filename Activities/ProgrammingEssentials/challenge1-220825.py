# 1) Utilizando la funcion print y ciclos for, crear una tabla de multiplicar para los numeros del 1 al 10:

filas = 10
columnas = 10

for i in range(1, filas + 1):
    for j in range(1, columnas + 1):
        print(f"{i * j:4}", end="")
    print()

print("    ", end="")
for col in range(1, columnas + 1):
    print(f"{col:4}", end="")
print()

print("    " + "-" * (filas * 4))

for fila in range(1, filas + 1):
    print(f"{fila:2} |", end="")
    for col in range(1, columnas + 1):
        print(f"{fila * col:4}", end="")
    print()
