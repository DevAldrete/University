from datetime import datetime, timedelta
import os
from uuid import uuid4, UUID

REPORTS_DIR = "reports"


def fecha_de_archivo(file_name: str) -> datetime | None:
    """Extrae la fecha del nombre del archivo con formato YY-MMDDreportes.txt"""
    date_part = file_name.replace("reportes.txt", "").strip()
    try:
        return datetime.strptime(date_part, "%y-%m%d")
    except ValueError:
        return None


def eliminar_reporte():
    """Elimina un reporte seleccionado por el usuario."""
    archivos = [f for f in os.listdir(REPORTS_DIR) if f.endswith("reportes.txt")]
    if not archivos:
        print("No hay reportes para eliminar.")
        return

    print("\nReportes disponibles:")
    for idx, archivo in enumerate(sorted(archivos), start=1):
        print(f"{idx}. {archivo}")

    try:
        seleccion = int(input("Seleccione el número del reporte a eliminar: "))
        if 1 <= seleccion <= len(archivos):
            archivo_a_borrar = sorted(archivos)[seleccion - 1]
            confirm = input(
                f"¿Seguro que quieres eliminar '{archivo_a_borrar}'? (s/n): "
            ).lower()
            if confirm == "s":
                os.remove(os.path.join(REPORTS_DIR, archivo_a_borrar))
                print(f"Reporte '{archivo_a_borrar}' eliminado.")
            else:
                print("Eliminación cancelada.")
        else:
            print("Selección inválida.")
    except ValueError:
        print("Entrada inválida.")


def buscar_numero_de_ticket_y_fecha_anterior():
    """Encuentra el archivo más reciente y devuelve el último ticket y fecha."""
    archivos = []
    for file in os.listdir(REPORTS_DIR):
        if file.endswith("reportes.txt"):
            fecha = fecha_de_archivo(file)
            if fecha:
                archivos.append((fecha, file))

    if not archivos:
        return 0, None

    archivos.sort(reverse=True, key=lambda x: x[0])
    fecha_ultima, archivo_ultimo = archivos[0]

    with open(os.path.join(REPORTS_DIR, archivo_ultimo), "r") as f:
        lineas = f.readlines()

    ultimo_ticket = 0
    hora = 0
    for linea in lineas:
        if linea.startswith("Ticket:"):
            ultimo_ticket = int(linea.split(":")[1].strip())
        elif linea.startswith("Hora:"):
            hora = int(linea.split(":")[1].strip())

    ultima_fecha = fecha_ultima.replace(hour=hora)
    return ultimo_ticket, ultima_fecha


def crear_archivo(
    fecha_anterior: datetime,
    num_ticket_anterior: int,
    numero_de_socio: str | UUID,
    tipo_de_reporte: str,
    status: str,
):
    tiempo_actual = datetime.now()
    if (tiempo_actual - fecha_anterior) >= timedelta(days=1):
        nombre_archivo = tiempo_actual.strftime("%y-%m%d") + "reportes.txt"
        ruta = os.path.join(REPORTS_DIR, nombre_archivo)
        try:
            with open(ruta, "x", encoding="utf-8") as archivo:
                archivo.write(f"Ticket: {num_ticket_anterior + 1}\n")
                archivo.write(f"Hora: {tiempo_actual.hour}\n")
                archivo.write(f"Numero de socio: {numero_de_socio}\n")
                archivo.write(f"Tipo de reporte: {tipo_de_reporte}\n")
                archivo.write(f"Status: {status}\n")
            print(f"Archivo creado: {ruta}")
            return num_ticket_anterior + 1, tiempo_actual
        except FileExistsError:
            print("El archivo ya existe.")
    else:
        print("Aún no ha pasado un día desde el último reporte.")
    return num_ticket_anterior, fecha_anterior


def actualizar_reporte():
    """Actualiza el último reporte creado."""
    num_ticket, fecha_ultima = buscar_numero_de_ticket_y_fecha_anterior()
    if fecha_ultima is None:
        print("No hay reportes para actualizar.")
        return

    nombre_archivo = fecha_ultima.strftime("%y-%m%d") + "reportes.txt"
    ruta = os.path.join(REPORTS_DIR, nombre_archivo)

    with open(ruta, "r", encoding="utf-8") as f:
        lineas = f.readlines()

    print("\nContenido actual del reporte:")
    for linea in lineas:
        print(linea.strip())

    nuevo_tipo = input("Nuevo tipo de reporte (Enter para no cambiar): ")
    nuevo_status = input("Nuevo status (Enter para no cambiar): ")

    for i, linea in enumerate(lineas):
        if nuevo_tipo and linea.startswith("Tipo de reporte:"):
            lineas[i] = f"Tipo de reporte: {nuevo_tipo}\n"
        if nuevo_status and linea.startswith("Status:"):
            lineas[i] = f"Status: {nuevo_status}\n"

    with open(ruta, "w", encoding="utf-8") as f:
        f.writelines(lineas)

    print(f"Reporte actualizado: {ruta}")


def main():
    while True:
        print("\nBienvenido!")
        print("1. Crear reporte")
        print("2. Eliminar Reporte")
        print("3. Actualizar Reporte")
        print("4. Salir")

        opcion = input("Ingrese una opción: ")

        if opcion == "1":
            tipo_de_reporte = input("Ingrese el tipo de reporte: ")
            status = input("Ingrese el status del reporte: ")
            numero_de_socio = (
                input("Ingrese el número de socio (default: anonimo): ") or uuid4()
            )

            num_ticket_anterior, fecha_anterior = (
                buscar_numero_de_ticket_y_fecha_anterior()
            )
            if fecha_anterior is None:
                fecha_anterior = datetime.now() - timedelta(days=2)

            crear_archivo(
                fecha_anterior,
                num_ticket_anterior,
                numero_de_socio,
                tipo_de_reporte,
                status,
            )

        elif opcion == "2":
            eliminar_reporte()
        elif opcion == "3":
            actualizar_reporte()
        elif opcion == "4":
            print("Saliendo...")
            break
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    main()
