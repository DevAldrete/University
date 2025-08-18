# from math import sqrt

a = input("Valor de a: ")


def sqrt(a: float):
    n = 1
    for _ in range(10):
        n = (n + a / n) * 0.5

    return n


def calcular_valor(a: float):
    return a / (2 * sqrt(a))


print(calcular_valor(float(a)))
