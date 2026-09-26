import time
import csv
import os
import matplotlib.pyplot as plt
from lector_excel import LectorInstancia
from funcion_objetivo import EvaluadorFO

# IMPORTANTE: Asegúrate de importar la clase desde el archivo donde tienes el ACO Original (puro)
# Según tu captura de pantalla anterior, el archivo se llama 'ant_colony_opt_original.py'
from ant_colony_opt_original import AntColonyOptimization

def main():
    print("1. Cargando datos para experimentación ACO (Original)...")
    lector = LectorInstancia('data/instancia_examenes_tema02.xlsx')
    examenes, franjas, aulas, matriculas = lector.cargar_datos()
    evaluador = EvaluadorFO(examenes, franjas, aulas, matriculas)

    # =========================================================================
    # EL MOTOR DE CONFIGURACIONES PARA ACO
    # =========================================================================
    configuraciones_a_probar = [
        # C1: Enjambre pequeño, muchas generaciones, evaporación alta (olvidan rápido, evitan estancarse).
        {"id": "B1_ACO_01", "num_hormigas": 15, "num_generaciones": 400, "alpha": 1.0, "beta": 2.0, "rho": 0.4, "Q": 100000.0},
        
        # C2: Enjambre masivo, pocas generaciones, evaporación baja (memoria fuerte a corto plazo).
        {"id": "B1_ACO_02", "num_hormigas": 100, "num_generaciones": 60, "alpha": 1.0, "beta": 2.0, "rho": 0.05, "Q": 100000.0},
        
        # C3: Guiadas fuertemente por la Feromona (alpha alto), ignoran casi la capacidad del aula (beta bajo).
        {"id": "B1_ACO_03", "num_hormigas": 40, "num_generaciones": 150, "alpha": 3.0, "beta": 0.5, "rho": 0.1, "Q": 100000.0},
        
        # C4: Comportamiento Ávido/Heurístico. Ignoran la feromona, se guían por el tamaño del aula (beta muy alto).
        {"id": "B1_ACO_04", "num_hormigas": 40, "num_generaciones": 150, "alpha": 0.5, "beta": 4.0, "rho": 0.1, "Q": 100000.0},
        
        # C5: Balance simétrico entre memoria (alpha) y heurística (beta) con evaporación estándar.
        {"id": "B1_ACO_05", "num_hormigas": 50, "num_generaciones": 200, "alpha": 2.0, "beta": 2.0, "rho": 0.15, "Q": 100000.0},
        
        # C6: Evaporación extrema (rho=0.8). La colonia olvida casi todo en cada generación.
        {"id": "B1_ACO_06", "num_hormigas": 40, "num_generaciones": 150, "alpha": 1.0, "beta": 2.0, "rho": 0.8, "Q": 100000.0},
        
        # C7: Evaporación ultralenta (rho=0.01). El rastro se vuelve permanente rápidamente.
        {"id": "B1_ACO_07", "num_hormigas": 60, "num_generaciones": 200, "alpha": 1.0, "beta": 2.0, "rho": 0.01, "Q": 100000.0},
        
        # C8: Enjambre mediano, fuerte peso a la memoria histórica (alpha alto), evaporación moderada.
        {"id": "B1_ACO_08", "num_hormigas": 30, "num_generaciones": 250, "alpha": 2.5, "beta": 1.5, "rho": 0.2, "Q": 100000.0},
        
        # C9: Alta dependencia de la heurística (beta) con un enjambre grande para explotar rápido.
        {"id": "B1_ACO_09", "num_hormigas": 80, "num_generaciones": 100, "alpha": 1.0, "beta": 3.5, "rho": 0.1, "Q": 100000.0},
        
        # C10: Alta exploración. Pocas hormigas, evaporación alta, mucha importancia a la intuición (beta).
        {"id": "B1_ACO_10", "num_hormigas": 20, "num_generaciones": 300, "alpha": 0.8, "beta": 3.0, "rho": 0.5, "Q": 100000.0},
    ]

    NUM_CORRIDAS = 30
    archivo_csv = 'resultados_ACO_experimentos.csv'
    
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
        plt.title(f'Convergencia ACO Original - Mejor Corrida ({id_conf})')
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