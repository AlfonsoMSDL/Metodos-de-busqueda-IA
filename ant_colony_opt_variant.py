import random
import numpy as np
from collections import defaultdict

class AntColonyOptimization:
    def __init__(self, examenes, franjas, aulas, evaluador_fo,
                 num_hormigas, num_generaciones, alpha, beta, rho, Q):
        self.examenes = examenes
        self.franjas = franjas
        self.aulas = aulas
        self.evaluador = evaluador_fo
        
        self.num_hormigas = num_hormigas
        self.num_generaciones = num_generaciones
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.Q = Q
        
        self.opciones_por_examen = self._precalcular_opciones()
        self.feromonas = {}
        self.heuristica = {}
        self._inicializar_feromonas_y_heuristica()

    def _precalcular_opciones(self):
        opciones = {}
        for e_id, examen in self.examenes.items():
            opciones_e = []
            for f_id in examen.franjas_permitidas:
                for a_id, aula in self.aulas.items():
                    if f_id in aula.franjas_disponibles:
                        opciones_e.append((f_id, a_id))
            opciones[e_id] = opciones_e
        return opciones

    def _inicializar_feromonas_y_heuristica(self):
        for e_id, opciones in self.opciones_por_examen.items():
            examen = self.examenes[e_id]
            for f_id, a_id in opciones:
                clave = (e_id, f_id, a_id)
                self.feromonas[clave] = 1.0  # Nivel base
                
                aula = self.aulas[a_id]
                if aula.capacidad >= examen.estudiantes:
                    desperdicio = aula.capacidad - examen.estudiantes
                    self.heuristica[clave] = 1.0 / (1.0 + desperdicio)
                else:
                    self.heuristica[clave] = 1e-6 # Penalización severa por falta de cupo

    def _reparar_solucion(self, solucion):
        """
        Búsqueda Local: Si la hormiga construyó un horario con pocas fallas, 
        intenta reacomodar solo unos pocos exámenes para lograr la factibilidad.
        """
        sol = solucion.copy()
        _, h_act, _, _ = self.evaluador.evaluar(sol)
        
        if h_act == 0:
            return sol
            
        # Intentos de micro-ajuste rápido (Hill Climbing)
        for _ in range(1000):
            e_id = random.choice(list(self.examenes.keys()))
            f_act, a_act = sol[e_id]
            
            nueva_f, nueva_a = random.choice(self.opciones_por_examen[e_id])
            sol[e_id] = (nueva_f, nueva_a)
            
            _, h_nuevo, _, _ = self.evaluador.evaluar(sol)
            
            # Solo acepta el cambio si mejora o mantiene las violaciones
            if h_nuevo <= h_act:
                h_act = h_nuevo
                if h_act == 0:
                    break
            else:
                sol[e_id] = (f_act, a_act) # Revertir cambio
                
        return sol

    def _construir_solucion_hormiga(self):
        solucion = {}
        ocupacion_aula_franja = set()
        examenes_por_franja = defaultdict(list)
        
        # 1. ORDEN HEURÍSTICO: Asignar primero los exámenes más masivos
        examenes_ordenados = sorted(self.examenes.keys(), key=lambda e: self.examenes[e].estudiantes, reverse=True)

        for e_id in examenes_ordenados:
            examen = self.examenes[e_id]
            opciones = self.opciones_por_examen[e_id]
            probabilidades = []

            for f_id, a_id in opciones:
                clave = (e_id, f_id, a_id)
                aula = self.aulas[a_id]
                
                # Regla de Transición ACO: Feromona vs Heurística
                tau = self.feromonas[clave] ** self.alpha
                eta = self.heuristica[clave] ** self.beta
                
                # 2. PENALIZACIÓN DINÁMICA: Las hormigas evitan aulas que ya ocuparon
                penalizacion = 1.0
                if (f_id, a_id) in ocupacion_aula_franja:
                    penalizacion *= 1e-5
                if aula.capacidad < examen.estudiantes:
                    penalizacion *= 1e-5

                for e_asignado in examenes_por_franja[f_id]:
                    if self.evaluador.matriz_conflictos[e_id][e_asignado] > 0:
                        penalizacion *= 1e-5

                probabilidades.append(tau * eta * penalizacion)

            suma_prob = sum(probabilidades)
            if suma_prob == 0:
                prob_normalizadas = [1.0 / len(opciones)] * len(opciones)
            else:
                prob_normalizadas = [p / suma_prob for p in probabilidades]

            # 3. CONSTRUCCIÓN PROBABILÍSTICA (La ruleta)
            idx_elegido = np.random.choice(len(opciones), p=prob_normalizadas)
            f_elegida, a_elegida = opciones[idx_elegido]
            
            solucion[e_id] = (f_elegida, a_elegida)
            ocupacion_aula_franja.add((f_elegida, a_elegida))
            examenes_por_franja[f_elegida].append(e_id)

        # 4. BÚSQUEDA LOCAL (Híbrido)
        solucion = self._reparar_solucion(solucion)
        return solucion

    def ejecutar(self):
        mejor_solucion_global = None
        mejor_costo_global = float('inf')
        historial_costos = []

        for gen in range(self.num_generaciones):
            soluciones_generacion = []
            costos_generacion = []

            for _ in range(self.num_hormigas):
                solucion = self._construir_solucion_hormiga()
                costo, _, _, _ = self.evaluador.evaluar(solucion)
                soluciones_generacion.append(solucion)
                costos_generacion.append(costo)

                if costo < mejor_costo_global:
                    mejor_costo_global = costo
                    mejor_solucion_global = solucion.copy()

            historial_costos.append(mejor_costo_global)

            # Evaporación general
            for clave in self.feromonas:
                self.feromonas[clave] *= (1.0 - self.rho)

            # Depósito Elitista (Solo las 3 mejores hormigas depositan feromona)
            idx_mejores = np.argsort(costos_generacion)[:3]
            for idx in idx_mejores:
                solucion = soluciones_generacion[idx]
                costo = costos_generacion[idx]
                deposito = self.Q / (costo + 1e-5)
                for e_id, (f_id, a_id) in solucion.items():
                    clave = (e_id, f_id, a_id)
                    self.feromonas[clave] += deposito

        return mejor_solucion_global, mejor_costo_global, historial_costos