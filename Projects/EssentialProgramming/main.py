"""
Sistema de gestión de préstamos de libros en una biblioteca escolar

Mejoras incluidas:
- IDs cortos y autocompletado por prefijo de ID.
- Visualización de préstamos con cálculo de multas ($15/día después de 7 días).
- Límite de 4 libros por usuario.
- Administración manual de préstamos (forzar agregar/quitar).
- Bloqueo de nuevos préstamos si el usuario tiene multa pendiente.
- Opción para pagar multas.
- Persistencia en un solo JSON: {"libros": {...}, "prestamos": {...}}.

Notas de diseño:
- Fecha de préstamo por usuario: se considera la más antigua relevante para calcular multa (modelo simple).
- MultaPendiente: se actualiza dinámicamente y puede guardarse para referencia al visualizar (se recalcula al entrar a visualizar o al intentar prestar).
"""

import json  # Lectura/escritura del archivo JSON: serializa objetos Python a texto JSON y viceversa
import uuid  # Generación de identificadores únicos (UUID) para libros
from datetime import (
    datetime,
    timedelta,
)  # datetime: manipulación de fechas y horas; timedelta: diferencia entre fechas

# --- Constantes de configuración ---
RUTA_JSON = "biblioteca.json"  # Archivo JSON de almacenamiento
DIAS_PRESTAMO = 7  # Días sin multa
MULTA_POR_DIA = 15  # Multa en pesos mexicanos por día de retraso
LIMITE_LIBROS = 4  # Máximo de libros por usuario

# --- Utilidades de persistencia ---


