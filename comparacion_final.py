import pandas as pd
import matplotlib.pyplot as plt
import os

def generar_boxplots(df, algoritmo, id_base, id_b1, id_b2):
    """Genera y guarda el diagrama de caja comparativo para un algoritmo."""
    datos_filtrados = df[df['ID_Config'].isin([id_base, id_b1, id_b2])]
    datos_filtrados['ID_Config'] = pd.Categorical(
        datos_filtrados['ID_Config'], 
        categories=[id_base, id_b1, id_b2], 
        ordered=True
    )
    
    plt.figure(figsize=(10, 6))
    datos_filtrados.boxplot(column='Costo_Total', by='ID_Config', grid=True, patch_artist=True)
    plt.title(f'Comparación de Costos - {algoritmo}')
    plt.suptitle('') 
    plt.xlabel('Configuración')
    plt.ylabel('Costo de la Función Objetivo')
    
    nombre_archivo = f'boxplot_comparativo_{algoritmo}.png'
    plt.savefig(nombre_archivo, dpi=300)
    plt.close('all')
    print(f"* Diagrama de caja guardado: {nombre_archivo}")

def generar_graficos_barras(df_sa, df_aco, campeon_sa, campeon_aco):
    """Genera los 3 gráficos de barras comparativos de la validación final."""
    # Extraer datos de los campeones
    datos_sa = df_sa[df_sa['ID_Config'] == campeon_sa]
    datos_aco = df_aco[df_aco['ID_Config'] == campeon_aco]
    
    # Calcular las 3 métricas clave
    cv_sa = (datos_sa['Costo_Total'].std() / datos_sa['Costo_Total'].mean()) * 100
    cv_aco = (datos_aco['Costo_Total'].std() / datos_aco['Costo_Total'].mean()) * 100
    
    tiempo_sa = datos_sa['Tiempo_s'].mean()
    tiempo_aco = datos_aco['Tiempo_s'].mean()
    
    iter_sa = datos_sa['Iteracion_Mejor'].mean()
    iter_aco = datos_aco['Iteracion_Mejor'].mean()

    # Crear la figura con 3 subgráficos (1 fila, 3 columnas)
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    algoritmos = ['SA', 'ACO']
    
    # Gráfico 1: CV (%)
    axes[0].bar(algoritmos, [cv_sa, cv_aco], color=['#1f77b4', '#ff7f0e'])
    axes[0].set_title('Variabilidad relativa (Estabilidad)')
    axes[0].set_ylabel('Coeficiente de Variación (%)')
    axes[0].grid(axis='y', linestyle='--', alpha=0.7)

    # Gráfico 2: Tiempo de ejecución
    axes[1].bar(algoritmos, [tiempo_sa, tiempo_aco], color=['#1f77b4', '#ff7f0e'])
    axes[1].set_title('Costo Computacional')
    axes[1].set_ylabel('Tiempo promedio por corrida (s)')
    axes[1].grid(axis='y', linestyle='--', alpha=0.7)

    # Gráfico 3: Paso de convergencia
    axes[2].bar(algoritmos, [iter_sa, iter_aco], color=['#1f77b4', '#ff7f0e'])
    axes[2].set_title('Velocidad de Convergencia')
    axes[2].set_ylabel('Iteración / Generación media')
    axes[2].grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    nombre_archivo = 'graficos_barras_validacion_final.png'
    plt.savefig(nombre_archivo, dpi=300)
    plt.close('all')
    print(f"* Gráficos de barras guardados: {nombre_archivo}")

