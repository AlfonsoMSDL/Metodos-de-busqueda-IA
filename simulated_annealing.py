import random
import math
import copy

class SimulatedAnnealing:
    def __init__(self, examenes, franjas, aulas, evaluador_fo, 
                 t_inicial=10000, alpha=0.95, t_final=0.1, iteraciones_por_temp=100):
        """
        Inicializa el algoritmo de Enfriamiento Simulado.
        
        :param examenes: Diccionario de objetos Examen {id: obj}
        :param franjas: Diccionario de objetos Franja {id: obj}
        :param aulas: Diccionario de objetos Aula {id: obj}
        :param evaluador_fo: Instancia de la clase EvaluadorFO
        :param t_inicial: Temperatura inicial alta para permitir exploración
        :param alpha: Tasa de enfriamiento (ej. 0.95 -> reduce 5% cada paso)
        :param t_final: Condición de parada por temperatura baja
        :param iteraciones_por_temp: Movimientos a intentar antes de bajar la temperatura (L)
        """
        self.examenes = examenes
        self.franjas = franjas
        self.aulas = aulas
        self.evaluador = evaluador_fo
        
        # Hiperparámetros
        self.t_inicial = t_inicial
        self.alpha = alpha
        self.t_final = t_final
        self.iteraciones_por_temp = iteraciones_por_temp
        
        # Registro histórico para métricas y gráficas
        self.historial_costos = []
        
    def _generar_solucion_inicial(self):
        """
        Genera un punto de partida rápido. Asigna a cada examen una franja 
        aleatoria de sus permitidas, y un aula aleatoria disponible en esa franja.
        Retorna: dict {id_examen: (id_franja, id_aula)}
        """
        solucion = {}
        for id_examen, examen in self.examenes.items():
            # Escoger franja permitida al azar
            f_id = random.choice(examen.franjas_permitidas)
            
            # Buscar qué aulas están disponibles en esa franja
            aulas_validas = [a_id for a_id, aula in self.aulas.items() 
                             if f_id in aula.franjas_disponibles]
            
            # Escoger un aula al azar (asumimos que siempre habrá al menos una disponible)
            a_id = random.choice(aulas_validas)
            
            solucion[id_examen] = (f_id, a_id)
            
        return solucion

    def _generar_vecino(self, solucion_actual):
        vecino = solucion_actual.copy()
        
        # 1. Seleccionar un examen al azar
        id_examen = random.choice(list(self.examenes.keys()))
        examen = self.examenes[id_examen]
        f_actual, a_actual = vecino[id_examen]
        
        # 2. Elegir el tipo de mutación: 
        # 1 = Solo cambiar aula, 2 = Solo cambiar franja, 3 = Cambiar ambas
        opcion = random.choice([1, 2, 3])
        
        if opcion == 1: 
            # Cambiar solo el aula (mantiene la misma hora)
            aulas_validas = [a for a, aula in self.aulas.items() if f_actual in aula.franjas_disponibles]
            if aulas_validas:
                vecino[id_examen] = (f_actual, random.choice(aulas_validas))
                
        elif opcion == 2: 
            # Cambiar solo la franja (mantiene el mismo salón si está disponible)
            nueva_f = random.choice(examen.franjas_permitidas)
            aula_obj = self.aulas[a_actual]
            if nueva_f in aula_obj.franjas_disponibles:
                vecino[id_examen] = (nueva_f, a_actual)
            else:
                # Si el salón actual no abre en esa franja, toca cambiar ambas
                aulas_validas = [a for a, aula in self.aulas.items() if nueva_f in aula.franjas_disponibles]
                vecino[id_examen] = (nueva_f, random.choice(aulas_validas))
                
        else: 
            # Cambiar ambas al mismo tiempo (salto largo)
            nueva_f = random.choice(examen.franjas_permitidas)
            aulas_validas = [a for a, aula in self.aulas.items() if nueva_f in aula.franjas_disponibles]
            vecino[id_examen] = (nueva_f, random.choice(aulas_validas))
            
        return vecino

    def ejecutar(self):
        """
        Ejecuta el ciclo principal de Markov del algoritmo SA.
        Retorna la mejor solución encontrada y su costo.
        """
        # Paso 1: Estado inicial
        solucion_actual = self._generar_solucion_inicial()
        costo_actual, h, c_dia, p_libres = self.evaluador.evaluar(solucion_actual)
        
        # Rastrear al campeón histórico
        mejor_solucion = copy.deepcopy(solucion_actual)
        mejor_costo = costo_actual
        
        temperatura = self.t_inicial
        iteracion_global = 0
        
        # Bucle de enfriamiento externo
        while temperatura > self.t_final:
            
            # Bucle de equilibrio de Markov interno
            for _ in range(self.iteraciones_por_temp):
                iteracion_global += 1
                
                # Proponer un movimiento
                vecino = self._generar_vecino(solucion_actual)
                costo_vecino, v_h, v_c, v_p = self.evaluador.evaluar(vecino)
                
                # Calcular Delta E
                delta_e = costo_vecino - costo_actual
                
                # Criterio de Aceptación (Boltzmann)
                # Si el vecino es mejor, o si la probabilidad lo permite
                if delta_e < 0 or random.random() < math.exp(-delta_e / temperatura):
                    solucion_actual = vecino
                    costo_actual = costo_vecino
                    
                    # Actualizar al campeón si es el mejor absoluto visto hasta ahora
                    if costo_actual < mejor_costo:
                        mejor_costo = costo_actual
                        mejor_solucion = copy.deepcopy(solucion_actual)
                
                # Guardar registro para la gráfica de convergencia
                self.historial_costos.append(mejor_costo)
            
            # Enfriar el sistema
            temperatura *= self.alpha
            
        return mejor_solucion, mejor_costo, self.historial_costos