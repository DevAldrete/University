"""
Sistema de gestión de préstamos de libros en una biblioteca.

Este script implementa una solución completa para la administración de una
biblioteca, permitiendo gestionar un catálogo de libros y el préstamo de
estos a usuarios.

Caracteristicas
- Búsqueda por prefijo de ID para libros y usuarios.
- Modificación de datos de libros y usuarios.
- Visualización de préstamos con cálculo de multas ($15/día después de 7 días).
- Límite de 3 libros por usuario.
- Bloqueo de nuevos préstamos si el usuario tiene multa pendiente.
- Opción para pagar multas y actualizar datos manualmente.
- Persistencia de datos en un único archivo JSON.
"""

import json  # Modulo json importado con el fin de manejar archivos json
from typing import (
    Dict,
    List,
    Any,
    Optional,
)  # Tipado para variables, parametros, y mas, con el fin de recibir ayuda del IDE y validacion
import uuid  # UUID para generar IDs unicos
import pendulum as pm  # Pendulum es un modulo que permite manejar objetos datatime de manera inteligente y eficiente: https://pendulum.eustace.io/
from pydantic import (
    BaseModel,  # Crear clases que hereden de BaseModel con el fin de completar la validacion de pydantic
    Field,
)  # Pydantic es utilizado para validacion de datos de manera estricta

"""
Field utilizado dentro de BaseModel para indicar distintas caracteristicas de un campo o propiedad de la clase y validacion de la propiedad
"""

# --- Constantes de configuración ---
RUTA_JSON = "biblioteca.json"  # Archivo JSON de almacenamiento
DIAS_PRESTAMO = 7  # Días sin multa
MULTA_POR_DIA = 15.0  # Multa en pesos mexicanos por día de retraso
LIMITE_LIBROS = 3  # Máximo de libros por usuario


# --- Modelos de Datos (usando Pydantic) ---


class Libro(BaseModel):
    """
    Representa un libro en el catálogo de la biblioteca.

    Atributos:
        id (str): Identificador único del libro.
        nombre (str): Título del libro.
        disponible (bool): True si hay al menos una copia disponible.
        cantidad (int): Número de copias existentes de este libro.
    """

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4())
    )  # De manera automatica podemos crear IDs unicos utilizando default_factory
    nombre: str
    disponible: bool
    cantidad: int


class Prestamo(Libro):
    """
    Representa un libro que ha sido prestado a un usuario.
    Hereda de Libro y añade las fechas de préstamo y devolución.

    Atributos:
        fecha (str): Fecha y hora del préstamo en formato ISO 8601.
        fecha_devolucion (str): Fecha y hora límite para la devolución.
    """

    fecha: str
    fecha_devolucion: str


class Usuario(BaseModel):
    """
    Representa a un usuario de la biblioteca.

    Atributos:
        id (str): Identificador único del usuario.
        nombre (str): Nombre del usuario.
        libros (List[Prestamo]): Lista de libros que el usuario tiene en préstamo.
        multa_pendiente (float): Monto total de la multa acumulada.
    """

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    nombre: str
    libros: List[Prestamo] = []
    multa_pendiente: float = 0.0


# --- Lógica de la Biblioteca ---


