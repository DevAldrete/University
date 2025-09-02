"""
Importamos de la librería estándar "time" la función sleep
Esto nos permite pausar la ejecución del programa por X segundo
"""

from time import sleep

"""
Aquí vamos a construir la famosa "tabla pitagórica",
es decir, la tabla de multiplicar del 1 al 10.

La idea general:
- Usaremos una LIST COMPREHENSION ANIDADA para construir la tabla.
- Cada fila representa un número fijo (j) multiplicado por todos los números del 1 al 10.
- Cada columna es el resultado de multiplicar (i * j), pero usando nuestra función.
"""


def multiplicar(num1, n):
    """
    Esta función `multiplicar` hace lo mismo que el operador * (multiplicación),
    pero sin usarlo directamente.

    Parámetros:
    - num1: el número base que queremos multiplicar
    - n: cuántas veces se va a "sumar" el número base

    Lógica:
    - Inicializamos result = 0
    - Luego sumamos num1 a result, tantas veces como diga n
    - Esto imita el proceso matemático: multiplicar es sumar repetidamente
    """
    result = 0
    for _ in range(n):
        # usamos un bucle que se repite "n" veces
        result += num1  # cada vez le sumamos num1 al acumulador
    return result


"""
Ahora construimos la tabla.

Explicación paso por paso:
- range(1, 11) → genera los números del 1 al 10 (porque el 11 no se incluye).
- [multiplicar(i, j) for i in range(1, 11)]
      → genera UNA FILA de la tabla, para un valor fijo de j.
        Cada elemento de esa fila es el resultado de multiplicar i * j.
- El segundo for (for j in range(1, 11)) repite el proceso para todos los valores de j (1 al 10),
  por lo tanto obtenemos todas las filas.
"""

tabla = [[multiplicar(i, j) for i in range(1, 11)] for j in range(1, 11)]


def mostrar_tabla():
    """
    Función para mostrar en pantalla la tabla de Pitágoras del 1 al 10.
    Cada fila corresponde a un número multiplicado del 1 al 10.
    """
    # Recorremos cada "fila" dentro de la variable tabla
    for valores in tabla:
        """
        Convertimos cada número de la fila en texto con str(valor)
        porque join SOLO puede unir strings
        "\t".join(...) -> une los elementos con un TABULADOR entre ellos
        Esto da formato bonito como tabla
        """
        print("\t".join([str(valor) for valor in valores]))


def multiplicar_usando_tabla(num1, num2):
    """
    Función que devuelve el producto entre dos números,
    utilizando la tabla ya precalculada.
    """

    # El usuario ingresa valores del 1 al 10, pero los índices de la lista empiezan en 0. Por eso restamos 1 a cada número
    return tabla[num1 - 1][num2 - 1]


"""
"while True" significa que esto se repetirá para siempre
hasta que el usuario detenga manualmente el programa.
"""
while True:
    # Pausamos la ejecución 1 segundo
    sleep(1)

    # Mostramos título y la tabla completa
    print("---- Tabla de pitagoras del 1 al 10 ----")
    mostrar_tabla()

    """
    Solicitamos al usuario que ingrese dos números
    input() devuelve un string, así que usamos int() para convertirlo a número entero
    """
    usuario_num1 = int(input("Ingrese un numero del 1 al 10: "))
    usuario_num2 = int(input("Ingrese otro numero del 1 al 10: "))

    """
    Validamos que los números estén dentro del rango permitido (1 a 10)
    Si no lo están, mostramos un mensaje de error
    """
    if usuario_num1 < 1 or usuario_num1 > 10 or usuario_num2 < 1 or usuario_num2 > 10:
        print("\nError: Los numeros deben estar entre 1 y 10.")
        """
        "continue" hace que el programa regrese al inicio del while
        y vuelva a pedir los números
        """
        continue

    # Si los números son válidos, mostramos el proceso
    print("\nMultiplicando...")

    """
    Usamos la función multiplicar() para obtener el producto
    f-string (f"texto {variable}") permite insertar variables dentro del strin
    """
    print(f"\nProducto: {multiplicar(usuario_num1, usuario_num2)}\n")
