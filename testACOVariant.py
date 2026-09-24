import time
import csv
import matplotlib.pyplot as plt
from lector_excel import LectorInstancia
from funcion_objetivo import EvaluadorFO
from ant_colony_opt_variant import AntColonyOptimization

def main():
    print("1. Cargando datos de la instancia desde Excel...")
    lector = LectorInstancia('data/instancia_examenes_tema02.xlsx')
    examenes, franjas, aulas, matriculas = lector.cargar_datos()
    print(f"   - {len(examenes)} Exámenes, {len(franjas)} Franjas, {len(aulas)} Aulas cargados.")

    print("2. Inicializando Función Objetivo y matriz de conflictos...")
    evaluador = EvaluadorFO(examenes, franjas, aulas, matriculas)

    print("3. Configurando algoritmo de Colonia de Hormigas (ACO variante)...")

    aco = AntColonyOptimization(
        examenes=examenes,
        franjas=franjas,
        aulas=aulas,
        evaluador_fo=evaluador,
        num_hormigas=40,
        num_generaciones=150,
        alpha=1.0,
        beta=2.0,
        rho=0.1,
        Q=100000.0
    )

    print("4. Ejecutando optimización ACO variante... (Por favor espera)")
    inicio = time.time()
    mejor_solucion, mejor_costo, historial = aco.ejecutar()
    fin = time.time()

    _, h, c_dia, p_libres = evaluador.evaluar(mejor_solucion)

    print("\n" + "="*40)
    print("      RESULTADOS OPTIMIZACIÓN ACO      ")
    print("="*40)
    print(f"Tiempo de ejecución: {fin - inicio:.3f} segundos")
    print(f"Costo Total de la FO: {mejor_costo}")
    print(f"Violaciones Duras (H): {h}")
    if h == 0:
        print("   -> ESTADO: ¡Solución Factible! (Horario válido)")
    else:
        print("   -> ESTADO: Solución No Factible (Requiere ajustar hiperparámetros)")
        
    print(f"Casos estudiante-día (C_dia): {c_dia}")
    print(f"Puestos de aula no utilizados (P_libres): {p_libres}")
    print("="*40)

    # --- IMPRIMIR Y GUARDAR SOLUCIÓN EN TABLA ---
    print("\n" + "="*40)
    print("          HORARIO GENERADO (ACO)          ")
    print("="*40)
    print(f"{'Examen':<10} | {'Franja':<10} | {'Aula':<10}")
    print("-" * 35)
    
    for id_examen, (id_franja, id_aula) in sorted(mejor_solucion.items()):
        print(f"{id_examen:<10} | {id_franja:<10} | {id_aula:<10}")

    with open('horario_solucion_aco_variant.csv', 'w', newline='', encoding='utf-8') as archivo_csv:
        escritor = csv.writer(archivo_csv)
        escritor.writerow(['Examen', 'Franja', 'Aula'])
        for id_examen, (id_franja, id_aula) in sorted(mejor_solucion.items()):
            escritor.writerow([id_examen, id_franja, id_aula])
            
    print("-" * 35)
    print("El horario se ha guardado en 'horario_solucion_aco_variant.csv'")

    # --- GENERAR Y GUARDAR GRÁFICA DE CONVERGENCIA ---
    print("\n5. Generando gráfica de convergencia...")
    plt.figure(figsize=(10, 6))
    plt.plot(historial, color='g', linewidth=2)
    plt.title('Curva de Convergencia - Optimización por Colonia de Hormigas (ACO Variante)', fontsize=14)
    plt.xlabel('Generaciones', fontsize=12)
    plt.ylabel('Costo de la Función Objetivo', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig("convergencia_ACO_variant.png", dpi=300)
    print("Gráfica guardada como 'convergencia_ACO_variant.png' en la raíz del proyecto.")

if __name__ == "__main__":
    main()