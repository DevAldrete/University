"""
Actividad 4

Este script cubre:
1) Uso de tuplas
2) Uso de diccionarios
3) Manejo de excepciones
4) Uso de strings
5) Menú principal para ejecutar cada sección
"""

# Utilidades de entrada


def leer_entero(prompt: str) -> int:
    """
    Lee un entero desde input() con validación. Repite hasta que el usuario ingrese un número válido.
    - prompt: el texto que se mostrará al pedir el dato.
    - return: el entero validado.
    """
    while (
        True
    ):  # 'while' repite hasta que logremos convertir la entrada a int sin error.
        dato = input(prompt)  # input() siempre devuelve un string.
        try:  # Intentamos convertir a int.
            valor = int(dato)
            return valor  # Si funciona, devolvemos el entero.
        except ValueError:  # Si falla, avisamos y volvemos a pedir.
            print("Debes ingresar un número entero válido.")


# 1. Uso de tuplas


def sumar_numeros(nums: tuple[int | float, ...]) -> float:
    """
    Recibe una tupla de números y retorna la suma de todos sus elementos.
    El '...' en el type hint indica que la tupla puede tener muchos elementos.
    """
    return sum(nums)  # sum() agrega todos los valores numéricos de un iterable.


def actividad_tuplas() -> None:
    """
    Demostración paso a paso de:
    - Crear una tupla,
    - Acceder a su tercer elemento,
    - Agregar dos números (vía input) creando una nueva tupla,
    - Convertir la tupla a lista y ordenar,
    - Sumar los elementos con una función.
    """
    print("\n--- Actividad: Tuplas ---")

    # Creamos una tupla (inmutable) con al menos cinco números.
    numeros: tuple[int, ...] = (1, 2, 3, 4, 5)
    print("Tupla inicial:", numeros)

    # Accedemos al tercer elemento (índices empiezan en 0, así que 2 es el tercero).
    print("Tercer elemento (numeros[2]):", numeros[2])

    # Pedimos dos números adicionales al usuario.
    print("Agrega dos números adicionales a la tupla:")
    num1 = leer_entero("Número 1: ")
    num2 = leer_entero("Número 2: ")

    # Como las tuplas son inmutables, creamos una nueva tupla concatenando.
    numeros = numeros + (num1, num2)  # También se puede usar 'numeros += (num1, num2)'.
    print("Tupla actualizada:", numeros)

    # Convertimos la tupla a lista para poder ordenarla (las tuplas no tienen .sort()).
    lista_numeros = list(numeros)  # list() crea una lista desde cualquier iterable.
    lista_numeros.sort()  # .sort() ordena la lista en el lugar (in place) y no retorna nada.
    print("Números ordenados:", lista_numeros)

    # Alternativa: sorted(numeros) devuelve una nueva lista ordenada sin modificar 'numeros'.
    # print("Ordenados (con sorted):", sorted(numeros))

    # Sumamos los elementos de la tupla usando la función definida.
    total = sumar_numeros(numeros)
    print("Suma de todos los números en la tupla:", total)


# 2. Uso de diccionarios


def obtener_numero(contactos: dict[str, str], nombre: str) -> str | None:
    """
    Dado un diccionario de contactos (nombre -> teléfono) y un nombre,
    retorna el teléfono si existe, o None si no está registrado.
    Se utiliza dict.get() para evitar errores si la clave no existe.
    """
    return contactos.get(
        nombre
    )  # get() devuelve None (o un default) si la clave no está.


def actividad_diccionarios() -> None:
    """
    Demostración paso a paso de:
    - Crear un diccionario de contactos,
    - Agregar un nuevo contacto,
    - Iterar sobre las claves e imprimir los nombres,
    - Buscar un número por nombre usando una función.
    """
    print("\n--- Actividad: Diccionarios ---")

    # Creamos un diccionario con al menos tres entradas.
    contactos: dict[str, str] = {
        "mario": "1234567890",
        "ana": "0987654321",
        "luis": "1122334455",
    }
    print("Contactos iniciales:", contactos)

    # Agregamos un nuevo contacto mediante captura de datos.
    print("Agrega un nuevo contacto al diccionario")
    nombre = (
        input("Nombre: ").strip().lower()
    )  # normalizamos a minúsculas para búsquedas consistentes
    numero = input("Número de teléfono: ").strip()
    contactos[nombre] = numero  # Asignamos por clave; si la clave no existe, se crea.

    # Iteramos sobre las claves (nombres) con un 'for'.
    # 'for' recorre cada elemento de la secuencia; en un dict, por defecto, recorre sus claves.
    print("Nombres de contactos:")
    for key in contactos:
        print("-", key)

    # Probamos la búsqueda del número por nombre usando la función.
    consulta = input("Ingresa el nombre a consultar: ").strip().lower()
    resultado = obtener_numero(contactos, consulta)
    if resultado is None:
        print(f"No se encontró el contacto '{consulta}'.")
    else:
        print(f"Número de teléfono de {consulta}: {resultado}")


