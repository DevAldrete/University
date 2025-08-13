## Pedir horas y minutos (SALIDA Y ENTRADA)

entrada_hora = input("Hora de la entrada: ")
entrada_minutos = input("Minutos de la entrada: ")

salida_hora = input("Hora de la salida: ")
salida_minutos = input("Minutos de la salida: ")

total_salida = float(salida_hora) * 60 + float(salida_minutos)
total_entrada = float(entrada_hora) * 60 + float(entrada_minutos)

# total_minutos = 60 - (total_salida % 60 - total_entrada % 60)
total_horas = total_salida / 60 - total_entrada / 60
total_minutos = (total_horas - int(total_horas)) * 60
print(f"Permanecio: {int(total_horas)}:{int(total_minutos)}")
# horas_estancia = float(salida_hora) - float(entrada_hora)
# minutos_estancia = float(entrada_minutos) - float(salida_minutos)
