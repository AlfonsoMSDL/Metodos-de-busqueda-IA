from lector_excel import LectorInstancia

# Inicializar y leer
lector = LectorInstancia('data/instancia_examenes_tema02.xlsx')
examenes, franjas, aulas, matriculas = lector.cargar_datos()

# Ejemplo de lo fácil que es consultar gracias a los diccionarios:
print("Aula A102:", aulas['A102'].capacidad)
print("El examen E01 puede darse en:", examenes['E01'].franjas_permitidas)