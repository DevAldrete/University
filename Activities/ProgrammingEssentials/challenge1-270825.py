# Programacion, Ingles, Algebra
maria = [67, 100, 89]
juan = [68, 73, 71]
jesus = [80, 84, 87]
cristina = [92, 100, 78]

calificaciones = [maria, juan, jesus, cristina]
alumnos = ["Maria", "Juan", "Jesus", "Cristina"]

print("     Programacion - Algebra - Ingles")
for calificacion, alumno in zip(calificaciones, alumnos):
    print("----------------------------")
    print(f"{alumno}", end=" ")
    for num in calificacion:
        print(f"{num}", end=" - ")
    print()