# 3. Uso de excepciones


def actividad_excepciones() -> None:
    """
    Demostración de manejo de excepciones:
    - Capturar ValueError si el usuario ingresa valores no numéricos,
    - Mostrar la suma si ambos son numéricos,
    - Manejar ZeroDivisionError al dividir entre cero.
    """
    print("\n--- Actividad: Excepciones ---")

    # Intentamos leer dos enteros. Si falla la conversión, atrapamos el ValueError.
    try:
        num1 = int(input("Ingresa el primer número entero: "))
        num2 = int(input("Ingresa el segundo número entero: "))
    except ValueError:
        print("Error: Debes ingresar valores numéricos enteros.")
        return  # 'return' sale de la función, pues no podemos continuar sin números válidos.

    # Si llegamos aquí, ambos valores son enteros válidos.
    print("Tu suma es:", num1 + num2)

    # La división puede fallar si num2 es 0, así que protegemos ese caso.
    try:
        print("Tu división es:", num1 / num2)
    except ZeroDivisionError:
        print("Error: No se puede dividir entre cero.")


# 4. Uso de strings


def contar_palabras(texto: str) -> int:
    """
    Cuenta cuántas palabras contiene un string.
    Se usa .split() (por defecto separa por cualquier espacio en blanco) y len() para contar.
    """
    palabras = texto.split()
    return len(palabras)


def actividad_strings() -> None:
    """
    Demostración con strings:
    - Crear un mensaje,
    - Imprimir su longitud,
    - Convertir a mayúsculas,
    - Reemplazar una palabra,
    - Contar palabras mediante función.
    """
    print("\n--- Actividad: Strings ---")

    # Creamos el mensaje base como string (texto).
    mensaje = "Texto preferido"
    print("Mensaje original:", mensaje)

    # len() devuelve la cantidad de caracteres del string.
    print("Longitud del mensaje:", len(mensaje))

    # .upper() convierte todo el texto a mayúsculas.
    print("Mensaje en mayúsculas:", mensaje.upper())

    # .replace("preferido", "favorito") reemplaza la palabra indicada.
    print("Mensaje con palabra reemplazada:", mensaje.replace("preferido", "favorito"))

    # Contamos palabras usando la función definida arriba.
    print("Cantidad de palabras en el mensaje:", contar_palabras(mensaje))


# 5. Menú principal

"""
Muestra un menú con opciones y dirige al usuario a la actividad elegida.
Usa un bucle 'while True' para repetir hasta que el usuario elija salir.
Valida la opción con try/except para evitar ValueError.
"""
while True:
    print("\n--- Menú Principal ---")
    print("¿Qué tipo de dato deseas capturar o probar?")
    print("1. Tuplas")
    print("2. Diccionarios")
    print("3. Enteros y excepciones")
    print("4. Strings")
    print("5. Salir")

    # Leemos la opción validando que sea un entero.
    try:
        opcion = int(input("Elige una opción (1-5): "))
    except ValueError:
        print("Debes ingresar un número válido entre 1 y 5.")
        continue  # 'continue' salta al siguiente ciclo del while sin ejecutar lo de abajo.

    # Estructura condicional para cada opción.
    if opcion == 1:
        actividad_tuplas()
    elif opcion == 2:
        actividad_diccionarios()
    elif opcion == 3:
        actividad_excepciones()
    elif opcion == 4:
        actividad_strings()
    elif opcion == 5:
        print("Saliendo del programa...")
        break  # Rompe el bucle 'while True' y termina el menú.
    else:
        print("Opción fuera de rango. Elige entre 1 y 5.")
