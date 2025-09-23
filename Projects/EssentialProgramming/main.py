"""
Sistema de gestión de préstamos de libros en una biblioteca.

Este script implementa una solución completa para la administración de una
biblioteca, permitiendo gestionar un catálogo de libros y el préstamo de
estos a usuarios.

El sistema está diseñado para ser robusto y fácil de usar desde la consola,
ofreciendo una experiencia interactiva a través de un menú de opciones.

Características clave:
- Modelado de Datos con Pydantic: Se utilizan clases que heredan de BaseModel
  para asegurar que todos los datos (libros, usuarios, préstamos) tengan una
  estructura y tipos de datos consistentes. Esto previene errores comunes
  y facilita la validación automática.
- Manejo Inteligente de Fechas con Pendulum: La librería pendulum se usa
  para manejar las fechas de préstamo y devolución, simplificando cálculos
  de multas y manejo de zonas horarias.
- Persistencia de Datos: El estado completo de la biblioteca (catálogo y
  usuarios) se guarda en un único archivo JSON, permitiendo que los datos
  perduren entre sesiones.
- Búsqueda por Prefijo: Facilita la selección de libros y usuarios
  introduciendo solo los primeros caracteres de su ID único.
- Lógica de Negocio Completa:
    - Cálculo automático de multas por retraso ($15/día).
    - Límite de 3 libros por usuario para asegurar una distribución justa.
    - Bloqueo de nuevos préstamos si un usuario tiene multas pendientes.
    - Gestión completa de CRUD (Crear, Leer, Actualizar, Eliminar) para
      libros y usuarios.
"""

import json  # Módulo para trabajar con archivos JSON (JavaScript Object Notation).
from typing import (
    Dict,
    List,
    Any,
    Optional,
)  # Proporciona "type hints" (pistas de tipo) para mejorar la legibilidad y el análisis estático del código.
import uuid  # Módulo para generar identificadores únicos universales (UUIDs), perfectos para IDs de libros y usuarios.
import pendulum as pm  # Una librería que facilita el manejo de objetos de fecha y hora (datetime).
from pydantic import (
    BaseModel,  # Clase base de Pydantic para crear modelos de datos que se validan automáticamente.
    Field,      # Permite añadir metadatos y validaciones a los campos de un modelo Pydantic.
)

# --- Constantes de configuración ---
"""
Definir estas variables como constantes globales hace que el código sea más fácil de leer y modificar.
Si en el futuro se necesita cambiar la ruta del archivo o las reglas de negocio, solo se cambia aquí.
"""
RUTA_JSON = "biblioteca.json"  # Nombre del archivo donde se guardarán todos los datos.
DIAS_PRESTAMO = 7  # Periodo de gracia estándar para un préstamo antes de generar multas.
MULTA_POR_DIA = 15.0  # Costo en pesos mexicanos por cada día de retraso en la devolución.
LIMITE_LIBROS = 3  # Cantidad máxima de libros que un usuario puede tener prestados simultáneamente.


# --- Modelos de Datos (usando Pydantic) ---
"""
Los modelos de Pydantic son como "planos" para nuestros datos.
Definen qué campos debe tener un objeto, de qué tipo deben ser, y si tienen valores por defecto.
Pydantic se encarga de validar que cualquier dato que creemos o carguemos cumpla con estas reglas.
"""

class Libro(BaseModel):
    """
    Representa un libro en el catálogo de la biblioteca.

    Esta clase define la estructura de un libro. Al heredar de BaseModel,
    Pydantic validará automáticamente cualquier instancia de Libro.

    Atributos:
        id (str): Identificador único del libro, generado automáticamente.
        nombre (str): Título del libro.
        disponible (bool): Indica si hay al menos una copia para prestar.
        cantidad (int): Número total de copias de este libro que posee la biblioteca.
    """

    # Field se usa para configurar opciones avanzadas para un atributo.
    # default_factory es una función que se llama para generar un valor por defecto
    # cuando se crea un objeto Libro sin proporcionar un id.
    # Aquí, usamos uuid.uuid4() para generar un ID único y aleatorio.
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    nombre: str
    disponible: bool
    cantidad: int