def generar_tabla_comparativa(df_sa, df_aco, campeon_sa, campeon_aco):
    """Genera la tabla final comparando SA vs ACO usando los campeones del Bloque 2."""
    datos_sa = df_sa[df_sa['ID_Config'] == campeon_sa]
    datos_aco = df_aco[df_aco['ID_Config'] == campeon_aco]
    
    tasa_fact_sa = (datos_sa['Factible'] == 'SI').mean() * 100
    costo_prom_sa = datos_sa['Costo_Total'].mean()
    mejor_costo_sa = datos_sa['Costo_Total'].min()
    peor_costo_sa = datos_sa['Costo_Total'].max()
    std_sa = datos_sa['Costo_Total'].std()
    cv_sa = std_sa / costo_prom_sa if costo_prom_sa != 0 else 0
    tiempo_sa = datos_sa['Tiempo_s'].mean()
    iter_sa = datos_sa['Iteracion_Mejor'].mean()
    
    tasa_fact_aco = (datos_aco['Factible'] == 'SI').mean() * 100
    costo_prom_aco = datos_aco['Costo_Total'].mean()
    mejor_costo_aco = datos_aco['Costo_Total'].min()
    peor_costo_aco = datos_aco['Costo_Total'].max()
    std_aco = datos_aco['Costo_Total'].std()
    cv_aco = std_aco / costo_prom_aco if costo_prom_aco != 0 else 0
    tiempo_aco = datos_aco['Tiempo_s'].mean()
    iter_aco = datos_aco['Iteracion_Mejor'].mean()
    
    print(f"\n{'='*95}")
    print(f" TABLA FINAL COMPARATIVA: SA vs ACO (Corridas de Validación)")
    print(f"{'='*95}")
    print(f"{'Métrica':<30} | {'Simulated Annealing':<28} | {'Ant Colony Optimization':<28}")
    print(f"{'-'*30}-+-{'-'*28}-+-{'-'*28}")
    print(f"{'Mejor Configuración':<30} | {campeon_sa:<28} | {campeon_aco:<28}")
    print(f"{'Tasa de Factibilidad':<30} | {tasa_fact_sa:>27.1f}% | {tasa_fact_aco:>27.1f}%")
    print(f"{'Costo Promedio':<30} | {costo_prom_sa:>28.0f} | {costo_prom_aco:>28.0f}")
    print(f"{'Mejor Costo Encontrado':<30} | {mejor_costo_sa:>28.0f} | {mejor_costo_aco:>28.0f}")
    print(f"{'Peor Costo Encontrado':<30} | {peor_costo_sa:>28.0f} | {peor_costo_aco:>28.0f}")
    print(f"{'Desviación Estándar':<30} | {std_sa:>28.2f} | {std_aco:>28.2f}")
    print(f"{'Coeficiente de Variación':<30} | {cv_sa:>28.4f} | {cv_aco:>28.4f}")
    print(f"{'Tiempo Promedio (s)':<30} | {tiempo_sa:>28.2f} | {tiempo_aco:>28.2f}")
    print(f"{'Iteración de Convergencia':<30} | {iter_sa:>28.0f} | {iter_aco:>28.0f}")
    print(f"{'='*95}\n")

def main():
    print("Cargando y unificando archivos CSV...")
    
    df_sa_b1 = pd.read_csv('resultados_SA_experimentos.csv')
    df_sa_b2 = pd.read_csv('resultados_SA_experimentos_bloque2.csv')
    df_sa = pd.concat([df_sa_b1, df_sa_b2], ignore_index=True)
    
    df_aco_b1 = pd.read_csv('resultados_ACO_experimentos.csv')
    df_aco_b2 = pd.read_csv('resultados_ACO_experimentos_bloque2.csv')
    df_aco = pd.concat([df_aco_b1, df_aco_b2], ignore_index=True)
    
    MEJOR_B1_SA = 'B1_SA_02'
    MEJOR_B2_SA = 'B2_SA_09' 
    MEJOR_B1_ACO = 'B1_ACO_07'
    MEJOR_B2_ACO = 'B2_ACO_08' 
    
    print("\nGenerando Diagramas de Caja...")
    generar_boxplots(df_sa, "Simulated_Annealing", "Linea_Base", MEJOR_B1_SA, MEJOR_B2_SA)
    generar_boxplots(df_aco, "Ant_Colony", "Linea_Base", MEJOR_B1_ACO, MEJOR_B2_ACO)
    
    print("\nGenerando Gráficos de Barras (Diapositiva 11)...")
    generar_graficos_barras(df_sa, df_aco, MEJOR_B2_SA, MEJOR_B2_ACO)
    
    print("\nGenerando Tabla Comparativa Final...")
    generar_tabla_comparativa(df_sa, df_aco, MEJOR_B2_SA, MEJOR_B2_ACO)

if __name__ == "__main__":
    main()