num_patients = 3

while num_patients > 0:
    peso = float(input(f"Cual es el peso para el pasiente numero {num_patients}: "))
    estatura = float(input(f"Cual es la estatura del pasiente numero {num_patients}: "))

    imc = peso / (estatura**2)

    if imc >= 18.5 and imc < 25:
        print("Tienes un peso normal")
    elif imc >= 25 and imc < 30:
        print("Tienes sobrepeso")
    elif imc >= 30:
        print("Tienes obesidad")
    else:
        print("No considerado. IMC anormal.")

    num_patients -= 1
