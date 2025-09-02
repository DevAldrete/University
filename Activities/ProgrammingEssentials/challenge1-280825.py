def obtener_hora_y_minutos():
    while True:
        hora = input("Ingrese la hora en formato 24 horas: ")
        if not hora.isdigit() or not 0 <= int(hora) < 24:
            print("Hora inválida. Intente de nuevo.")
            continue

        minutos = input("Ingrese los minutos: ")
        if not minutos.isdigit() or not 0 <= int(minutos) < 60:
            print("Minutos inválidos. Intente de nuevo.")
            continue

        break

    print(f"La hora ingresada es {hora}:{minutos}")


if __name__ == "__main__":
    obtener_hora_y_minutos()
