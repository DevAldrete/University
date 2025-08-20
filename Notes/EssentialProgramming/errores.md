## Tipos de Errores en Python

1. Sintacticos: se generan al momento de escribir un programa y ocurren porque las palabras no forman una sentencia válida para Python; por ende, esta clase de inconvenientes se depuran gracias a los editores disponibles en la herramienta, en este caso, IDLE.

2. Semanticos: establecen si una sentencia tiene sentido y se ejecuta normalmente, es decir, detectan si el programa no realiza lo que el especialista desea que lleve a cabo; por esta razón, algunos autores los denominan errores de lógica.

3. En tiempo de ejecucion: suceden cuando un programa activo se detiene abruptamente por algún motivo, así que Python suele indicar el tipo de error de forma similar a como lo hace con las fallas anteriores.

2) Semanticos: El compilador te comenta si una sentencia tiene sentido, o pareciera que no hiciese lo que pensaste que fuese a hacer, un problema de logica. Ejemplo: Por ejemplo, si quisiese sacar el promedio de una lista de numeros, podria haber un problema si en lugar de declarar el promedio como: suma_total_numeros / longitud_de_lista; lo declarase como: suma_total_numeros / (longitud_de_lista - 1), no hay crash, no hay error de sintaxis, pero hay un error de logica, no es lo que tu querias.

3) Fase de depuracion: Correcion

- Determina el tipo de error (de sintaxis, semántico, lógico o de ejecución) para resolverlo apropiadamente.
- Realiza el diagrama de flujo y el algoritmo con las correcciones que vas a realizar; así, te asegurarás de que tu programación cumpla con la calidad requerida.
- Esta etapa del proceso es de las más laboriosas y complicadas, sobre todo si las anteriores no se realizaron con detenimiento.

4. Correr el ejemplo de suma los primeros 10 numeros naturales, o la ultima secuencia del ciclo for:

total = 0
for i in range(11):
total += i

print(total)
