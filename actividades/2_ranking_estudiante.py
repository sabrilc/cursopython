estudiantes =[
    ("Ana",95),
    ("Luis",80),
    ("Maria",100),
    ("Pedro",70)
]

#funcion para ordenar estudiantes por puntuación
def ordenar_estudiantes(estudiantes):
    return list(sorted(estudiantes, key=lambda x: x[1]))

#funcion para filtrar estudiantes aprobados (puntuación > 70)
def filtrar_estudiantes_aprobados(estudiantes):
    return list(filter(lambda x: x[1] > 70, estudiantes))

#funcion para aplicar un incremento del 5% a la puntuación de los estudiantes
def aplicar_incremento(estudiantes,):
    return list(map(lambda x: (x[0], x[1] * 1.05), estudiantes))


print(f"Estudiantes ordenados por puntuación ascendente: {ordenar_estudiantes(estudiantes)}")
print(f"Estudiantes aprobados (puntuación > 70): {filtrar_estudiantes_aprobados(estudiantes)}")
print(f"Estudiantes con incremento del 5% en la puntuación: {aplicar_incremento(estudiantes)}")




