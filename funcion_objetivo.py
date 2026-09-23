from collections import defaultdict

class EvaluadorFO:
    def __init__(self, examenes, franjas, aulas, matriculas):
        self.examenes = examenes      # dict {id_examen: ObjetoExamen}
        self.franjas = franjas        # dict {id_franja: ObjetoFranja}
        self.aulas = aulas            # dict {id_aula: ObjetoAula}
        self.matriculas = matriculas  # list [ObjetoMatricula]

        # 1. Mapeo de Día por Franja
        self.dia_por_franja = {f_id: f_obj.dia for f_id, f_obj in franjas.items()}

        # 2. Construir Matriz de Conflictos
        self.matriz_conflictos = self._construir_matriz_conflictos()

    def _construir_matriz_conflictos(self):
        # Mapear estudiante -> lista de exámenes
        estudiante_examenes = defaultdict(list)
        for m in self.matriculas:
            estudiante_examenes[m.id_estudiante].append(m.id_examen)

        # Contar pares de exámenes compartidos
        conflictos = defaultdict(lambda: defaultdict(int))
        for lista_e in estudiante_examenes.values():
            for i in range(len(lista_e)):
                for j in range(i + 1, len(lista_e)):
                    e1, e2 = lista_e[i], lista_e[j]
                    conflictos[e1][e2] += 1
                    conflictos[e2][e1] += 1
        return conflictos

    def evaluar(self, solucion):
        """
        solucion: dict {id_examen: (id_franja, id_aula)}
        Retorna: costo_total, H, C_dia, P_libres
        """
        H = 0
        C_dia = 0
        P_libres = 0

        ocupacion_aula_franja = defaultdict(list)
        examenes_por_franja = defaultdict(list)
        examenes_por_dia = defaultdict(list)

        # 1. Evaluación Examen por Examen (Capacidad, Franjas permitidas, Aulas disponibles)
        for e_id, (f_id, a_id) in solucion.items():
            examen = self.examenes[e_id]
            aula = self.aulas[a_id]

            # DURA: Franja permitida
            if f_id not in examen.franjas_permitidas:
                H += 1

            # DURA: Aula disponible en la franja
            if f_id not in aula.franjas_disponibles:
                H += 1

            # DURA: Capacidad del aula
            if aula.capacidad < examen.estudiantes:
                H += 1
            else:
                # BLANDA: Puestos libres (solo si no viola capacidad)
                P_libres += (aula.capacidad - examen.estudiantes)

            # Agrupar para verificar sobreocupación y cruces
            ocupacion_aula_franja[(f_id, a_id)].append(e_id)
            examenes_por_franja[f_id].append(e_id)
            dia = self.dia_por_franja[f_id]
            examenes_por_dia[(dia, f_id)].append(e_id)

        # DURA: Un aula no puede tener > 1 examen en la misma franja
        for _, lista_ex in ocupacion_aula_franja.items():
            if len(lista_ex) > 1:
                H += (len(lista_ex) - 1)

        # DURA: Estudiantes con 2 exámenes en la MISMA franja
        for f_id, lista_ex in examenes_por_franja.items():
            for i in range(len(lista_ex)):
                for j in range(i + 1, len(lista_ex)):
                    e1, e2 = lista_ex[i], lista_ex[j]
                    H += self.matriz_conflictos[e1][e2]

        # BLANDA (C_dia): Estudiantes con 2 exámenes el MISMO día pero distinta franja
        dias_agrupados = defaultdict(list)
        for (dia, f_id), lista_ex in examenes_por_dia.items():
            dias_agrupados[dia].append((f_id, lista_ex))

        for dia, franjas_list in dias_agrupados.items():
            for i in range(len(franjas_list)):
                for j in range(i + 1, len(franjas_list)):
                    f1_id, ex1_list = franjas_list[i]
                    f2_id, ex2_list = franjas_list[j]
                    # Si son franjas diferentes del mismo día
                    if f1_id != f2_id:
                        for e1 in ex1_list:
                            for e2 in ex2_list:
                                C_dia += self.matriz_conflictos[e1][e2]

        # Calcular costo según la fórmula oficial
        costo_total = 100000 * H + 100 * C_dia + P_libres
        return costo_total, H, C_dia, P_libres