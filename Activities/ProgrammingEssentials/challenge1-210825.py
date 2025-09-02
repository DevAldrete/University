from time import sleep

print("Bienvenido a una simulacion de un reloj!")

horas = float(input("Hora: "))
minutos = float(input("Minutos: "))
segundos = float(input("Segundos: "))

if segundos > 60:
    minutos += segundos % 60
    segundos //= 60

if minutos > 60:
    horas += minutos % 60
    minutos //= 60

if horas > 24:
    horas //= 24

# while True:
#     print(f"\n{int(horas)}:{int(minutos)}:{int(segundos)}\n")
#
#     sleep(1)
#     segundos += 1
#
#     if segundos == 60:
#         minutos += 1
#         segundos = 0
#
#     if minutos == 60:
#         horas += 1
#         minutos = 0
#
#     if horas == 24:
#         horas = 0

for _ in iter(int, 1):
    print(f"\n{int(horas)}:{int(minutos)}:{int(segundos)}\n")

    sleep(1)
    segundos += 1

    if segundos == 60:
        minutos += 1
        segundos = 0

    if minutos == 60:
        horas += 1
        minutos = 0

    if horas == 24:
        horas = 0
