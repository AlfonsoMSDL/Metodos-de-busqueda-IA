import time
import csv
import os
import matplotlib.pyplot as plt
from lector_excel import LectorInstancia
from funcion_objetivo import EvaluadorFO
from simulated_annealing import SimulatedAnnealing

def main():
    print("1. Cargando datos para experimentación SA...")
    lector = LectorInstancia('data/instancia_examenes_tema02.xlsx')
    examenes, franjas, aulas, matriculas = lector.cargar_datos()
    evaluador = EvaluadorFO(examenes, franjas, aulas, matriculas)

    # =========================================================================
    # EL MOTOR DE CONFIGURACIONES
    # Para la Línea Base, dejas solo el primer elemento.
    """configuraciones_a_probar = [
            {
                "id": "Linea_Base", 
                "t_inicial": 2000000, 
                "alpha": 0.99, 
                "t_final": 0.1, 
                "iteraciones": 400
            }
        ]"""
    # Para el Bloque 1, simplemente agregas 10 diccionarios más aquí abajo.
    # =========================================================================
    configuraciones_a_probar = [
        # C1: Enfriamiento rápido y baja temperatura. (Búsqueda agresiva/ávida)
        {"id": "B1_SA_01", "t_inicial": 500000, "alpha": 0.85, "t_final": 0.1, "iteraciones": 200},
        
        # C2: Enfriamiento muy lento y alta temperatura. (Máxima exploración global, tomará más tiempo)
        {"id": "B1_SA_02", "t_inicial": 5000000, "alpha": 0.995, "t_final": 0.1, "iteraciones": 600},
        
        # C3: Temperatura inicial moderada pero muchas iteraciones por nivel. (Explotación profunda)
        {"id": "B1_SA_03", "t_inicial": 2000000, "alpha": 0.90, "t_final": 0.1, "iteraciones": 1000},
        
        # C4: Temperatura extrema, enfriamiento estándar. (Permite aceptar muchos errores al inicio)
        {"id": "B1_SA_04", "t_inicial": 10000000, "alpha": 0.95, "t_final": 0.1, "iteraciones": 400},
        
        # C5: Micro-búsqueda. Temperatura baja, enfriamiento lentísimo. (Afinación fina)
        {"id": "B1_SA_05", "t_inicial": 100000, "alpha": 0.999, "t_final": 0.1, "iteraciones": 200},
        
        # C6: Pocas iteraciones pero enfriamiento conservador. (Descenso gradual ligero)
        {"id": "B1_SA_06", "t_inicial": 2000000, "alpha": 0.98, "t_final": 0.1, "iteraciones": 100},
        
        # C7: Búsqueda equilibrada de convergencia rápida.
        {"id": "B1_SA_07", "t_inicial": 1000000, "alpha": 0.92, "t_final": 0.1, "iteraciones": 500},
        
        # C8: Congelamiento abrupto. Alta temperatura que cae drásticamente.
        {"id": "B1_SA_08", "t_inicial": 8000000, "alpha": 0.80, "t_final": 0.1, "iteraciones": 300},
        
        # C9: Alta cantidad de iteraciones con enfriamiento estándar.
        {"id": "B1_SA_09", "t_inicial": 3000000, "alpha": 0.95, "t_final": 0.1, "iteraciones": 800},
        
        # C10: Baja temperatura inicial, enfriamiento rápido. (Casi un Hill Climbing, cero tolerancia a errores)
        {"id": "B1_SA_10", "t_inicial": 50000, "alpha": 0.80, "t_final": 0.1, "iteraciones": 400},
    ]

    NUM_CORRIDAS = 30
    archivo_csv = 'resultados_SA_experimentos.csv'
    
    # Crear el CSV con encabezados si no existe
    if not os.path.exists(archivo_csv):
        with open(archivo_csv, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['ID_Config', 'Corrida', 'Costo_Total', 'H', 'C_dia', 'P_libres', 'Factible', 'Tiempo_s', 'Iteracion_Mejor'])

    # BUCLE EXTERNO: Recorre cada configuración que hayas puesto en la lista
    for config in configuraciones_a_probar:
        id_conf = config["id"]
        print(f"\n==================================================")
        print(f" EVALUANDO CONFIGURACIÓN: {id_conf}")
        print(f" Parámetros: T={config['t_inicial']}, Alpha={config['alpha']}, Iter={config['iteraciones']}")
        print(f"==================================================")

        mejor_costo_historico = float('inf')
        mejor_historial = []

        # BUCLE INTERNO: Las 30 ejecuciones independientes obligatorias
        for corrida in range(1, NUM_CORRIDAS + 1):
            print(f"  -> Ejecutando corrida {corrida:02d}/{NUM_CORRIDAS}...", end='', flush=True)
            
            sa = SimulatedAnnealing(
                examenes=examenes, franjas=franjas, aulas=aulas, evaluador_fo=evaluador,
                t_inicial=config["t_inicial"], 
                alpha=config["alpha"], 
                t_final=config["t_final"], 
                iteraciones_por_temp=config["iteraciones"]
            )
            
            inicio = time.time()
            mejor_solucion, mejor_costo, historial = sa.ejecutar()
            fin = time.time()
            
            tiempo_ejecucion = fin - inicio
            _, h, c_dia, p_libres = evaluador.evaluar(mejor_solucion)
            factible = "SI" if h == 0 else "NO"

            # --- NUEVA LÍNEA PARA CALCULAR LA ITERACIÓN ---
            # Busca en qué índice del historial se alcanzó el costo más bajo por primera vez
            iteracion_mejor = historial.index(min(historial))
            
            # Guardado en caliente: se abre, escribe y cierra para no perder datos
            # Guardado en caliente (Agregamos iteracion_mejor al final)
            with open(archivo_csv, mode='a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([id_conf, corrida, mejor_costo, h, c_dia, p_libres, factible, round(tiempo_ejecucion, 3), iteracion_mejor])
                
            print(f" Costo: {mejor_costo} | H: {h} | Tiempo: {tiempo_ejecucion:.2f}s")

            # Identificar la mejor corrida de esta configuración para la gráfica
            if mejor_costo < mejor_costo_historico:
                mejor_costo_historico = mejor_costo
                mejor_historial = historial

        # Generar gráfica de la mejor corrida para esta configuración específica
        plt.figure(figsize=(10, 6))
        plt.plot(mejor_historial, color='blue', linewidth=2)
        plt.title(f'Convergencia SA - Mejor Corrida ({id_conf})')
        plt.xlabel('Iteraciones (Temperatura)')
        plt.ylabel('Costo de la Función Objetivo')
        plt.grid(True, linestyle='--', alpha=0.7)
        nombre_grafica = f"convergencia_SA_{id_conf}.png"
        plt.savefig(nombre_grafica, dpi=300)
        plt.close() # Cerrar la figura para no saturar la memoria RAM
        print(f"\n* Gráfica de la mejor corrida guardada como '{nombre_grafica}'")

    print(f"\nTodos los experimentos finalizaron. Datos asegurados en '{archivo_csv}'")

if __name__ == "__main__":
    main()