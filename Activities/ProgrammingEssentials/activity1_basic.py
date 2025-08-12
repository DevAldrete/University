### Pedimos el tiempo de cada plataforma de manera ordenada, no le damos nombre ya que solo estamos interesados en encontrar
### el tiempo utilizado en total de todas las plataformas y el porcentaje del dia utilizado
plataforma1 = input("Dame el tiempo utilizado en la plataforma 1: ")
plataforma2 = input("Dame el tiempo utilizado en la plataforma 2: ")
plataforma3 = input("Dame el tiempo utilizado en la plataforma 3: ")
plataforma4 = input("Dame el tiempo utilizado en la plataforma 4: ")
plataforma5 = input("Dame el tiempo utilizado en la plataforma 5: ")

### Asumiendo que siempre pasara un numero o valor compatible para ser transformado desde string a float
### Esto puede causar errores y causar el crash del programa, por lo que se recomienda utilizar try-catch pattern o try-except
tiempo_total = (
    float(plataforma1)
    + float(plataforma2)
    + float(plataforma3)
    + float(plataforma4)
    + float(plataforma5)
)

### Mostramos el tiempo total que tenemos entre las 5 plataformas
print("\nTiempo total: ", tiempo_total)

### Calculamos el porcentaje del dia dividiendo entre el total de horas (la suma total) de las plataformas y sacamos el porcentaje multiplicando por 100
porcentaje_del_dia = (tiempo_total / 24) * 100

### Mostramos el porcentaje del dia utilizado a partir del calculo que hicimos utilizando el tiempo_total
print("\nPorcentaje del dia: ", porcentaje_del_dia)
