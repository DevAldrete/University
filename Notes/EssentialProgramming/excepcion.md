### 1. ¿Qué es una excepción personalizada en Python?

Una **excepción personalizada** es una clase que tú defines para representar errores específicos en tu programa. En lugar de usar solo las excepciones estándar como `ValueError` o `TypeError`, puedes crear tus propias excepciones para manejar situaciones particulares con mayor claridad y control.

---

### 2. ¿Cómo se crea una excepción personalizada?

Generalmente se crea definiendo una nueva clase que hereda de `Exception` o alguna subclase de esta. Ejemplo:

```python
class SaldoInsuficienteError(Exception):
    pass
```

También puedes personalizar el mensaje de error:

```python
class SaldoInsuficienteError(Exception):
    def __init__(self, mensaje):
        super().__init__(mensaje)
```

---

### 3. ¿Qué papel tiene la palabra reservada `raise`?

La palabra clave `raise` se usa para **lanzar** (o "elevar") una excepción. Puede ser una excepción estándar o personalizada. Es como decirle a Python: “¡Ocurrió un problema, detén el flujo normal y maneja esto!”

---

### Código completo con excepción personalizada

```python
'''
Definimos una clase de excepción personalizada que hereda de Exception.
Esto nos permite lanzar errores específicos con mensajes más claros.
'''
class SaldoInsuficienteError(Exception):  # Heredamos de la clase base Exception
    '''
    Constructor de la clase. Se ejecuta al crear una instancia de SaldoInsuficienteError.
    El parámetro 'mensaje' tiene un valor por defecto.
    '''
    def __init__(self, mensaje="El saldo es insuficiente para realizar el pago."):
        # Llamamos al constructor de la clase padre para inicializar el mensaje
        super().__init__(mensaje)

'''
Bloque principal del programa. Usamos try-except para manejar errores de forma controlada.
'''
try:
    # Solicitamos al usuario que ingrese su saldo y lo convertimos a float
    saldo = float(input("Ingrese su saldo: "))  # input() devuelve str, float() lo convierte a número decimal

    # Solicitamos el monto a pagar
    precio = float(input("Dame el total a pagar: "))

    # Verificamos si el saldo es suficiente
    if precio > saldo:
        # Si no lo es, lanzamos nuestra excepción personalizada con un mensaje formateado
        raise SaldoInsuficienteError(f"No puedes pagar ${precio:.2f} con un saldo de ${saldo:.2f}")

    # Si no se lanza excepción, se realiza el pago
    print("Pago realizado con éxito.")

# Capturamos específicamente la excepción SaldoInsuficienteError
except SaldoInsuficienteError as e:
    # Mostramos el mensaje de error contenido en la excepción
    print(f"Error: {e}")

# Este mensaje se muestra siempre, ocurra o no una excepción
print("Fin del programa")
```
