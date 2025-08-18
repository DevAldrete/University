# Elabora un programa que realice el cálculo del precio de
# entrada para los visitantes que desean recorrer el
# Museo de Antropología e Historia de tu ciudad, el cual debe considerar los siguientes descuentos:
# Adulto Mayor - 12%
# Profesor - 10%
# Estudiante - 10%
# El precio de entrada es de $30 para menores de edad y $45 para mayores de 18 años, mientras que los niños menores de tres años no pagan boleto.

### Empezamos por pedir al usuario cuantos visitantes son para poder utilizar un for-loop
num_visitantes = int(input("Cuantos visitantes son? "))

### Aqui almacenaremos los costos de cada visitante
### Ya que al final de cada loop guardamos el costo final por visitante aqui mismo para posteriormente
### Mostrarlos por un loop al final del programa!
costos_por_visitante = []

### Loopeamos a traves de un rango de visitantes (esto simplemente es una lista del 0 al numero de vistantes)
### Esto con la finalidad de solo determinar cuantas veces realmente se va a repetir el loop
### Ademas, guardamos el numero del visitante del arreglo de rangos para poder identificarlos y no confundir al usuario
for num in range(num_visitantes):
    ### Pedimos la edad del visitante {num} para posteriormente identificar si les corresponde un boleto de menor de edad
    ### O mayor de edad
    edad = int(input(f"Cual es la edad del visitante {num + 1}: "))

    ### Aqui hacemos un simple check de que la edad sea valida, si no,
    ### se tomara un valor por defecto de 18 anos para evitar problemas en el programa
    if edad < 0:
        print("Edad no valida, se tomara su edad como mayor de edad.")
        edad = 18

    ### El tipo de visitante se lo pedimos al usuario para determinar el descuento que se le aplicara
    ### Le decimos las opciones que hay para evitar problemas
    tipo_visitante = input(
        "Que tipo de visitnate es [adulto mayor | profesor | estudiante ]: "
    )

    ### Aqui definimos las variables que usaremos para calcular el costo final del boleto
    costo_del_boleto = 0
    descuento = 0

    ### El tipo de visitante lo convertimos a minusculas para poder comparar correctamente en el caso que el
    ### usuario halla escrito mal alguna letra en mayusculas
    ### Y hacemos una comparacion con la cadena de texto adulto mayor para identificar el descuento que se le aplicara
    if tipo_visitante.lower() == "adulto mayor":
        costo_del_boleto = 45
        descuento = 0.12
    ### De igual manera hacemos otra comparacion con la cadena de texto profesor para determinal el descuento correcto
    elif tipo_visitante.lower() == "profesor":
        costo_del_boleto = 45
        descuento = 0.10
    ### Finalmente hacemos la comparacion con la cadena de texto estudiante para determinar el descuento correcto
    elif tipo_visitante.lower() == "estudiante":
        ### Esta vez si nos importa la edad, ya que un estudiante puede ser menor o mayor de edad
        ### Y esto para identificar el costo correcto del boleto
        if edad < 18:
            costo_del_boleto = 30
        else:
            costo_del_boleto = 45
        descuento = 0.10

    ### Este else se ejecutara en el caso que el tipo de visitante no sea ninguno de los anteriores
    ### Si asi es el caso, simplemente se cobrara el costo completo del boleto ya que no se pudo identificar un tipo de visitante correcto
    else:
        ### Mostramos un mensaje al usuario para informarle que el tipo de visitante no es reconocido
        print(
            "Tipo de visitante no reconocido, se cobrara el costo completo del boleto"
        )
        ### Hacemos un check de la edad para determinar el costo correcto del boleto
        if edad < 18:
            costo_del_boleto = 30
        else:
            costo_del_boleto = 45

        ### Se calcula directamente el final costo del boleto sin descuento aplicado
        final_costo_del_boleto = costo_del_boleto
        continue

    ### Se calcula el costo final del boleto con el descuento aplicado
    final_costo_del_boleto = costo_del_boleto - (costo_del_boleto * descuento)
    ### Se almacena el costo final del boleto en la lista que habiamos definido arriba, esto se hace por practicidad
    costos_por_visitante.append(final_costo_del_boleto)

### Al final del programa, se muestran los costos finales de cada visitante
### haciendo un loop por cada costo dentro de la lista costo_por_visitante
for costo in costos_por_visitante:
    print(f"El costo final del boleto es: ${costo:.2f}")
