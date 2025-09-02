CMAM = 0.01  # Centimetros a Metros
PIAPU = 12  # Pies a Pulgadas
YAAPI = 3  # Yardas a Pies
PULGADAS = 2.54  # Pulgadas


def convertir_medida(
    medida: float, actual: str = "pulgadas", destino: str = "centimetros"
) -> float:
    """
    Args:
        actual: str -> Unidad Actual
    Returns:
        float: El resultado en Metros o Centimetros
    """
    resultado = medida * PULGADAS

    if actual.lower() == "pies":
        resultado *= PIAPU

    if actual.lower() == "yardas":
        resultado *= PIAPU * YAAPI

    if destino.lower() == "metros":
        resultado *= CMAM

    return resultado


while True:
    medida = input("Dame el número de la medida original [q, quit o exit para salir]: ")
    if medida in ["q", "exit", "quit"]:
        break
    medida = float(medida)
    UnidadActual = str(
        input("Dime si está en Yardas, Pies o Pulgadas [q, quit o exit para salir]: ")
    )
    if UnidadActual in ["q", "exit", "quit"]:
        break
    UnidadDestino = str(
        input(
            "Dime a que lo quieres convertir, Metros o Centimetros [q, quit o exit para salir]: "
        )
    )
    if UnidadDestino in ["q", "exit", "quit"]:
        break

    medida2 = None

    if UnidadActual.lower() in [
        "yardas",
        "pies",
        "pulgadas",
    ] and UnidadDestino.lower() in ["centimetros", "metros"]:
        medida2 = convertir_medida(medida, UnidadActual, UnidadDestino)
        # if UnidadActual.lower() == "yardas":
        #     if UnidadDestino.lower() == "centimetros":
        #         medida2 = medida * YAAPI * PIAPU * PULGADAS
        #     elif UnidadDestino.lower() == "metros":
        #         medida2 = medida * YAAPI * PIAPU * PULGADAS * CMAM
        #     else:
        #         print("Unidad desconocida de destino.")
        #         break
        # elif UnidadActual.lower() == "pies":
        #     if UnidadDestino.lower() == "centimetros":
        #         medida2 = medida * PIAPU * PULGADAS
        #     elif UnidadDestino.lower() == "metros":
        #         medida2 = medida * PIAPU * PULGADAS * CMAM
        #     else:
        #         print("Unidad desconocida de destino.")
        #         break
        # elif UnidadActual.lower() == "pulgadas":
        #     if UnidadDestino.lower() == "centimetros":
        #         medida2 = medida * PULGADAS
        #     elif UnidadDestino.lower() == "metros":
        #         medida2 = medida * PULGADAS * CMAM
        #     else:
        #         print("Unidad desconocida de destino.")
        #         break

    else:
        print("Unidades no reconocidas.")
        continue

    if medida2 is not None:
        print(f"Resultado en {medida2}")
    else:
        print("Ha habido un error en encontrar la medida deseada.")
        break

print("Fin del programa")
