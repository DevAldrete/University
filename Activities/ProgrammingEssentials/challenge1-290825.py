"""Reto para el viernes 29 de agosto
Analizar, comprender, corregir y completar el código de la función validar_clave"""


def validar_clave(usuario, contrasena):
    """
    Esta función busca al usuario, valida que la contraseña le corresponda.
    Si lo encontró, retorna True, y el nivel de privilegios que le corresponde.
    Si no lo encontró, retorna False y 0
    """
    usuarios = ["Root", "Admin", "Sysop"]
    claves = ["111", "222", "333"]
    privilegios = [1, 2, 2]

    if contrasena is claves[0] and usuario is usuarios[0]:
        return True, privilegios[0]
    elif contrasena is claves[1] and usuario is usuarios[1]:
        return True, privilegios[1]
    elif contrasena is claves[2] and usuario is usuarios[2]:
        return True, privilegios[2]
    else:
        return False, 0


login = input("Dame tu nombre de usuario: ")
clave = input("Contraseña: ")
valido, nivel = validar_clave(login, clave)
if valido:
    print("Bienvenido")
    if nivel == 1:
        print("Tienes todos los privilegios")
    else:
        print("Tienes privilegios limitados")
else:
    print("Acceso no permitido")
print("Fin del programa")
