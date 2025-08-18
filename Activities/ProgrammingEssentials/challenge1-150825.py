peso = float(input("Cual es tu peso: "))
estatura = float(input("Cual es tu estatura: "))

imc = peso / (estatura**2)

if imc >= 18.5 and imc < 25:
    print("Tienes un peso normal")
elif imc >= 25 and imc < 30:
    print("Tienes sobrepeso")
elif imc >= 30:
    print("Tienes obesidad")
else:
    print("No considerado.")
