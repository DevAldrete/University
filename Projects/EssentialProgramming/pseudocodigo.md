Definir listaLibros = ["Don Quijote", "1984", "Cien años de soledad"]
Definir prestamos = diccionario (usuario -> lista de libros)

Repetir
Mostrar menú
Leer opcion
Si opcion == 1:
Mostrar libros disponibles
Si opcion == 2:
Pedir usuario y libro
Si libro en listaLibros y usuario tiene < 3 prestamos
Quitar libro de listaLibros
Agregar libro a prestamos[usuario]
Sino
Mostrar "No se puede prestar"
Si opcion == 3:
Pedir usuario y libro
Si libro en prestamos[usuario]
Quitar libro de prestamos[usuario]
Agregar libro a listaLibros
Sino
Mostrar "Error"
Hasta opcion == 4
