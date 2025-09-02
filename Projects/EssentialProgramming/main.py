"""
Sistema de gestión de préstamos de libros en una biblioteca escolar

Objetivo:
Digitalizar el proceso de préstamos y devoluciones de libros, 
que actualmente se hace a mano en una libreta.

Problemas a resolver:
- No existe registro digital de qué usuario tiene qué libro.
- No se controlan fechas ni límites de libros prestados.
- Puede haber préstamos duplicados de un mismo libro.

Reglas del negocio:
1. Cada usuario puede llevarse máximo 3 libros a la vez.
2. Un libro solo puede ser prestado si está disponible.
3. Cuando un libro se devuelve, vuelve a la lista de disponibles.
4. El sistema debe mostrar los libros disponibles.
5. Se pueden agregar libros nuevos al inventario.
"""

# DATOS DEL SISTEMA

# Lista de libros disponibles en la biblioteca
# Cada elemento es un texto (string) con el título de un libro
libros_disponibles = ["Drácula", "El Principito", "Cien años de soledad", "Alicia en el país de las maravillas"]

# Diccionario que guarda los préstamos
# Clave: nombre del usuario
# Valor: lista de libros prestados
prestamos = {}

# BUCLE PRINCIPAL

# El bucle while True mantiene el programa en ejecución
# hasta que el usuario elija salir
while True:
    print("\n---- MENÚ PRINCIPAL ----\n")
    print("1. Ver libros disponibles")
    print("2. Prestar libro")
    print("3. Devolver libro")
    print("4. Agregar libro al inventario")
    print("5. Salir")

    # input() siempre devuelve un string, lo convertimos a número con int()
    opcion = input("\nElige una opción: ")

    # Si no es un número válido, volver al menú
    if not opcion.isdigit():
        print("Opción inválida, escribe un número del 1 al 5.")
        continue

    opcion = int(opcion)  # Convertimos el texto a número entero

    # Opción 1: Ver libros
    if opcion == 1:
        print("\n--- Libros Disponibles ---")
        if len(libros_disponibles) == 0:
            print("No hay libros disponibles en este momento.")
        else:
            # enumerate() recorre la lista mostrando índice y valor
            for i, libro in enumerate(libros_disponibles):
                print(f"{i+1}. {libro}")

    
    # Opción 2: Prestar libro
    elif opcion == 2:
        usuario = input("\nNombre del usuario: ")
        libro = input("Título del libro a prestar: ")

        # Validar si el libro está disponible
        if libro not in libros_disponibles:
            print("Ese libro no está disponible o no existe en la biblioteca.")
        else:
            # Revisar cuántos libros tiene ya prestados el usuario
            if usuario in prestamos and len(prestamos[usuario]) >= 3:
                print("Este usuario ya tiene 3 libros prestados. No puede llevarse más.")
            else:
                # Eliminar el libro de los disponibles
                libros_disponibles.remove(libro)

                # Si el usuario no existía en el diccionario, lo agregamos
                if usuario not in prestamos:
                    prestamos[usuario] = [libro]
                else:
                    prestamos[usuario].append(libro)

                print(f"Se ha prestado el libro '{libro}' al usuario '{usuario}'.")

    
    # Opción 3: Devolver libro
    elif opcion == 3:
        usuario = input("\nNombre del usuario: ")
        libro = input("Título del libro a devolver: ")

        # Validar que el usuario exista en el diccionario
        if usuario not in prestamos:
            print("Este usuario no tiene libros prestados.")
        else:
            # Validar que realmente tenga ese libro
            if libro not in prestamos[usuario]:
                print("Ese libro no está registrado como prestado a este usuario.")
            else:
                # Quitar el libro de su lista
                prestamos[usuario].remove(libro)

                # Si después de devolver no le quedan libros, eliminamos su entrada
                if len(prestamos[usuario]) == 0:
                    del prestamos[usuario]

                # Agregar el libro de nuevo a la lista de disponibles
                libros_disponibles.append(libro)

                print(f"El usuario '{usuario}' ha devuelto el libro '{libro}'.")

    
    # Opción 4: Agregar libro
    elif opcion == 4:
        nuevo_libro = input("\nTítulo del nuevo libro: ")

        # Validamos que no esté duplicado
        if nuevo_libro in libros_disponibles:
            print("Ese libro ya está en el inventario.")
        else:
            libros_disponibles.append(nuevo_libro)
            print(f"El libro '{nuevo_libro}' ha sido agregado al inventario.")

    
    # Opción 5: Salir
    elif opcion == 5:
        print("Saliendo del sistema...")
        break  # break rompe el bucle while y termina el programa

    
    # Opción inválida
    else:
        print("Opción no válida. Elige entre 1 y 5.")

