import time
import matplotlib.pyplot as plt
from lector_excel import LectorInstancia
from funcion_objetivo import EvaluadorFO
from simulated_annealing import SimulatedAnnealing

def main():
    print("1. Cargando datos de la instancia desde Excel...")
    lector = LectorInstancia('data/instancia_examenes_tema02.xlsx')
    examenes, franjas, aulas, matriculas = lector.cargar_datos()
    print(f"   - {len(examenes)} Exámenes, {len(franjas)} Franjas, {len(aulas)} Aulas cargados.")

    print("2. Inicializando Función Objetivo y matriz de conflictos...")
    evaluador = EvaluadorFO(examenes, franjas, aulas, matriculas)

    print("3. Configurando algoritmo de Enfriamiento Simulado (Línea Base)...")
    # Configuración de hiperparámetros más lenta y profunda
    sa = SimulatedAnnealing(
        examenes=examenes,
        franjas=franjas,
        aulas=aulas,
        evaluador_fo=evaluador,
        t_inicial=2000000,        # 2 Millones (Cubre penalizaciones altísimas de cruces de estudiantes)
        alpha=0.99,               # Enfriamiento lentísimo (0.99 en vez de 0.90 o 0.95)
        t_final=0.1,
        iteraciones_por_temp=400  # Muchas más oportunidades de movimiento en cada grado de temperatura
    )

    print("4. Ejecutando optimización... (El procesador está trabajando, espera unos segundos)")
    inicio = time.time()
    mejor_solucion, mejor_costo, historial = sa.ejecutar()
    fin = time.time()

    print("\n" + "="*40)
    print("      RESULTADOS DE LA OPTIMIZACIÓN      ")
    print("="*40)
    print(f"Tiempo de ejecución: {fin - inicio:.3f} segundos")

    # Descomponer el costo de la mejor solución encontrada
    _, h, c_dia, p_libres = evaluador.evaluar(mejor_solucion)
    
    print(f"\nCosto Total de la FO: {mejor_costo}")
    print(f"Violaciones Duras (H): {h}")
    if h == 0:
        print("   -> ESTADO: ¡Solución Factible! (Horario válido)")
    else:
        print("   -> ESTADO: Solución No Factible (Requiere ajustar hiperparámetros)")
        
    print(f"Casos estudiante-día (C_dia): {c_dia}")

    # ... código anterior ...
    print(f"Puestos de aula no utilizados (P_libres): {p_libres}")
    print("="*40)

    # --- NUEVO CÓDIGO PARA MOSTRAR Y GUARDAR LA SOLUCIÓN ---
    print("\n" + "="*40)
    print("          HORARIO GENERADO          ")
    print("="*40)
    print(f"{'Examen':<10} | {'Franja':<10} | {'Aula':<10}")
    print("-" * 35)
    
    # Ordenar alfabéticamente por examen para mejor lectura
    for id_examen, (id_franja, id_aula) in sorted(mejor_solucion.items()):
        print(f"{id_examen:<10} | {id_franja:<10} | {id_aula:<10}")

    # Guardar en un archivo CSV
    import csv
    with open('horario_solucion.csv', 'w', newline='', encoding='utf-8') as archivo_csv:
        escritor = csv.writer(archivo_csv)
        escritor.writerow(['Examen', 'Franja', 'Aula'])
        for id_examen, (id_franja, id_aula) in sorted(mejor_solucion.items()):
            escritor.writerow([id_examen, id_franja, id_aula])
            
    print("-" * 35)
    print("El horario completo se ha guardado en 'horario_solucion.csv'")
    # ... aquí sigue el código de la gráfica plt.show() o plt.savefig() ...

    print("\n5. Generando gráfica de convergencia...")
    plt.figure(figsize=(10, 6))
    plt.plot(historial, color='b', linewidth=2)
    plt.title('Curva de Convergencia - Enfriamiento Simulado (SA)', fontsize=14)
    plt.xlabel('Iteraciones de Temperatura (Enfriamiento)', fontsize=12)
    plt.ylabel('Costo de la Función Objetivo', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig("convergencia_SA.png", dpi=300)
    print("Gráfica guardada como 'convergencia_SA.png' en la raíz del proyecto.")

if __name__ == "__main__":
    main()