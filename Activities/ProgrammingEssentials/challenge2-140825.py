from math import sqrt

a = float(input("Valor de a: "))
b = float(input("Valor de b: "))
c = float(input("Valor de c: "))

radical = b**2 - 4 * a * c
if radical <= 0:
    print("No hay solucion!")
else:
    print("Hay soluciones reales")
    x1 = (sqrt(radical) + b) / (2 * a)
    x2 = (sqrt(radical) - b) / (2 * a)
    print(f"Resultados: ({x1}, {x2})")