class Prestamo(Libro):
    """
    Representa un libro que ha sido prestado a un usuario.

    Esta clase hereda todos los atributos de Libro y añade información
    específica del préstamo, como las fechas. Esto evita duplicar código
    y mantiene una relación lógica clara: un préstamo es, fundamentalmente,
    un libro con contexto temporal.

    Atributos:
        fecha (str): Fecha y hora del préstamo en formato ISO 8601 (un estándar
                     internacional para representar fechas y horas).
        fecha_devolucion (str): Fecha y hora límite para devolver el libro sin multa.
    """

    fecha: str
    fecha_devolucion: str


class Usuario(BaseModel):
    """
    Representa a un usuario registrado en la biblioteca.

    Atributos:
        id (str): Identificador único del usuario, generado automáticamente.
        nombre (str): Nombre completo del usuario.
        libros (List[Prestamo]): Una lista que contiene los libros que el
                                 usuario tiene actualmente en préstamo.
                                 Por defecto, es una lista vacía.
        multa_pendiente (float): Monto total de la multa acumulada por el
                                 usuario. Por defecto, es 0.0.
    """

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    nombre: str
    libros: List[Prestamo] = []  # Valor por defecto: una lista vacía.
    multa_pendiente: float = 0.0 # Valor por defecto: 0.0.


# --- Lógica de la Biblioteca ---

