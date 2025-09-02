# 1) Explicar cada uno de los siguientes metodos de una lista
"""
### `append()`
- **¿Para qué sirve?**
  Agrega un elemento al final de la lista.

- **Parámetros:**
  - `element`: cualquier objeto que quieras añadir (número, string, lista, etc.)

- **Ejemplo:**
  ```python
  lista = [1, 2, 3]
  lista.append(4)
  # Resultado: [1, 2, 3, 4]
  ```


### `insert()`
- **¿Para qué sirve?**
  Inserta un elemento en una posición específica de la lista.

- **Parámetros:**
  - `index`: posición donde se insertará el elemento
  - `element`: el objeto que se quiere insertar

- **Ejemplo:**
  ```python
  lista = [1, 2, 4]
  lista.insert(2, 3)
  # Resultado: [1, 2, 3, 4]
  ```


### `remove()`
- **¿Para qué sirve?**
  Elimina la primera aparición de un elemento específico en la lista.

- **Parámetros:**
  - `element`: el valor que se desea eliminar

- **Ejemplo:**
  ```python
  lista = [1, 2, 3, 2]
  lista.remove(2)
  # Resultado: [1, 3, 2]
  ```

### `reverse()`
- **¿Para qué sirve?**
  Invierte el orden de los elementos de la lista **in-place** (modifica la lista original).

- **Parámetros:**
  - No tiene parámetros.

- **Ejemplo:**
  ```python
  lista = [1, 2, 3]
  lista.reverse()
  # Resultado: [3, 2, 1]
  ```


### `sort()`
- **¿Para qué sirve?**
  Ordena los elementos de la lista **in-place**. Por defecto, en orden ascendente.

- **Parámetros opcionales:**
  - `key`: función que especifica un criterio de ordenación
  - `reverse`: `True` para orden descendente, `False` para ascendente (por defecto)

- **Ejemplo básico:**
  ```python
  lista = [3, 1, 2]
  lista.sort()
  # Resultado: [1, 2, 3]
  ```

- **Ejemplo avanzado con `key`:**
  ```python
  palabras = ['banana', 'kiwi', 'manzana']
  palabras.sort(key=len)
  # Resultado: ['kiwi', 'banana', 'manzana']
  ```
"""

# 2) Un programa que utilice listas, para que, cuando le demos dia y mes de una fecha, el programa nos calcule y muestre:
# Cuantos dias tiene ese mes,
# Cuantos dias han transcurrido en lo que va del ano

# meses = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
# mapped_meses = {
#     "Enero": 0,
#     "Febrero": 1,
#     "Marzo": 2,
#     "Abril": 3,
#     "Mayo": 4,
#     "Junio": 5,
#     "Julio": 6,
#     "Agosto": 7,
#     "Septiembre": 8,
#     "Octubre": 9,
#     "Noviembre": 10,
#     "Diciembre": 11,
# }
#
# mes = input("El mes: ").capitalize()
# print(f"Dias del mes: {meses[mapped_meses[mes]]}")
# print(meses[: mapped_meses[mes]])
# dias_totales_antes_del_mes = sum(meses[: mapped_meses[mes]])
# dias = int(input("El dia: "))
# print(
#     f"Dias que han transcurrido en lo que va del ano: {dias_totales_antes_del_mes + dias}"
# )

# 3) Se tiene una lista para vacaciones que da derecho a una noche de baile, paseo en parachute y paseo por los manglares

derechos = ["baile", "parachute", "manglares"]

while True:
    print("\n---- Bienvenido a vacaciones XYZ ----")
    print("1. Noche de Baile")
    print("2. Paseo con Parachute")
    print("3. Paseo por Manglares")
    print("4. Salir\n")

    option = int(input("Que le gustaria hacer? "))

    if option == 1:
        if "baile" not in derechos:
            print("Usted no posee el derecho a pasar una Noche de Baile.")
            continue

        print("Disfrute su Noche de Baile!")
        derechos.remove("baile")
    elif option == 2:
        if "parachute" not in derechos:
            print("Usted no posee el derecho a un Paseo con Parachute.")
            continue

        print("Disfrute de su Paseo con Parachute!")
        derechos.remove("parachute")
    elif option == 3:
        if "manglares" not in derechos:
            print("Usted no posee el derecho a un Paseo por lo Manglares.")
            continue
        print("Disfrute de su Paseo por los Manglares!")
        derechos.remove("manglares")
    elif option == 4:
        break
    else:
        print("Opcion no valida!")
        continue

print("Saliendo de Vacaciones XYZ...")
