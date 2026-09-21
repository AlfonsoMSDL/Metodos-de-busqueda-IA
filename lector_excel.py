import pandas as pd
from modelos import Examen, Franja, Aula, Matricula

class LectorInstancia:
    def __init__(self, ruta_archivo):
        self.ruta_archivo = ruta_archivo

    def cargar_datos(self):
        """
        Lee el archivo Excel y retorna diccionarios para consultas rápidas O(1)
        y una lista para las matrículas.
        """
        # Cargar todas las hojas necesarias
        df_examenes = pd.read_excel(self.ruta_archivo, sheet_name='Examenes')
        df_franjas = pd.read_excel(self.ruta_archivo, sheet_name='Franjas')
        df_aulas = pd.read_excel(self.ruta_archivo, sheet_name='Aulas')
        df_matriculas = pd.read_excel(self.ruta_archivo, sheet_name='Matriculas')

        # 1. Extraer Exámenes (Retorna un diccionario { 'E01': ObjetoExamen, ... })
        examenes = {}
        for _, row in df_examenes.iterrows():
            examen = Examen(
                id_examen=row['Examen'],
                estudiantes=row['Estudiantes'],
                duracion=row['Duracion_min'],
                franjas_permitidas=row['Franjas_permitidas']
            )
            examenes[examen.id_examen] = examen

        # 2. Extraer Franjas (Retorna diccionario { 'F1': ObjetoFranja, ... })
        franjas = {}
        for _, row in df_franjas.iterrows():
            franja = Franja(
                id_franja=row['Franja'],
                dia=row['Dia'],
                horario=row['Horario']
            )
            franjas[franja.id_franja] = franja

        # 3. Extraer Aulas (Retorna diccionario { 'A101': ObjetoAula, ... })
        aulas = {}
        for _, row in df_aulas.iterrows():
            aula = Aula(
                id_aula=row['Aula'],
                capacidad=row['Capacidad'],
                franjas_disponibles=row['Franjas_disponibles']
            )
            aulas[aula.id_aula] = aula

        # 4. Extraer Matrículas (Retorna una lista simple de Objetos Matricula)
        matriculas = []
        for _, row in df_matriculas.iterrows():
            matricula = Matricula(
                id_estudiante=row['Estudiante'],
                id_examen=row['Examen']
            )
            matriculas.append(matricula)

        return examenes, franjas, aulas, matriculas