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
    configuraciones_a_probar = [
        # B2: Sintonización fina alrededor del campeón B1_SA_02 (Alpha alto, buscando eficiencia en tiempo)
        {"id": "B2_SA_01", "t_inicial": 5000000, "alpha": 0.996, "t_final": 0.1, "iteraciones": 400},
        {"id": "B2_SA_02", "t_inicial": 5000000, "alpha": 0.994, "t_final": 0.1, "iteraciones": 450},
        {"id": "B2_SA_03", "t_inicial": 4000000, "alpha": 0.995, "t_final": 0.1, "iteraciones": 500},
        {"id": "B2_SA_04", "t_inicial": 4000000, "alpha": 0.993, "t_final": 0.1, "iteraciones": 400},
        {"id": "B2_SA_05", "t_inicial": 3000000, "alpha": 0.997, "t_final": 0.1, "iteraciones": 300}, # Alpha extremo, menos iteraciones
        {"id": "B2_SA_06", "t_inicial": 3000000, "alpha": 0.995, "t_final": 0.1, "iteraciones": 350},
        {"id": "B2_SA_07", "t_inicial": 6000000, "alpha": 0.992, "t_final": 0.1, "iteraciones": 500},
        {"id": "B2_SA_08", "t_inicial": 5000000, "alpha": 0.995, "t_final": 0.1, "iteraciones": 300}, # Prueba de velocidad agresiva
        {"id": "B2_SA_09", "t_inicial": 4500000, "alpha": 0.994, "t_final": 0.1, "iteraciones": 550},
        {"id": "B2_SA_10", "t_inicial": 5000000, "alpha": 0.998, "t_final": 0.1, "iteraciones": 250}, # Enfriamiento casi estático
    ]

    NUM_CORRIDAS = 30
    archivo_csv = 'resultados_SA_experimentos_bloque2.csv'
    
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