def cargar_datos():
    """
    Carga los datos desde el archivo JSON. Si no existe, crea la estructura base.
    Estructura:
    {
        "libros": {
            "abc123": {"Nombre": "Drácula", "Disponible": true, "Cantidad": 3},
            ...
        },
        "prestamos": {
            "UsuarioX": {"Fecha": "YYYY-MM-DD", "Libros": ["Drácula", ...], "MultaPendiente": 0}
        }
    }
    """
    try:
        with open(RUTA_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Asegurar campos mínimos
            if "libros" not in data:
                data["libros"] = {}
            if "prestamos" not in data:
                data["prestamos"] = {}
            # Normalizar estructura de prestamos (asegurar MultaPendiente)
            for u, p in data["prestamos"].items():
                if "MultaPendiente" not in p:
                    p["MultaPendiente"] = 0
            return data
    except FileNotFoundError:
        return {"libros": {}, "prestamos": {}}


def guardar_datos(biblioteca):
    """Guarda el estado completo en el JSON con indentación legible y soporte de acentos."""
    with open(RUTA_JSON, "w", encoding="utf-8") as f:
        json.dump(biblioteca, f, ensure_ascii=False, indent=4)


# --- Utilidades de IDs ---


def generar_id_corto():
    """
    Genera un ID corto de 6 caracteres tomando el prefijo de un uuid4.
    Ventaja: suficientemente único para inventarios pequeños/medianos y fácil de teclear.
    """
    return str(uuid.uuid4())[:6]


def autocompletar_id(biblioteca, id_parcial):
    """
    Autocompleta un ID de libro a partir de su prefijo.
    - Si hay coincidencia única: devuelve el ID completo.
    - Si hay múltiples: muestra opciones y devuelve None (para reintento).
    - Si no hay coincidencias: devuelve None.
    """
    coincidencias = [lid for lid in biblioteca["libros"] if lid.startswith(id_parcial)]
    if len(coincidencias) == 1:
        return coincidencias[0]
    elif len(coincidencias) > 1:
        print("Coincidencias encontradas:")
        for cid in coincidencias:
            print(f"{cid} | {biblioteca['libros'][cid]['Nombre']}")
        return None
    else:
        return None


# --- Lógica de multas ---


def calcular_multa(fecha_str):
    """
    Calcula la multa a partir de una fecha de préstamo (YYYY-MM-DD).
    - Se considera fecha límite = fecha_prestamo + DIAS_PRESTAMO.
    - Si hoy > fecha_límite: multa = días_retraso * MULTA_POR_DIA
    - Si no hay retraso: 0
    """
    # Deprecated: mantiene compatibilidad con estructura antigua de fecha de préstamo
    fecha_prestamo = datetime.strptime(fecha_str, "%Y-%m-%d %H:%M") if len(fecha_str) > 10 else datetime.strptime(fecha_str, "%Y-%m-%d")
    fecha_limite = fecha_prestamo + timedelta(days=DIAS_PRESTAMO)
    dias_retraso = (datetime.now().date() - fecha_limite.date()).days
    return max(0, dias_retraso * MULTA_POR_DIA)


# Cálculo de multa basado en fecha de devolución de cada libro
def calcular_multa_libro(book):
    """
    Dado un diccionario book con FechaDevolucion "YYYY-MM-DD HH:MM", retorna multa si hay retraso.
    """
    fecha_limite = datetime.strptime(book["FechaDevolucion"], "%Y-%m-%d %H:%M")
    dias_retraso = (datetime.now() - fecha_limite).days
    return max(0, dias_retraso * MULTA_POR_DIA)


def actualizar_multas(biblioteca):
    """
    Recalcula y actualiza MultaPendiente para todos los usuarios con préstamos activos.
    Regla: Multa se calcula contra la fecha del registro del usuario (modelo simple).
    """
    # Recalcula MultaPendiente sumando multas de cada libro activo
    for usuario, datos in biblioteca["prestamos"].items():
        total = 0
        for book in datos.get("Libros", []):
            total += calcular_multa_libro(book)
        datos["MultaPendiente"] = total


# --- Vistas e inventario ---


def mostrar_libros(biblioteca):
    """
    Muestra libros con cantidad disponible > 0.
    Se imprime: ID | Nombre (Cantidad: N)
    """
    print("\n--- Libros Disponibles ---")
    disponibles = False
    for libro_id, datos in biblioteca["libros"].items():
        if datos["Cantidad"] > 0:
            disponibles = True
            print(f"{libro_id} | {datos['Nombre']} (Cantidad: {datos['Cantidad']})")
    if not disponibles:
        print("No hay libros disponibles.")


def agregar_libro(biblioteca):
    """
    Agrega un libro nuevo:
    - Pide nombre y cantidad.
    - Evita duplicados por nombre (insensible a mayúsculas).
    - Genera ID corto y marca disponibilidad según cantidad.
    """
    nombre = input("\nTítulo del nuevo libro: ").strip()
    try:
        cantidad = int(input("Cantidad de ejemplares: ").strip())
    except ValueError:
        print("Cantidad inválida.")
        return

    for datos in biblioteca["libros"].values():
        if datos["Nombre"].lower() == nombre.lower():
            print("Ese libro ya existe en el inventario.")
            return

    libro_id = generar_id_corto()
    biblioteca["libros"][libro_id] = {
        "Nombre": nombre,
        "Disponible": cantidad > 0,
        "Cantidad": cantidad,
    }
    print(f"Libro '{nombre}' agregado con ID {libro_id}.")


def modificar_libro(biblioteca):
    """
    Modifica nombre y/o cantidad de un libro existente.
    - Autocompleta ID por prefijo.
    - Actualiza la disponibilidad automáticamente con base en la cantidad.
    """
    id_parcial = input("\nID (o parte del ID) del libro a modificar: ").strip()
    libro_id = autocompletar_id(biblioteca, id_parcial)
    if not libro_id:
        print("No se encontró un libro con ese ID.")
        return

    nuevo_nombre = input("Nuevo título (vacío para no cambiar): ").strip()
    nueva_cantidad = input("Nueva cantidad (vacío para no cambiar): ").strip()

    if nuevo_nombre:
        biblioteca["libros"][libro_id]["Nombre"] = nuevo_nombre
    if nueva_cantidad:
        try:
            cantidad = int(nueva_cantidad)
        except ValueError:
            print("Cantidad inválida. No se realizaron cambios en cantidad.")
        else:
            biblioteca["libros"][libro_id]["Cantidad"] = cantidad
            biblioteca["libros"][libro_id]["Disponible"] = cantidad > 0

    print("Libro modificado.")


def eliminar_libro(biblioteca):
    """
    Elimina un libro del inventario.
    - No permite eliminar si algún usuario lo tiene prestado (por nombre).
    """
    id_parcial = input("\nID (o parte del ID) del libro a eliminar: ").strip()
    libro_id = autocompletar_id(biblioteca, id_parcial)
    if not libro_id:
        print("No se encontró un libro con ese ID.")
        return

    nombre_libro = biblioteca["libros"][libro_id]["Nombre"]
    for prestamo in biblioteca["prestamos"].values():
        for book in prestamo.get("Libros", []):
            if isinstance(book, dict) and book.get("Nombre") == nombre_libro:
                print("No se puede eliminar un libro que está prestado.")
                return

    del biblioteca["libros"][libro_id]
    print("Libro eliminado.")


# --- Préstamos ---


def prestar_libro(biblioteca):
    """
    Registra un préstamo por cada libro:
    - Autocompleta ID de libro.
    - Verifica stock, límite de libros y multas pendientes.
    - Descuenta inventario y guarda Fecha y FechaDevolucion por registro.
    - Persistencia en JSON con estructura detallada.
    """
    usuario = input("\nNombre del usuario: ").strip()
    # Recalcular multas para bloquear préstamo si hay deudas
    actualizar_multas(biblioteca)
    if usuario in biblioteca["prestamos"] and biblioteca["prestamos"][usuario].get("MultaPendiente", 0) > 0:
        print(f"Préstamo bloqueado: multa pendiente de ${biblioteca['prestamos'][usuario]['MultaPendiente']} MXN")
        return
    # Selección de libro por ID parcial
    id_parcial = input("ID (o parte del ID) del libro a prestar: ").strip()
    libro_id = autocompletar_id(biblioteca, id_parcial)
    if not libro_id:
        print("No se encontró un libro con ese ID.")
        return
    libro = biblioteca["libros"][libro_id]
    if libro["Cantidad"] <= 0:
        print("No hay ejemplares disponibles.")
        return
    # Verificar límite de préstamos activos
    actuales = len(biblioteca.get("prestamos", {}).get(usuario, {}).get("Libros", []))
    if actuales >= LIMITE_LIBROS:
        print(f"Límite de {LIMITE_LIBROS} libros alcanzado para {usuario}.")
        return
    # Actualizar inventario
    libro["Cantidad"] -= 1
    libro["Disponible"] = libro["Cantidad"] > 0
    # Registrar préstamo con fecha de inicio y fecha de devolución por libro
    now = datetime.now()
    registro = {
        "Nombre": libro["Nombre"],
        "Fecha": now.strftime("%Y-%m-%d %H:%M"),
        "FechaDevolucion": (now + timedelta(days=DIAS_PRESTAMO)).strftime("%Y-%m-%d %H:%M")
    }
    if usuario not in biblioteca["prestamos"]:
        biblioteca["prestamos"][usuario] = {"Libros": [registro], "MultaPendiente": 0}
    else:
        biblioteca["prestamos"][usuario]["Libros"].append(registro)
    # Inicialmente sin multa en préstamos recién hechos
    actualizar_multas(biblioteca)
    print(f"Préstamo registrado: '{libro['Nombre']}' para usuario {usuario}.")


def devolver_libro(biblioteca):
    """
    Registra la devolución:
    - Valida que el usuario y el libro existan en sus préstamos.
    - Incrementa inventario y marca disponible.
    - Si el usuario se queda sin libros, se mantiene su MultaPendiente para pago.
    """
    usuario = input("\nNombre del usuario: ").strip()
    libro_nombre = input("Título del libro a devolver: ").strip()

    if usuario not in biblioteca["prestamos"]:
        print("Este usuario no tiene préstamos.")
        return

    # Validar que el libro esté prestado (buscar en registros por Nombre)
    prestamos_usuario = biblioteca["prestamos"][usuario].get("Libros", [])
    if not any(b.get("Nombre", "").lower() == libro_nombre.lower() for b in prestamos_usuario):
        print("Ese libro no está registrado como prestado a este usuario.")
        return

    # Devolver al inventario (buscar por nombre)
    for _, datos in biblioteca["libros"].items():
        if datos["Nombre"] == libro_nombre:
            datos["Cantidad"] += 1
            datos["Disponible"] = True
            break

    # Devolver al inventario (buscar por nombre y luego eliminar registro detallado)

    # Encontrar y remover la entrada de libro, calcular multa si hay retraso
    removed = None
    for book in prestamos_usuario:
        if book.get("Nombre", "").lower() == libro_nombre.lower():
            removed = book
            break
    if removed:
        multa_libro = calcular_multa_libro(removed)
        biblioteca["prestamos"][usuario]["MultaPendiente"] = biblioteca["prestamos"][usuario].get("MultaPendiente", 0) + multa_libro
        prestamos_usuario.remove(removed)
        print(f"Multa generada por este libro: ${multa_libro} MXN")
    # Verificar si sin libros y sin multa, limpiar registro
    if usuario in biblioteca["prestamos"] and not biblioteca["prestamos"][usuario]["Libros"] and biblioteca["prestamos"][usuario]["MultaPendiente"] == 0:
        del biblioteca["prestamos"][usuario]
    print(f"El usuario '{usuario}' ha devuelto '{libro_nombre}'.")


def visualizar_prestamos(biblioteca):
    """
    Muestra todos los préstamos:
    - Usuario, Fecha de préstamo, Libros, Fecha límite, Días de retraso y Multa.
    - Recalcula multas al vuelo para mostrar información actualizada.
    """
    print("\n--- Préstamos y multas ---")
    if not biblioteca["prestamos"]:
        print("No hay préstamos registrados.")
        return

    actualizar_multas(biblioteca)

    for usuario, datos in biblioteca["prestamos"].items():
        print(f"\nUsuario: {usuario}")
        if not datos.get("Libros"):  # Sin préstamos activos
            print("(Sin préstamos activos)")
            print(f"Multa pendiente: ${datos.get('MultaPendiente', 0)} MXN")
            continue
        total = 0
        for book in datos["Libros"]:
            fecha_lim = datetime.strptime(book["FechaDevolucion"], "%Y-%m-%d %H:%M")
            dias_retraso = max(0, (datetime.now() - fecha_lim).days)
            multa = calcular_multa_libro(book)
            print(f"- '{book['Nombre']}': préstamo {book['Fecha']} | vence {book['FechaDevolucion']} | retraso {dias_retraso} días | multa ${multa} MXN")
            total += multa
        print(f"Total multa en préstamos activos: ${total} MXN")
        print(f"Multa pendiente acumulada: ${datos.get('MultaPendiente', 0)} MXN")


def pagar_multa(biblioteca):
    """
    Permite registrar el pago de multas de un usuario.
    - Si hay importe pendiente, se puede pagar total o parcial.
    - Si el pago excede, se ajusta a 0.
    - Tras pagar completamente, el usuario puede volver a pedir préstamos.
    """
    usuario = input("\nNombre del usuario a pagar multa: ").strip()
    if usuario not in biblioteca["prestamos"]:
        print("Este usuario no tiene registro de préstamos/multas.")
        return

    # Calcular multa total: deudas anteriores + multas por préstamos activos
    datos_usuario = biblioteca["prestamos"][usuario]
    # Fines provenientes de préstamos activos
    multas_activas = sum(calcular_multa_libro(book) for book in datos_usuario.get("Libros", []))
    # Deudas previas de libros ya devueltos almacenadas en MultaPendiente
    deudas_previas = datos_usuario.get("MultaPendiente", 0)
    saldo = multas_activas + deudas_previas

    if saldo <= 0:
        print("El usuario no tiene multa pendiente.")
        return

    print(f"Multa pendiente: ${saldo} MXN")
    try:
        pago = float(input("Monto a pagar: ").strip())
    except ValueError:
        print("Monto inválido.")
        return

    nuevo_saldo = max(0, saldo - pago)
    # Registrar nuevo monto pendiente
    datos_usuario["MultaPendiente"] = nuevo_saldo
    print(f"Pago registrado. Multa restante: ${nuevo_saldo} MXN")

    # Si el usuario ya no tiene libros y la multa quedó en 0, se puede limpiar su registro
    if not biblioteca["prestamos"][usuario]["Libros"] and nuevo_saldo == 0:
        del biblioteca["prestamos"][usuario]
        print("Registro del usuario limpiado (sin libros ni multas).")


def administrar_prestamos_manual(biblioteca):
    """
    Administración manual de préstamos (modo forzado):
    - Agregar/quitar un libro por nombre directo en la lista del usuario.
    - Opcionalmente forzar (ignorar inventario y límite) bajo responsabilidad del operador.
    - Útil para corregir inconsistencias o migraciones.
    """
    usuario = input("\nNombre del usuario: ").strip()
    accion = input("¿Agregar o quitar libro? (a/q): ").strip().lower()
    libro_nombre = input("Título del libro: ").strip()
    forzar = (
        input("¿Forzar operación ignorando límite e inventario? (s/n): ")
        .strip()
        .lower()
        == "s"
    )

    if accion == "a":
        # Verificar límite si NO se forza
        if not forzar and usuario in biblioteca["prestamos"]:
            if len(biblioteca["prestamos"][usuario]["Libros"]) >= LIMITE_LIBROS:
                print(
                    f"Límite de {LIMITE_LIBROS} libros alcanzado (usa modo forzado para bypass)."
                )
                return
        # Asegurar estructura del usuario
        if usuario not in biblioteca["prestamos"]:
            # Registrar manual con fecha y hora actual
            biblioteca["prestamos"][usuario] = {
                "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Libros": [libro_nombre],
                "MultaPendiente": 0,
            }
        else:
            biblioteca["prestamos"][usuario]["Libros"].append(libro_nombre)
        # Ajustar inventario si se encuentra el libro exacto por nombre y no es forzado
        if not forzar:
            for _, datos in biblioteca["libros"].items():
                if datos["Nombre"].lower() == libro_nombre.lower():
                    if datos["Cantidad"] > 0:
                        datos["Cantidad"] -= 1
                        datos["Disponible"] = datos["Cantidad"] > 0
                    else:
                        print(
                            "Advertencia: inventario sin stock; operación manual aún aplicada al préstamo."
                        )
                    break
        print(f"Libro '{libro_nombre}' agregado manualmente a {usuario}.")

    elif accion == "q":
        if (
            usuario in biblioteca["prestamos"]
            and libro_nombre in biblioteca["prestamos"][usuario]["Libros"]
        ):
            biblioteca["prestamos"][usuario]["Libros"].remove(libro_nombre)
            # Devolver a inventario si no es forzado
            if not forzar:
                for _, datos in biblioteca["libros"].items():
                    if datos["Nombre"].lower() == libro_nombre.lower():
                        datos["Cantidad"] += 1
                        datos["Disponible"] = True
                        break
            print(f"Libro '{libro_nombre}' quitado manualmente de {usuario}.")
            # Mantener registro del usuario para permitir pago de multa si aplica
        else:
            print("No se encontró ese libro en los préstamos del usuario.")
    else:
        print("Opción inválida.")


# --- Programa principal (menú) ---


def main():
    """
    Bucle principal de interacción por consola.
    - Todas las operaciones persisten cambios inmediatamente.
    """
    biblioteca = cargar_datos()

    while True:
        print("\n---- MENÚ PRINCIPAL ----")
        print("1. Ver libros disponibles")
        print("2. Agregar libro")
        print("3. Modificar libro")
        print("4. Eliminar libro")
        print("5. Prestar libro")
        print("6. Devolver libro")
        print("7. Visualizar préstamos y multas")
        print("8. Pagar multa")
        print("9. Administración manual de préstamos")
        print("10. Salir")

        opcion = input("\nElige una opción: ").strip()

        if opcion == "1":
            mostrar_libros(biblioteca)
        elif opcion == "2":
            agregar_libro(biblioteca)
        elif opcion == "3":
            modificar_libro(biblioteca)
        elif opcion == "4":
            eliminar_libro(biblioteca)
        elif opcion == "5":
            prestar_libro(biblioteca)
        elif opcion == "6":
            devolver_libro(biblioteca)
        elif opcion == "7":
            visualizar_prestamos(biblioteca)
        elif opcion == "8":
            pagar_multa(biblioteca)
        elif opcion == "9":
            administrar_prestamos_manual(biblioteca)
        elif opcion == "10":
            # Guardar cambios y salir
            guardar_datos(biblioteca)
            print("Saliendo del sistema...")
            break
        else:
            print("Opción inválida. Por favor ingresa un número entre 1 y 10.")

        # Guardar después de cada operación
        guardar_datos(biblioteca)


if __name__ == "__main__":
    main()
