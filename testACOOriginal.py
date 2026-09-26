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
        {
            "id": "Linea_Base", 
            "num_hormigas": 40, 
            "num_generaciones": 150, 
            "alpha": 1.0, 
            "beta": 2.0, 
            "rho": 0.1, 
            "Q": 100000.0
        },
        
        # Ejemplo para cuando pases al Bloque 1 (descomentarás y agregarás más):
        # {
        #     "id": "B1_Config_01", 
        #     "num_hormigas": 50, 
        #     "num_generaciones": 200, 
        #     "alpha": 1.5, 
        #     "beta": 3.0, 
        #     "rho": 0.15, 
        #     "Q": 100000.0
        # },
    ]

    NUM_CORRIDAS = 30
    archivo_csv = 'resultados_ACO_experimentos.csv'
    
    # Crear el CSV con encabezados si no existe
    if not os.path.exists(archivo_csv):
        with open(archivo_csv, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['ID_Config', 'Corrida', 'Costo_Total', 'H', 'C_dia', 'P_libres', 'Factible', 'Tiempo_s'])

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
            
            # Guardado en caliente
            with open(archivo_csv, mode='a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([id_conf, corrida, mejor_costo, h, c_dia, p_libres, factible, round(tiempo_ejecucion, 3)])
                
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