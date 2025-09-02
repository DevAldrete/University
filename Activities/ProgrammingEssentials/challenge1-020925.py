# Diccionario de los dias del mes

meses = {
    "Enero": 31,
    "Febrero": 28,
    "Marzo": 31,
    "Abril": 30,
    "Mayo": 31,
    "Junio": 30,
    "Julio": 31,
    "Agosto": 31,
    "Septiembre": 30,
    "Octubre": 31,
    "Noviembre": 30,
    "Diciembre": 31,
}


def buscar(nombre_mes, diccionario):
    return diccionario.get(nombre_mes, "Mes no encontrado")


def es_primo(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


for i, key in enumerate(meses.keys(), start=1):
    dias_del_mes = buscar(key, meses)
    if not es_primo(i):
        print(f"{key} tiene {dias_del_mes} días y no es número primo.")
