class Examen:
    def __init__(self, id_examen, estudiantes, duracion, franjas_permitidas):
        self.id_examen = id_examen
        self.estudiantes = int(estudiantes)
        self.duracion = int(duracion)
        # Convertimos 'F1,F2,F6,F7' en una lista ['F1', 'F2', 'F6', 'F7']
        self.franjas_permitidas = [f.strip() for f in str(franjas_permitidas).split(',')]

    def __repr__(self):
        return f"Examen({self.id_examen}, Estudiantes: {self.estudiantes})"

class Franja:
    def __init__(self, id_franja, dia, horario):
        self.id_franja = id_franja
        self.dia = dia
        self.horario = horario

    def __repr__(self):
        return f"Franja({self.id_franja}, {self.dia} {self.horario})"

class Aula:
    def __init__(self, id_aula, capacidad, franjas_disponibles):
        self.id_aula = id_aula
        self.capacidad = int(capacidad)
        self.franjas_disponibles = [f.strip() for f in str(franjas_disponibles).split(',')]

    def __repr__(self):
        return f"Aula({self.id_aula}, Cap: {self.capacidad})"

class Matricula:
    def __init__(self, id_estudiante, id_examen):
        self.id_estudiante = id_estudiante
        self.id_examen = id_examen

    def __repr__(self):
        return f"Matricula({self.id_estudiante} -> {self.id_examen})"