from sqlalchemy import (
    create_engine,
    Table,
    Column,
    Integer,
    String,
    MetaData,
    select,
    insert,
    update,
    delete,
)
from sqlalchemy.engine import Connection

# --- 1. CONFIGURACIÓN DE LA CONEXIÓN ---
# Reemplaza con tus propios datos obtenidos de la consola de AWS RDS
DB_USER = "postgres"
DB_PASSWORD = "postgresdb"
DB_HOST = ""
DB_PORT = ""
DB_NAME = "testdb"

DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


# --- FUNCIÓN AUXILIAR PARA MOSTRAR EL ESTADO DE LA TABLA ---
def print_table_state(conn: Connection, table: Table, title: str):
    """Ejecuta un SELECT * y muestra los resultados de forma ordenada."""
    print(f"\n--- {title} ---")
    select_stmt = select(table)
    result = conn.execute(select_stmt)
    rows = result.fetchall()

    if not rows:
        print("La tabla 'users' está vacía.")
    else:
        print(f"{'ID':<5}{'Nombre':<20}{'Email':<30}")
        print("-" * 55)
        for row in rows:
            print(f"{row.id:<5}{row.name:<20}{row.email:<30}")
    print("-" * 55)


# --- 2. LÓGICA PRINCIPAL ---
try:
    engine = create_engine(
        DATABASE_URL, echo=False
    )  # echo=False para un output más limpio
    with engine.connect() as connection:
        print("¡Conexión a la base de datos RDS PostgreSQL exitosa! 🎉")

        # --- 3. CREAR UNA TABLA (Operación DDL) ---
        metadata = MetaData()
        users_table = Table(
            "users",
            metadata,
            Column("id", Integer, primary_key=True),
            Column("name", String(50)),
            Column("email", String(50)),
        )
        metadata.create_all(engine)
        print("\nTabla 'users' creada o ya existente.")

        # Opcional: Limpiar la tabla para empezar de cero en cada ejecución
        # connection.execute(users_table.delete())
        # connection.commit()

        # Mostrar estado inicial (debería estar vacía)
        print_table_state(connection, users_table, "ESTADO INICIAL DE LA TABLA")

        # --- 4. OPERACIONES CRUD ---

        # CREATE (Crear) - Insertar 4 nuevos usuarios
        print("\n>>> INICIANDO OPERACIÓN: CREATE <<<")
        users_to_add = [
            {"name": "Ana", "email": "ana@example.com"},
            {"name": "Carlos", "email": "carlos@example.com"},
            {"name": "Elena", "email": "elena@example.com"},
            {"name": "Luis", "email": "luis@example.com"},
        ]
        connection.execute(insert(users_table), users_to_add)
        connection.commit()
        print("Se han insertado 4 nuevos usuarios.")
        print_table_state(
            connection, users_table, "ESTADO DE LA TABLA DESPUÉS DE CREATE"
        )

        # READ (Leer) - La función auxiliar ya hace esto
        print("\n>>> INICIANDO OPERACIÓN: READ <<<")
        print("La operación de lectura simplemente muestra el estado actual.")
        print_table_state(connection, users_table, "ESTADO ACTUAL (LECTURA)")

        # UPDATE (Actualizar) - Actualizar el email de Ana
        print("\n>>> INICIANDO OPERACIÓN: UPDATE <<<")
        print_table_state(connection, users_table, "ESTADO DE LA TABLA ANTES DE UPDATE")
        update_stmt = (
            update(users_table)
            .where(users_table.c.name == "Ana")
            .values(email="ana.actualizada@example.com")
        )
        connection.execute(update_stmt)
        connection.commit()
        print("Se ha actualizado el email de 'Ana'.")
        print_table_state(
            connection, users_table, "ESTADO DE LA TABLA DESPUÉS DE UPDATE"
        )

        # DELETE (Borrar) - Borrar a Carlos
        print("\n>>> INICIANDO OPERACIÓN: DELETE <<<")
        print_table_state(connection, users_table, "ESTADO DE LA TABLA ANTES DE DELETE")
        delete_stmt = delete(users_table).where(users_table.c.name == "Carlos")
        connection.execute(delete_stmt)
        connection.commit()
        print("Se ha eliminado a 'Carlos'.")
        print_table_state(connection, users_table, "ESTADO FINAL DE LA TABLA")

except Exception as e:
    print(f"Error al conectar o ejecutar operaciones en la base de datos: {e}")
