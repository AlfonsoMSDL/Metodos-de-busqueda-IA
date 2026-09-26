import time
import csv
import os
import matplotlib.pyplot as plt
from lector_excel import LectorInstancia
from funcion_objetivo import EvaluadorFO

# IMPORTANTE: Asegúrate de importar la clase desde el archivo donde tienes el ACO Original (puro)
# Según tu captura de pantalla anterior, el archivo se llama 'ant_colony_opt_original.py'
from ant_colony_opt import AntColonyOptimization

def main():
    print("1. Cargando datos para experimentación ACO...")
    lector = LectorInstancia('data/instancia_examenes_tema02.xlsx')
    examenes, franjas, aulas, matriculas = lector.cargar_datos()
    evaluador = EvaluadorFO(examenes, franjas, aulas, matriculas)

    # =========================================================================
    # EL MOTOR DE CONFIGURACIONES PARA ACO
    # =========================================================================
    configuraciones_a_probar = [
        # B2: Sintonización fina alrededor del campeón B1_ACO_07 (Evaporación ultra baja, potenciando feromonas)
        {"id": "B2_ACO_01", "num_hormigas": 60, "num_generaciones": 200, "alpha": 1.2, "beta": 2.0, "rho": 0.01, "Q": 100000.0},
        {"id": "B2_ACO_02", "num_hormigas": 60, "num_generaciones": 200, "alpha": 1.0, "beta": 2.0, "rho": 0.005, "Q": 100000.0}, # Evaporación extrema baja
        {"id": "B2_ACO_03", "num_hormigas": 70, "num_generaciones": 180, "alpha": 1.0, "beta": 2.0, "rho": 0.01, "Q": 100000.0},
        {"id": "B2_ACO_04", "num_hormigas": 50, "num_generaciones": 250, "alpha": 1.0, "beta": 2.0, "rho": 0.02, "Q": 100000.0},
        {"id": "B2_ACO_05", "num_hormigas": 60, "num_generaciones": 200, "alpha": 1.5, "beta": 1.8, "rho": 0.01, "Q": 100000.0},
        {"id": "B2_ACO_06", "num_hormigas": 65, "num_generaciones": 200, "alpha": 1.1, "beta": 2.2, "rho": 0.015, "Q": 100000.0},
        {"id": "B2_ACO_07", "num_hormigas": 60, "num_generaciones": 150, "alpha": 1.0, "beta": 2.0, "rho": 0.01, "Q": 100000.0}, # Prueba de velocidad
        {"id": "B2_ACO_08", "num_hormigas": 55, "num_generaciones": 220, "alpha": 1.3, "beta": 1.9, "rho": 0.008, "Q": 100000.0},
        {"id": "B2_ACO_09", "num_hormigas": 60, "num_generaciones": 200, "alpha": 1.0, "beta": 2.5, "rho": 0.01, "Q": 100000.0}, # Subiendo heurística un poco
        {"id": "B2_ACO_10", "num_hormigas": 80, "num_generaciones": 150, "alpha": 1.0, "beta": 2.0, "rho": 0.02, "Q": 100000.0},
    ]

    NUM_CORRIDAS = 30
    archivo_csv = 'resultados_ACO_experimentos_bloque2.csv'
    
    # Crear el CSV con encabezados si no existe
    if not os.path.exists(archivo_csv):
        with open(archivo_csv, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['ID_Config', 'Corrida', 'Costo_Total', 'H', 'C_dia', 'P_libres', 'Factible', 'Tiempo_s', 'Iteracion_Mejor'])

    # BUCLE EXTERNO: Recorre cada configuración en la lista
    for config in configuraciones_a_probar:
        id_conf = config["id"]
        print(f"\n==================================================")
        print(f" EVALUANDO CONFIGURACIÓN ACO: {id_conf}")
        print(f" Hormigas={config['num_hormigas']} | Gen={config['num_generaciones']} | Alpha={config['alpha']} | Beta={config['beta']} | Rho={config['rho']}")
        print(f"==================================================")

        mejor_costo_historico = float('inf')
        mejor_historial = []

        # BUCLE INTERNO: Las 30 ejecuciones independientes
        for corrida in range(1, NUM_CORRIDAS + 1):
            print(f"  -> Ejecutando corrida {corrida:02d}/{NUM_CORRIDAS}...", end='', flush=True)
            
            aco = AntColonyOptimization(
                examenes=examenes, 
                franjas=franjas, 
                aulas=aulas, 
                evaluador_fo=evaluador,
                num_hormigas=config["num_hormigas"],
                num_generaciones=config["num_generaciones"],
                alpha=config["alpha"],
                beta=config["beta"],
                rho=config["rho"],
                Q=config["Q"]
            )
            
            inicio = time.time()
            mejor_solucion, mejor_costo, historial = aco.ejecutar()
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

            # Identificar la mejor corrida para la gráfica de convergencia
            if mejor_costo < mejor_costo_historico:
                mejor_costo_historico = mejor_costo
                mejor_historial = historial

        # Generar gráfica de la mejor corrida para esta configuración
        plt.figure(figsize=(10, 6))
        plt.plot(mejor_historial, color='green', linewidth=2)
        plt.title(f'Convergencia ACO - Mejor Corrida ({id_conf})')
        plt.xlabel('Generaciones')
        plt.ylabel('Costo de la Función Objetivo')
        plt.grid(True, linestyle='--', alpha=0.7)
        nombre_grafica = f"convergencia_ACO_{id_conf}.png"
        plt.savefig(nombre_grafica, dpi=300)
        plt.close() # Cerrar figura para liberar memoria
        print(f"\n* Gráfica de la mejor corrida guardada como '{nombre_grafica}'")

    print(f"\nTodos los experimentos finalizaron. Datos asegurados en '{archivo_csv}'")

if __name__ == "__main__":
    main()