class Biblioteca:
    """
    Clase principal que encapsula toda la lógica y los datos de la biblioteca.

    Actúa como el "motor" del sistema. Contiene las listas de libros y usuarios
    y proporciona métodos para interactuar con ellos (prestar, devolver, etc.).
    Almacenar todo dentro de una clase mantiene el código organizado y coherente.
    """

    def __init__(self) -> None:
        """
        Constructor de la clase Biblioteca.

        Al crear una nueva instancia de Biblioteca, este método se ejecuta
        automáticamente. Su principal tarea es intentar cargar los datos desde
        el archivo JSON. Si el archivo no existe o está vacío, inicializa
        las listas de libros y usuarios como vacías.
        """
        self.libros: List[Libro] = []
        self.usuarios: List[Usuario] = []

        # El "walrus operator" (:=) asigna el resultado de self.cargar_datos()
        # a la variable datos y, al mismo tiempo, verifica si datos no es None.
        if datos := self.cargar_datos():
            """
            Si se cargaron datos, usamos una "list comprehension" para convertir
            cada diccionario de libro/usuario del JSON en un objeto Pydantic.
            Libro.model_validate() es el método de Pydantic que toma un
            diccionario y lo convierte en una instancia de la clase Libro,
            validando todos los campos en el proceso.
            """
            self.libros = [Libro.model_validate(libro) for libro in datos.get("libros", [])]
            self.usuarios = [Usuario.model_validate(usuario) for usuario in datos.get("usuarios", [])]
        else:
            print("No se encontró un archivo de datos, se iniciará una biblioteca nueva.")

    def cargar_datos(self) -> Optional[Dict[str, Any]]:
        """
        Carga los datos de la biblioteca desde el archivo JSON.

        Maneja dos posibles errores comunes:
        1. FileNotFoundError: Si el archivo biblioteca.json no existe (por ejemplo,
           la primera vez que se ejecuta el programa).
        2. json.JSONDecodeError: Si el archivo existe pero está corrupto o mal
           formateado, lo que impide que se pueda interpretar como JSON.

        Retorna:
            Un diccionario con los datos si la carga es exitosa, o None si
            ocurre un error.
        """
        try:
            with open(RUTA_JSON, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return None  # No es un error, simplemente no hay datos guardados.
        except json.JSONDecodeError:
            print("Error: El archivo JSON está corrupto o mal formateado.")
            return None

    def guardar_datos(self) -> None:
        """
        Guarda el estado actual de la biblioteca en el archivo JSON.

        Este método se llama después de cada operación que modifica los datos
        para asegurar la persistencia. Convierte las listas de objetos
        Libro y Usuario en diccionarios compatibles con JSON usando
        el método .model_dump() de Pydantic antes de escribirlos en el archivo.
        """
        try:
            with open(RUTA_JSON, "w", encoding="utf-8") as f:
                # model_dump() convierte el objeto Pydantic a un diccionario de Python.
                datos = {
                    "libros": [libro.model_dump() for libro in self.libros],
                    "usuarios": [usuario.model_dump() for usuario in self.usuarios],
                }
                """
                json.dump escribe el diccionario en el archivo.
                indent=4 formatea el JSON para que sea legible por humanos.
                ensure_ascii=False permite guardar caracteres especiales como acentos.
                """
                json.dump(datos, f, indent=4, ensure_ascii=False)
        except IOError as e:
            print(f"Error al intentar guardar los datos en el archivo: {e}")

    # --- Métodos de Gestión de Libros ---

    def mostrar_catalogo(self) -> None:
        """Imprime en consola una lista formateada de todos los libros del catálogo."""
        items = self.libros
        print("\n--- Catálogo de Libros ---")
        if not items:
            print("No hay libros en el catálogo.")
            return
        for item in items:
            estado = "Disponible" if item.disponible else "Agotado"
            print(f"- ID: {item.id} | Nombre: {item.nombre} | Cantidad: {item.cantidad} ({estado})")

    def agregar_libro(self, nombre: str, cantidad: int) -> None:
        """
        Agrega un nuevo libro o actualiza la cantidad de uno existente.

        Args:
            nombre (str): Título del libro a agregar.
            cantidad (int): Número de copias a añadir.
        """
        # Primero, busca si el libro ya existe (ignorando mayúsculas/minúsculas).
        for libro in self.libros:
            if libro.nombre.lower() == nombre.lower():
                libro.cantidad += cantidad
                libro.disponible = libro.cantidad > 0 # Asegura que el estado sea correcto.
                print(f"Se agregaron {cantidad} copias de '{nombre}'. Cantidad total: {libro.cantidad}.")
                return # Termina la función para no agregarlo de nuevo.

        # Si el bucle termina sin encontrar el libro, se crea uno nuevo.
        nuevo_libro = Libro(nombre=nombre, cantidad=cantidad, disponible=cantidad > 0)
        self.libros.append(nuevo_libro)
        print(f"Libro '{nombre}' agregado al catálogo con {cantidad} copias.")

    def obtener_libro(self, libro_id: str) -> Optional[Libro]:
        """
        Busca un libro en el catálogo por su ID completo.

        Args:
            libro_id (str): El ID exacto del libro a buscar.

        Retorna:
            El objeto Libro si se encuentra, de lo contrario None.
        """
        for libro in self.libros:
            if libro.id == libro_id:
                return libro
        return None

    def modificar_libro(self, libro_id: str) -> bool:
        """
        Permite al usuario cambiar el nombre y/o la cantidad de un libro existente.

        Args:
            libro_id (str): ID del libro a modificar.

        Returns:
            True si el libro se modificó, False si no se encontró.
        """
        libro = self.obtener_libro(libro_id)
        if not libro:
            print("Error: No se encontró un libro con ese ID.")
            return False

        print(f"Modificando libro: '{libro.nombre}' (Cantidad actual: {libro.cantidad})")

        # Pide un nuevo nombre. Si el usuario presiona Enter, no se cambia.
        nuevo_nombre = input(f"Nuevo nombre (deja en blanco para mantener '{libro.nombre}'): ").strip()
        if nuevo_nombre:
            libro.nombre = nuevo_nombre
            print(f"Nombre del libro actualizado a '{libro.nombre}'.")

        # Pide una nueva cantidad. Usa un bloque try-except para manejar
        # el caso en que el usuario no introduzca un número válido.
        try:
            nueva_cantidad_str = input(f"Nueva cantidad (deja en blanco para mantener {libro.cantidad}): ").strip()
            if nueva_cantidad_str:
                nueva_cantidad = int(nueva_cantidad_str)
                if nueva_cantidad < 0:
                    print("Error: La cantidad no puede ser negativa.")
                else:
                    libro.cantidad = nueva_cantidad
                    libro.disponible = libro.cantidad > 0
                    print(f"Cantidad actualizada a {libro.cantidad}.")
        except ValueError:
            print("Entrada inválida. La cantidad no fue modificada.")

        return True

    def eliminar_libro(self, libro_id: str) -> bool:
        """
        Elimina un libro del catálogo por su ID.

        Args:
            libro_id (str): El ID del libro a eliminar.

        Retorna:
            True si el libro fue eliminado, False si no se encontró.
        """
        libro = self.obtener_libro(libro_id)
        if libro:
            self.libros.remove(libro)
            print(f"Libro '{libro.nombre}' eliminado correctamente.")
            return True
        print("Error: No se encontró un libro con ese ID.")
        return False

    # --- Métodos de Gestión de Usuarios ---

    def mostrar_usuarios(self) -> None:
        """Imprime en consola una lista formateada de todos los usuarios registrados."""
        items = self.usuarios
        print("\n--- Lista de Usuarios ---")
        if not items:
            print("No hay usuarios registrados.")
            return
        for item in items:
            print(f"- ID: {item.id} | Nombre: {item.nombre}")

    def crear_usuario(self, nombre: str) -> Usuario:
        """
        Crea un nuevo usuario y lo añade a la lista de la biblioteca.

        Args:
            nombre (str): Nombre del nuevo usuario.

        Retorna:
            El objeto Usuario recién creado.
        """
        nuevo_usuario = Usuario(nombre=nombre)
        self.usuarios.append(nuevo_usuario)
        print(f"Usuario '{nombre}' creado con ID: {nuevo_usuario.id}")
        return nuevo_usuario

    def obtener_usuario(self, usuario_id: str) -> Optional[Usuario]:
        """
        Busca un usuario por su ID completo.

        Args:
            usuario_id (str): El ID exacto del usuario a buscar.

        Retorna:
            El objeto Usuario si se encuentra, de lo contrario None.
        """
        for usuario in self.usuarios:
            if usuario.id == usuario_id:
                return usuario
        return None

    def modificar_usuario(self, usuario_id: str) -> bool:
        """
        Permite al usuario cambiar el nombre de un usuario existente.

        Args:
            usuario_id (str): El ID del usuario a modificar.

        Returns:
            True si se modificó, False si no se encontró.
        """
        usuario = self.obtener_usuario(usuario_id)
        if not usuario:
            print("Error: No se encontró un usuario con ese ID.")
            return False

        print(f"Modificando usuario: '{usuario.nombre}'")
        nuevo_nombre = input(f"Nuevo nombre (deja en blanco para mantener '{usuario.nombre}'): ").strip()
        if nuevo_nombre:
            usuario.nombre = nuevo_nombre
            print(f"Nombre del usuario actualizado a '{usuario.nombre}'.")
        else:
            print("No se realizaron cambios.")
        return True

    # --- Métodos de Préstamos y Multas ---

    def actualizar_multa(self, usuario: Usuario) -> None:
        """
        Calcula y actualiza la multa de un usuario basándose en sus préstamos.

        Usa pendulum para comparar la fecha actual con la fecha de devolución
        de cada libro prestado.

        Args:
            usuario (Usuario): El objeto usuario cuya multa se va a calcular.
        """
        multa_total = 0.0
        # pm.now() obtiene la fecha y hora actual en una zona horaria específica.
        ahora = pm.now("America/Mexico_City")

        for libro_prestado in usuario.libros:
            # pm.parse() convierte la fecha en formato string (ISO 8601) a un objeto pendulum.
            fecha_devolucion = pm.parse(libro_prestado.fecha_devolucion)
            if ahora > fecha_devolucion:
                # La diferencia entre dos objetos pendulum da un objeto Period.
                # .in_days() extrae la diferencia total en días.
                dias_retraso = (ahora - fecha_devolucion).in_days()
                multa_total += dias_retraso * MULTA_POR_DIA

        usuario.multa_pendiente = multa_total

    def actualizar_todas_las_multas(self) -> None:
        """
        Ejecuta actualizar_multa para cada usuario en la biblioteca.
        Útil para asegurar que todos los datos estén al día antes de guardarlos.
        """
        if not self.usuarios:
            print("No hay usuarios registrados para actualizar.")
            return

        print("Actualizando multas para todos los usuarios...")
        for usuario in self.usuarios:
            self.actualizar_multa(usuario)
        print("¡Multas actualizadas!")

    def prestar_libro(self, usuario_id: str, libro_id: str) -> bool:
        """
        Gestiona el proceso completo de prestar un libro a un usuario.

        Realiza varias validaciones antes de confirmar el préstamo:
        1. Verifica que tanto el usuario como el libro existan.
        2. Actualiza y comprueba si el usuario tiene multas pendientes.
        3. Comprueba si el usuario ha alcanzado el límite de libros.
        4. Verifica que el libro esté disponible.

        Retorna:
            True si el préstamo fue exitoso, False en caso contrario.
        """
        usuario = self.obtener_usuario(usuario_id)
        libro_catalogo = self.obtener_libro(libro_id)

        if not usuario or not libro_catalogo:
            print("Error: ID de usuario o libro no encontrado.")
            return False

        # Es crucial actualizar la multa justo antes de intentar un préstamo.
        self.actualizar_multa(usuario)
        if usuario.multa_pendiente > 0:
            print(f"Error: El usuario tiene una multa de ${usuario.multa_pendiente:.2f} y no puede solicitar préstamos.")
            return False

        if len(usuario.libros) >= LIMITE_LIBROS:
            print(f"Error: El usuario ya ha alcanzado el límite de {LIMITE_LIBROS} libros prestados.")
            return False

        if not libro_catalogo.disponible or libro_catalogo.cantidad <= 0:
            print(f"Error: El libro '{libro_catalogo.nombre}' no está disponible.")
            return False

        # Actualiza el catálogo
        libro_catalogo.cantidad -= 1
        libro_catalogo.disponible = libro_catalogo.cantidad > 0

        # Crea el registro del préstamo usando pendulum
        fecha_prestamo = pm.now("America/Mexico_City")
        fecha_devolucion = fecha_prestamo.add(days=DIAS_PRESTAMO)

        """
        rea una instancia de Prestamo.
        libro_catalogo.model_dump() desempaqueta el diccionario del libro
        (id, nombre, etc.) y lo usa como argumentos para crear el objeto Prestamo.
        """
        prestamo = Prestamo(
            **libro_catalogo.model_dump(),
            fecha=fecha_prestamo.to_iso8601_string(), # Convierte a string estándar
            fecha_devolucion=fecha_devolucion.to_iso8601_string(),
        )

        # Añade el préstamo a la lista del usuario.
        usuario.libros.append(prestamo)
        print(f"Préstamo exitoso: '{libro_catalogo.nombre}' a '{usuario.nombre}'.")
        print(f"Fecha de devolución: {fecha_devolucion.format('DD-MM-YYYY')}.")
        return True

    def devolver_libro(self, usuario_id: str, libro_prestado_id: str) -> bool:
        """
        Registra la devolución de un libro.

        Retorna:
            True si la devolución fue exitosa, False en caso contrario.
        """
        usuario = self.obtener_usuario(usuario_id)
        if not usuario:
            print("Error: ID de usuario no encontrado.")
            return False

        # Busca el libro en la lista de préstamos del usuario.
        libro_a_devolver = None
        for libro in usuario.libros:
            if libro.id == libro_prestado_id:
                libro_a_devolver = libro
                break # Sale del bucle una vez que lo encuentra.

        if not libro_a_devolver:
            print("Error: El usuario no tiene prestado un libro con ese ID.")
            return False

        # Proceso de devolución
        usuario.libros.remove(libro_a_devolver)
        libro_catalogo = self.obtener_libro(libro_a_devolver.id)
        if libro_catalogo:
            libro_catalogo.cantidad += 1
            libro_catalogo.disponible = True
        else:
            """
            Este else maneja un caso extremo: si el libro fue eliminado
            del catálogo mientras estaba prestado. Al devolverlo, se
            re-agrega al catálogo.
            """
            self.libros.append(
                Libro(
                    id=libro_a_devolver.id,
                    nombre=libro_a_devolver.nombre,
                    cantidad=1,
                    disponible=True,
                )
            )

        print(f"Devolución exitosa: '{libro_a_devolver.nombre}' por '{usuario.nombre}'.")
        # Después de devolver, se actualiza la multa por si había retrasos.
        self.actualizar_multa(usuario)
        if usuario.multa_pendiente > 0:
            print(f"El usuario ahora tiene una multa pendiente de ${usuario.multa_pendiente:.2f}.")
        return True

    def pagar_multa(self, usuario_id: str) -> bool:
        """
        Pone a cero la multa pendiente de un usuario.

        Retorna:
            True si se procesó el pago, False si no se encontró al usuario.
        """
        usuario = self.obtener_usuario(usuario_id)
        if not usuario:
            print("Error: ID de usuario no encontrado.")
            return False

        self.actualizar_multa(usuario) # Asegura que el monto sea el actual.
        if usuario.multa_pendiente > 0:
            print(f"Se ha pagado la multa de ${usuario.multa_pendiente:.2f} para el usuario '{usuario.nombre}'.")
            usuario.multa_pendiente = 0.0
        else:
            print("El usuario no tiene multas pendientes.")
        return True


# --- Interfaz de Usuario por Consola (Menú) ---
"""
Estas funciones no forman parte de la clase Biblioteca, son "helpers"
para la interfaz de usuario. El guion bajo _ al inicio sugiere que
son funciones "privadas" o de uso interno para este módulo.
"""

def _buscar_por_prefijo_id(lista_items: List[Any], prefijo: str) -> Optional[str]:
    """
    Función de ayuda para buscar un item por los primeros caracteres de su ID.

    Esto mejora la experiencia de usuario al no requerir que se escriba el
    largo ID completo.

    Args:
        lista_items (List[Any]): Lista de objetos (libros o usuarios).
        prefijo (str): Los primeros caracteres del ID a buscar.

    Returns:
        - El ID completo si solo hay una coincidencia.
        - El ID completo si hay varias coincidencias y el usuario elige una.
        - None si no hay coincidencias o el usuario no selecciona una válida.
    """
    # List comprehension para filtrar la lista y encontrar todas las coincidencias.
    coincidencias = [item for item in lista_items if item.id.startswith(prefijo)]

    if not coincidencias:
        print("No se encontró ningún item con ese prefijo de ID.")
        return None

    if len(coincidencias) == 1:
        # Si solo hay uno, es el que buscamos.
        return coincidencias[0].id

    # Si hay múltiples, se le pide al usuario que desambigüe.
    print("Múltiples coincidencias encontradas. Por favor, especifica el ID completo:")
    for item in coincidencias:
        print(f"- ID: {item.id} | Nombre: {item.nombre}")
    id_completo = input("Introduce el ID completo de la lista: ").strip()

    # Verifica que el ID introducido sea uno de los de la lista de coincidencias.
    for item in coincidencias:
        if item.id == id_completo:
            return id_completo

    print("El ID introducido no es válido.")
    return None


def _seleccionar_item(biblioteca: Biblioteca, tipo_item: str) -> Optional[str]:
    """
    Función genérica para mostrar una lista (de libros o usuarios) y
    pedir al usuario que seleccione uno usando su ID o un prefijo.

    Args:
        biblioteca (Biblioteca): La instancia de la biblioteca.
        tipo_item (str): 'libro' o 'usuario'.

    Returns:
        El ID completo del item seleccionado o None.
    """
    if tipo_item == "libro":
        items = biblioteca.libros
        biblioteca.mostrar_catalogo()
    else:  # 'usuario'
        items = biblioteca.usuarios
        biblioteca.mostrar_usuarios()
    
    # Si la lista está vacía, no hay nada que seleccionar.
    if not items:
        return None

    id_prefijo = input("Introduce el ID completo o los primeros caracteres: ").strip()

    if not id_prefijo:
        return None

    return _buscar_por_prefijo_id(items, id_prefijo)


def main():
    """
    Función principal que ejecuta el bucle del menú de la aplicación.
    """
    biblioteca = Biblioteca() # Crea la instancia principal.

    while True:
        # Imprime el menú de opciones en cada iteración.
        print("\n" + "=" * 25)
        print("     MENÚ PRINCIPAL     ")
        print("=" * 25)
        print("--- GESTIÓN DE LIBROS ---")
        print("1. Ver catálogo de libros")
        print("2. Agregar libro al catálogo")
        print("3. Modificar libro")
        print("4. Eliminar libro del catálogo")
        print("\n--- GESTIÓN DE USUARIOS ---")
        print("5. Ver lista de usuarios")
        print("6. Crear nuevo usuario")
        print("7. Modificar usuario")
        print("\n--- OPERACIONES ---")
        print("8. Prestar libro")
        print("9. Devolver libro")
        print("10. Ver préstamos de un usuario")
        print("11. Pagar multa de un usuario")
        print("12. Actualizar multas y guardar")
        print("\n13. Salir")

        opcion = input("\nElige una opción: ").strip()

        # Cada if/elif corresponde a una opción del menú y llama al método apropiado de la clase Biblioteca.

        if opcion == "1":
            biblioteca.mostrar_catalogo()

        elif opcion == "2":
            nombre = input("Nombre del nuevo libro: ").strip()
            if not nombre:
                print("El nombre no puede estar vacío.")
                continue # Vuelve al inicio del bucle while.
            try:
                cantidad = int(input("Cantidad de copias: ").strip())
                if cantidad > 0:
                    biblioteca.agregar_libro(nombre, cantidad)
                else:
                    print("La cantidad debe ser un número positivo.")
            except ValueError:
                print("Error: La cantidad debe ser un número entero.")

        elif opcion == "3":
            print("Selecciona el libro a modificar:")
            id_libro = _seleccionar_item(biblioteca, "libro")
            if id_libro:
                biblioteca.modificar_libro(id_libro)

        elif opcion == "4":
            print("Selecciona el libro a eliminar:")
            id_libro = _seleccionar_item(biblioteca, "libro")
            if id_libro:
                # Pide confirmación antes de una acción destructiva.
                if input(f"¿Seguro que deseas eliminarlo? (s/n): ").lower() == "s":
                    biblioteca.eliminar_libro(id_libro)

        elif opcion == "5":
            biblioteca.mostrar_usuarios()

        elif opcion == "6":
            nombre = input("Nombre del nuevo usuario: ").strip()
            if nombre:
                biblioteca.crear_usuario(nombre)
            else:
                print("El nombre no puede estar vacío.")

        elif opcion == "7":
            print("Selecciona el usuario a modificar:")
            id_usuario = _seleccionar_item(biblioteca, "usuario")
            if id_usuario:
                biblioteca.modificar_usuario(id_usuario)

        elif opcion == "8":
            print("Selecciona el usuario que solicita el préstamo:")
            id_usuario = _seleccionar_item(biblioteca, "usuario")
            if not id_usuario:
                continue
            print("\nSelecciona el libro a prestar:")
            id_libro = _seleccionar_item(biblioteca, "libro")
            if id_libro:
                biblioteca.prestar_libro(id_usuario, id_libro)

        elif opcion == "9":
            print("Selecciona el usuario que devolverá el libro:")
            id_usuario = _seleccionar_item(biblioteca, "usuario")
            if not id_usuario:
                continue
            
            # Obtiene el objeto usuario para verificar si tiene libros prestados.
            if usuario := biblioteca.obtener_usuario(id_usuario):
                if not usuario.libros:
                    print("Este usuario no tiene libros para devolver.")
                    continue

                print("\n--- Libros prestados al usuario ---")
                for libro in usuario.libros:
                    print(f"- ID: {libro.id} | Nombre: {libro.nombre}")

                id_libro_dev = input("Introduce el ID del libro a devolver: ").strip()
                if id_libro_dev:
                    biblioteca.devolver_libro(id_usuario, id_libro_dev)

        elif opcion == "10":
            print("Selecciona el usuario para ver sus préstamos:")
            id_usuario = _seleccionar_item(biblioteca, "usuario")
            if id_usuario:
                if usuario := biblioteca.obtener_usuario(id_usuario):
                    biblioteca.actualizar_multa(usuario) # Siempre mostrar datos actualizados.
                    print(f"\n--- Resumen de {usuario.nombre} ---")
                    print(f"Multa Pendiente: ${usuario.multa_pendiente:.2f}")
                    print("Libros en préstamo:")
                    if not usuario.libros:
                        print("  (Ninguno)")
                    else:
                        for libro in usuario.libros:
                            fecha_dev_obj = pm.parse(libro.fecha_devolucion)
                            print(
                                f"  - {libro.nombre} (Devolver antes del: {fecha_dev_obj.format('DD-MM-YYYY')})"
                            )
                    print("-" * 20)

        elif opcion == "11":
            print("Selecciona el usuario que va a pagar su multa:")
            id_usuario = _seleccionar_item(biblioteca, "usuario")
            if id_usuario:
                biblioteca.pagar_multa(id_usuario)

        elif opcion == "12":
            # Opción manual para forzar la actualización y guardado.
            biblioteca.actualizar_todas_las_multas()
            biblioteca.guardar_datos()
            print("Datos guardados en el archivo.")

        elif opcion == "13":
            print("Guardando datos y saliendo del sistema...")
            biblioteca.guardar_datos() # Asegura que todo se guarde antes de salir.
            break # Rompe el bucle while True y termina el programa.

        else:
            print("Opción inválida. Por favor, elige un número del menú.")

        # Guardado automático después de cada operación que modifica el estado.
        if opcion in ["2", "3", "4", "6", "7", "8", "9", "11"]:
            biblioteca.guardar_datos()


"""
# Este es un estándar en Python. El código dentro de este if solo se
# ejecutará cuando el script es corrido directamente (y no cuando es importado
# por otro script). Es el punto de entrada de la aplicación.
"""
if __name__ == "__main__":
    main()
