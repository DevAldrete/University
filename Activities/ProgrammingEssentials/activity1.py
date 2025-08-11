### Importamos los modulos necesarios para nuestro programa.
### Importamos un tipo de dato del modulo typing para ayudarnos con el autocompletado del IDE.
from typing import Dict

### Importamos un logger de la libreria logging para tener un programa limpio al final en "produccion", ya que podemos desactivar
### los loggers cuando queramos, a diferencia de los prints.
from logging import Logger

### Esto simplemente es una funcion que me gusta importar debido a que es un print pero "mejor" y mas bonito (esto se puede ignorar)
from pprint import pprint as print

### Inicializamos un simple logger que toma el parametro de una variable global especial llamada __name__ que se refiere al nombre del modulo o fichero actual.
logger = Logger(__name__)


def main():
    ### Realizamos un tracking de las plataformas o redes sociales, etc. que nos dara el usuario. No nos limitamos a obtener solo 5, si no las que sean necesarias, podriamos considerar poner limites
    ### Debido a que una persona no puede ver tantas plataformas que quiera debido al limite de un dia, pero esto podria ser expandido al registrar la fecha y de esa manera tambien tendriamos
    ### la oportunidad de hacer un tracking de lo que hacemos durante toda la semana, mes, etc.
    tracking: Dict[
        str, float
    ] = {}  ### Utiliza tipado para ayuda en el autocompletado del IDE, no es necesario, pero es una buena practica para que el IDE sepa que tipo de datos se espera en el diccionario.

    ### Loop infinito para obtener los datos necesarios del usuario sin limites
    while True:
        ### Le pedimos al usuario que ingrese su plataforma
        platform = input(
            "\nCual plataforma o red social gustas tener un registro de? Plataforma: "
        )

        ### Le pedimos al usuario que ingrese las horas que dedico a la plataforma anterior que ingreso
        userInput = input(
            "\nIngresa la/las horas que hayas dedicado a esa actividad o 'listo' para terminar el programa): "
        )

        ### Intentamos ejecutar el codigo de este bloque codigo, que yo espero que de error debido a que si el usuario ingresa listo o cualquier otra cosa que no se peuda convertir a float, entonces
        ### manejamos el error y soltamos un ValueError y rompemos el loop infinito de while.
        try:
            ### Intentamos cambiar de string a float el input del usuario, debido a que las horas deben ser floats para ser sumadas o realizar operaciones en ellas de manera correcta
            number: float = float(userInput)

            ### Hacemos uso del diccionario para registrar la plataforma y la hora que nos dio el usuario y utilizarla despues
            tracking[platform] = number

            ### Volvemos a hacer el mismo proceso desde el while True

        ### Si ocurre un error, que yo tengo pensado que seria simplemente no dar la hora, sino, un string, y este no se podria transformar a float, lo que nos daria un error
        ### Por lo que lo atrapamos o manejamos utilizando try-except (o try-catch pattern) con un ValueError, que es el error que se lanza cuando no se puede convertir un string a float.
        except ValueError as e:
            print("Intentando calcular con lo que se tiene...")

            ### Rompemos el loop sin lanzar el error (con la keyword raise) debido a que esto romperia el programa
            break

    ### Checamos si nuestro registro no esta vacio, si esta vacio, simplemente retornamos 0 y terminamos el programa
    if len(tracking) == 0:
        return 0

    ### Inicializamos una variable para almacenar el tiempo total que se ha dedicado a las plataformas o redes sociales
    total_time: float = 0

    ### Empezamos un nuevo loop finito a una lista de tuplas con los valores del tipado de tracking (str, float)
    ### Esto con la meta de sumar las horas de cada plataforma en la variable total_time y obtener las horas totales dedicadas a las plataformas
    for idx, value in tracking.items():
        logger.info(f"Tracking {idx}...")

        ### Aqui hacemos una suma del valor a total_time, y redeclaramos la variable para no perder el valor anterior de total_time
        ### Esto seria el equivalente de usar total_time = total_time + value
        total_time += value

    ### Mostramos los valores del registro para temas de debugging de nuestra aplicacion en caso de ser necesario
    print(tracking)

    ### Mostramos cual ha sido el tiempo total dedicado a las plataformas o redes sociales
    print(f"\nYour total time: {total_time:.2f}\n")

    ### Calculamos el porcentaje del dia que se ha dedicado a las plataformas o redes sociales, considerando que un dia tiene 24 horas
    percentage = (total_time / 24) * 100

    ### Y por ultimo, mostramos el porcentaje del dia que se ha dedicado a las plataformas o redes sociales
    print(
        f"El porcentaje del dia que has tomado por estas plataformas o aplicaciones es del: {(percentage):.2f}"
    )


### Esto lo hago principalmente como buena practica, ya que solo se ejectura este codigo de la funcion main(), si se ejecuta el modulo o fichero directamente (python3.xx activity1.py)
if __name__ == "__main__":
    ### Ejecutamos la funcion main() para iniciar el programa
    main()
