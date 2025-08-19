"""
Elabora un programa que realice el cálculo del precio de
entrada para los visitantes que desean recorrer el
Museo de Antropología e Historia de tu ciudad.

Descuentos:
  - Adulto mayor: 12%
  - Profesor: 10%
  - Estudiante: 10%

Precios base:
  - Niños menores de 3 años: Gratis
  - Menores de edad (3 a 17): $30
  - Adultos (18 en adelante): $45
"""

# Pedimos al usuario cuántos visitantes son
num_visitantes = int(input("¿Cuántos visitantes son? "))

# Aquí almacenaremos los costos de cada visitante
costos_por_visitante = []

# Iteramos según la cantidad de visitantes
for num in range(num_visitantes):
    # Pedimos la edad del visitante actual
    edad = int(input(f"¿Cuál es la edad del visitante {num + 1}? "))

    # Si la edad es inválida, asumimos adulto (18 años)
    if edad < 0:
        print("Edad no válida, se tomará como mayor de edad.")
        edad = 18

    # Pedimos el tipo de visitante (adulto mayor, profesor, estudiante, etc.)
    tipo_visitante = input(
        "¿Qué tipo de visitante es? [adulto mayor | profesor | estudiante]: "
    )

    # Variables para el cálculo del boleto
    costo_del_boleto = 0
    descuento = 0

    # Convertimos el texto a minúsculas con .lower()
    # Esto nos permite comparar sin importar cómo lo escribió el usuario, ya que lo convertimos a minúsculas
    if tipo_visitante.lower() == "adulto mayor":
        costo_del_boleto = 45
        descuento = 0.12

    elif tipo_visitante.lower() == "profesor":
        costo_del_boleto = 45
        descuento = 0.10

    elif tipo_visitante.lower() == "estudiante":
        # Los estudiantes pueden ser menores o mayores de edad,
        # por lo tanto revisamos su edad para el precio base
        if edad < 18:
            costo_del_boleto = 30
        else:
            costo_del_boleto = 45
        descuento = 0.10

    else:
        # Si no se reconoce el tipo de visitante, no se aplica descuento
        print("Tipo de visitante no reconocido, se cobrará el costo completo.")
        if edad < 3:
            costo_del_boleto = 0
        elif edad < 18:
            costo_del_boleto = 30
        else:
            costo_del_boleto = 45

        final_costo_del_boleto = costo_del_boleto
        costos_por_visitante.append(final_costo_del_boleto)
        continue

    # Calculamos el costo final aplicando el descuento
    final_costo_del_boleto = costo_del_boleto - (costo_del_boleto * descuento)

    # Guardamos el costo final en la lista
    costos_por_visitante.append(final_costo_del_boleto)

# Mostramos los costos de todos los visitantes
for costo in costos_por_visitante:
    print(f"El costo final del boleto es: ${costo:.2f}")
