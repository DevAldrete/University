
Inicio
	Cargar datos desde biblioteca.json
	Mientras True:
		Mostrar menú:
			1. Ver libros disponibles
			2. Agregar libro
			3. Modificar libro
			4. Eliminar libro
			5. Prestar libro
			6. Devolver libro
			7. Visualizar préstamos y multas
			8. Pagar multa
			9. Administrar préstamos manual
			10. Salir
		Leer opción del usuario
		Segun opción hacer
			Caso 1: llamar mostrar_libros(biblioteca)
			Caso 2: llamar agregar_libro(biblioteca)
			Caso 3: llamar modificar_libro(biblioteca)
			Caso 4: llamar eliminar_libro(biblioteca)
			Caso 5: llamar prestar_libro(biblioteca)
			Caso 6: llamar devolver_libro(biblioteca)
			Caso 7: llamar visualizar_prestamos(biblioteca)
			Caso 8: llamar pagar_multa(biblioteca)
			Caso 9: llamar administrar_prestamos_manual(biblioteca)
			Caso 10: guardar_datos(biblioteca) y salir
			De otro modo: mostrar "Opción inválida"
	Fin Mientras
Fin