class Biblioteca:
    """
    Clase principal que gestiona todas las operaciones de la biblioteca,
    incluyendo el catálogo de libros y los préstamos a usuarios.
    """

    def __init__(self) -> None:
        """
        Inicializa la biblioteca, cargando los datos desde el archivo JSON
        si existe.
        """
        self.libros: List[Libro] = []
        self.usuarios: List[Usuario] = []
        if datos := self.cargar_datos():
            self.libros = [
                Libro.model_validate(libro) for libro in datos.get("libros", [])
            ]
            self.usuarios = [
                Usuario.model_validate(usuario) for usuario in datos.get("usuarios", [])
            ]
        else:
            print(
                "No se encontró un archivo de datos, se iniciará una biblioteca nueva."
            )

    def cargar_datos(self) -> Optional[Dict[str, Any]]:
        """
        Carga los datos de la biblioteca desde un archivo JSON.

        Retorna:
            Un diccionario con los datos si el archivo existe y es válido,
            o None si ocurre un error.
        """
        try:
            with open(RUTA_JSON, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return None
        except json.JSONDecodeError:
            print("Error: El archivo JSON está corrupto o mal formateado.")
            return None

    def guardar_datos(self) -> None:
        """
        Guarda el estado actual de la biblioteca (libros y usuarios)
        en el archivo JSON.
        """
        try:
            with open(RUTA_JSON, "w", encoding="utf-8") as f:
                datos = {
                    "libros": [libro.model_dump() for libro in self.libros],
                    "usuarios": [usuario.model_dump() for usuario in self.usuarios],
                }
                json.dump(datos, f, indent=4, ensure_ascii=False)
        except IOError as e:
            print(f"Error al intentar guardar los datos en el archivo: {e}")

    # --- Métodos de Gestión de Libros ---
    def mostrar_catalogo(self) -> None:
        items = self.libros
        print("\n--- Catálogo de Libros ---")
        if not items:
            print("No hay libros en el catálogo.")
            return None
        for item in items:
            estado = "Disponible" if item.disponible else "Agotado"
            print(
                f"- ID: {item.id} | Nombre: {item.nombre} | Cantidad: {item.cantidad} ({estado})"
            )

    def agregar_libro(self, nombre: str, cantidad: int) -> None:
        """
        Agrega un nuevo libro al catálogo o incrementa la cantidad si ya existe.

        Args:
            nombre (str): El nombre del libro a agregar.
            cantidad (int): El número de copias a agregar.
        """
        for libro in self.libros:
            if libro.nombre.lower() == nombre.lower():
                libro.cantidad += cantidad
                libro.disponible = libro.cantidad > 0
                print(
                    f"Se agregaron {cantidad} copias de '{nombre}'. Cantidad total: {libro.cantidad}."
                )
                return

        nuevo_libro = Libro(nombre=nombre, cantidad=cantidad, disponible=cantidad > 0)
        self.libros.append(nuevo_libro)
        print(f"Libro '{nombre}' agregado al catálogo con {cantidad} copias.")

    def obtener_libro(self, libro_id: str) -> Optional[Libro]:
        """
        Busca un libro en el catálogo por su ID.

        Args:
            libro_id (str): El ID del libro a buscar.

        Retorna:
            El objeto Libro si se encuentra, de lo contrario None.
        """
        for libro in self.libros:
            if libro.id == libro_id:
                return libro
        return None

    def modificar_libro(self, libro_id: str) -> bool:
        """
        Modifica la información de un libro existente en el catálogo.

        Args:
            libro_id (str): El ID del libro a modificar.

        Returns:
            True si el libro se modificó con éxito, False en caso contrario.
        """
        libro = self.obtener_libro(libro_id)
        if not libro:
            print("Error: No se encontró un libro con ese ID.")
            return False

        print(
            f"Modificando libro: '{libro.nombre}' (Cantidad actual: {libro.cantidad})"
        )

        nuevo_nombre = input(
            f"Nuevo nombre (deja en blanco para mantener '{libro.nombre}'): "
        ).strip()
        if nuevo_nombre:
            libro.nombre = nuevo_nombre
            print(f"Nombre del libro actualizado a '{libro.nombre}'.")

        try:
            nueva_cantidad_str = input(
                f"Nueva cantidad (deja en blanco para mantener {libro.cantidad}): "
            ).strip()
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
        items = self.usuarios
        print("\n--- Lista de Usuarios ---")
        if not items:
            print("No hay usuarios registrados.")
            return None
        for item in items:
            print(f"- ID: {item.id} | Nombre: {item.nombre}")

    def crear_usuario(self, nombre: str) -> Usuario:
        """
        Crea un nuevo usuario y lo añade a la lista de usuarios.

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
        Busca un usuario por su ID.

        Args:
            usuario_id (str): El ID del usuario a buscar.

        Retorna:
            El objeto Usuario si se encuentra, de lo contrario None.
        """
        for usuario in self.usuarios:
            if usuario.id == usuario_id:
                return usuario
        return None

    def modificar_usuario(self, usuario_id: str) -> bool:
        """
        Modifica el nombre de un usuario existente.

        Args:
            usuario_id (str): El ID del usuario a modificar.

        Returns:
            True si el usuario se modificó con éxito, False en caso contrario.
        """
        usuario = self.obtener_usuario(usuario_id)
        if not usuario:
            print("Error: No se encontró un usuario con ese ID.")
            return False

        print(f"Modificando usuario: '{usuario.nombre}'")
        nuevo_nombre = input(
            f"Nuevo nombre (deja en blanco para mantener '{usuario.nombre}'): "
        ).strip()
        if nuevo_nombre:
            usuario.nombre = nuevo_nombre
            print(f"Nombre del usuario actualizado a '{usuario.nombre}'.")
        else:
            print("No se realizaron cambios.")
        return True

    # --- Métodos de Préstamos y Multas ---
    def actualizar_multa(self, usuario: Usuario) -> None:
        """
        Calcula y actualiza la multa pendiente de un usuario basándose
        en la fecha actual.

        Args:
            usuario (Usuario): El usuario cuya multa se va a calcular.
        """
        multa_total = 0.0
        ahora = pm.now("America/Mexico_City")

        for libro_prestado in usuario.libros:
            fecha_devolucion = pm.parse(libro_prestado.fecha_devolucion)
            if ahora > fecha_devolucion:
                dias_retraso = (ahora - fecha_devolucion).in_days()
                multa_total += dias_retraso * MULTA_POR_DIA

        usuario.multa_pendiente = multa_total

    def actualizar_todas_las_multas(self):
        """
        Recalcula las multas para todos los usuarios de la biblioteca.
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
        Realiza el préstamo de un libro a un usuario.

        Args:
            usuario_id (str): El ID del usuario que solicita el préstamo.
            libro_id (str): El ID del libro a prestar.

        Retorna:
            True si el préstamo fue exitoso, de lo contrario False.
        """
        usuario = self.obtener_usuario(usuario_id)
        libro_catalogo = self.obtener_libro(libro_id)

        if not usuario or not libro_catalogo:
            print("Error: ID de usuario o libro no encontrado.")
            return False

        self.actualizar_multa(usuario)
        if usuario.multa_pendiente > 0:
            print(
                f"Error: El usuario tiene una multa de ${usuario.multa_pendiente:.2f} y no puede solicitar préstamos."
            )
            return False

        if len(usuario.libros) >= LIMITE_LIBROS:
            print(
                f"Error: El usuario ya ha alcanzado el límite de {LIMITE_LIBROS} libros prestados."
            )
            return False

        if not libro_catalogo.disponible or libro_catalogo.cantidad <= 0:
            print(f"Error: El libro '{libro_catalogo.nombre}' no está disponible.")
            return False

        libro_catalogo.cantidad -= 1
        libro_catalogo.disponible = libro_catalogo.cantidad > 0

        fecha_prestamo = pm.now("America/Mexico_City")
        fecha_devolucion = fecha_prestamo.add(days=DIAS_PRESTAMO)

        prestamo = Prestamo(
            **libro_catalogo.model_dump(),
            fecha=fecha_prestamo.to_iso8601_string(),
            fecha_devolucion=fecha_devolucion.to_iso8601_string(),
        )

        usuario.libros.append(prestamo)
        print(f"Préstamo exitoso: '{libro_catalogo.nombre}' a '{usuario.nombre}'.")
        print(f"Fecha de devolución: {fecha_devolucion.format('DD-MM-YYYY')}.")
        return True

    def devolver_libro(self, usuario_id: str, libro_prestado_id: str) -> bool:
        """
        Registra la devolución de un libro por parte de un usuario.

        Args:
            usuario_id (str): El ID del usuario que devuelve el libro.
            libro_prestado_id (str): El ID del libro que está siendo devuelto.

        Retorna:
            True si la devolución fue exitosa, de lo contrario False.
        """
        usuario = self.obtener_usuario(usuario_id)
        if not usuario:
            print("Error: ID de usuario no encontrado.")
            return False

        libro_a_devolver = None
        for libro in usuario.libros:
            if libro.id == libro_prestado_id:
                libro_a_devolver = libro

        if not libro_a_devolver:
            print("Error: El usuario no tiene prestado un libro con ese ID.")
            return False

        usuario.libros.remove(libro_a_devolver)
        libro_catalogo = self.obtener_libro(libro_a_devolver.id)
        if libro_catalogo:
            libro_catalogo.cantidad += 1
            libro_catalogo.disponible = True
        else:
            self.libros.append(
                Libro(
                    id=libro_a_devolver.id,
                    nombre=libro_a_devolver.nombre,
                    cantidad=1,
                    disponible=True,
                )
            )

        print(
            f"Devolución exitosa: '{libro_a_devolver.nombre}' por '{usuario.nombre}'."
        )
        self.actualizar_multa(usuario)
        if usuario.multa_pendiente > 0:
            print(
                f"El usuario ahora tiene una multa pendiente de ${usuario.multa_pendiente:.2f}."
            )
        return True

    def pagar_multa(self, usuario_id: str) -> bool:
        """
        Registra el pago de la multa de un usuario.

        Args:
            usuario_id (str): El ID del usuario que paga la multa.

        Retorna:
            True si el pago se registró, False si el usuario no se encontró.
        """
        usuario = self.obtener_usuario(usuario_id)
        if not usuario:
            print("Error: ID de usuario no encontrado.")
            return False

        self.actualizar_multa(usuario)
        if usuario.multa_pendiente > 0:
            print(
                f"Se ha pagado la multa de ${usuario.multa_pendiente:.2f} para el usuario '{usuario.nombre}'."
            )
            usuario.multa_pendiente = 0.0
        else:
            print("El usuario no tiene multas pendientes.")
        return True


# --- Interfaz de Usuario por Consola (Menú) ---


def _buscar_por_prefijo_id(lista_items: List[Any], prefijo: str) -> Optional[str]:
    """
    Busca un item (libro o usuario) por el prefijo de su ID.

    Args:
        lista_items (List[Any]): La lista de objetos (libros o usuarios) donde buscar.
        prefijo (str): Los primeros caracteres del ID.

    Returns:
        El ID completo si se encuentra una única coincidencia.
        None si no hay coincidencias o hay múltiples y el usuario no elige una.
    """
    coincidencias = [item for item in lista_items if item.id.startswith(prefijo)]

    if not coincidencias:
        print("No se encontró ningún item con ese prefijo de ID.")
        return None

    if len(coincidencias) == 1:
        return coincidencias[0].id

    print("Múltiples coincidencias encontradas. Por favor, especifica el ID completo:")
    for item in coincidencias:
        print(f"- ID: {item.id} | Nombre: {item.nombre}")
    id_completo = input("Introduce el ID completo de la lista: ").strip()

    # Verificamos que el ID completo esté en las coincidencias
    for item in coincidencias:
        if item.id == id_completo:
            return id_completo

    print("El ID introducido no es válido.")
    return None


def _seleccionar_item(biblioteca: Biblioteca, tipo_item: str) -> Optional[str]:
    """
    Función de ayuda genérica para mostrar y seleccionar un libro o usuario.

    Args:
        biblioteca (Biblioteca): La instancia de la biblioteca.
        tipo_item (str): 'libro' o 'usuario'.

    Returns:
        El ID del item seleccionado o None.
    """
    if tipo_item == "libro":
        items = biblioteca.libros
        biblioteca.mostrar_catalogo()
    else:  # usuario
        items = biblioteca.usuarios
        print("\n--- Lista de Usuarios ---")
        if not items:
            print("No hay usuarios registrados.")
            return None
        for item in items:
            print(f"- ID: {item.id} | Nombre: {item.nombre}")

    id_prefijo = input("Introduce el ID completo o los primeros caracteres: ").strip()

    if not id_prefijo:
        return None

    return _buscar_por_prefijo_id(items, id_prefijo)


def main():
    """
    Bucle principal de interacción por consola.
    Todas las operaciones persisten los cambios inmediatamente en el archivo JSON.
    """
    biblioteca = Biblioteca()

    while True:
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

        if opcion == "1":
            biblioteca.mostrar_catalogo()

        elif opcion == "2":
            nombre = input("Nombre del nuevo libro: ").strip()
            if not nombre:
                print("El nombre no puede estar vacío.")
                continue
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
                if input(f"¿Seguro (s/n)?: ").lower() == "s":
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

            else:
                print("Usuario no encontrado.")

        elif opcion == "10":
            print("Selecciona el usuario para ver sus préstamos:")
            id_usuario = _seleccionar_item(biblioteca, "usuario")
            if id_usuario:
                if usuario := biblioteca.obtener_usuario(id_usuario):
                    biblioteca.actualizar_multa(usuario)
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
                else:
                    print("Usuario no encontrado.")

        elif opcion == "11":
            print("Selecciona el usuario que va a pagar su multa:")
            id_usuario = _seleccionar_item(biblioteca, "usuario")
            if id_usuario:
                biblioteca.pagar_multa(id_usuario)

        elif opcion == "12":
            biblioteca.actualizar_todas_las_multas()
            biblioteca.guardar_datos()
            print("Datos guardados en el archivo.")

        elif opcion == "13":
            print("Guardando datos y saliendo del sistema...")
            biblioteca.guardar_datos()
            break

        else:
            print("Opción inválida.")

        # Guardar después de cada operación que modifica datos
        if opcion in ["2", "3", "4", "6", "7", "8", "9", "11"]:
            biblioteca.guardar_datos()


if __name__ == "__main__":
    main()
