import pandas as pd
import matplotlib.pyplot as plt
import os

def generar_boxplots(df, algoritmo, id_base, id_b1, id_b2):
    """Genera y guarda el diagrama de caja comparativo para un algoritmo."""
    # Filtrar solo las configuraciones que nos interesan
    datos_filtrados = df[df['ID_Config'].isin([id_base, id_b1, id_b2])]
    
    # Ordenar categóricamente para que el gráfico salga en el orden correcto
    datos_filtrados['ID_Config'] = pd.Categorical(
        datos_filtrados['ID_Config'], 
        categories=[id_base, id_b1, id_b2], 
        ordered=True
    )
    
    plt.figure(figsize=(10, 6))
    datos_filtrados.boxplot(column='Costo_Total', by='ID_Config', grid=True, patch_artist=True)
    
    plt.title(f'Comparación de Costos - {algoritmo}')
    plt.suptitle('')  # Eliminar el título automático de pandas
    plt.xlabel('Configuración')
    plt.ylabel('Costo de la Función Objetivo')
    
    nombre_archivo = f'boxplot_comparativo_{algoritmo}.png'
    plt.savefig(nombre_archivo, dpi=300)
    plt.close('all')
    print(f"* Diagrama de caja guardado: {nombre_archivo}")

def generar_tabla_comparativa(df_sa, df_aco, campeon_sa, campeon_aco):
    """Genera la tabla final comparando SA vs ACO usando los campeones del Bloque 2."""
    
    # Extraer los datos solo de los campeones
    datos_sa = df_sa[df_sa['ID_Config'] == campeon_sa]
    datos_aco = df_aco[df_aco['ID_Config'] == campeon_aco]
    
    # Calcular métricas para SA
    tasa_fact_sa = (datos_sa['Factible'] == 'SI').mean() * 100
    costo_prom_sa = datos_sa['Costo_Total'].mean()
    mejor_costo_sa = datos_sa['Costo_Total'].min()
    cv_sa = datos_sa['Costo_Total'].std() / costo_prom_sa
    tiempo_sa = datos_sa['Tiempo_s'].mean()
    iter_sa = datos_sa['Iteracion_Mejor'].mean()
    
    # Calcular métricas para ACO
    tasa_fact_aco = (datos_aco['Factible'] == 'SI').mean() * 100
    costo_prom_aco = datos_aco['Costo_Total'].mean()
    mejor_costo_aco = datos_aco['Costo_Total'].min()
    cv_aco = datos_aco['Costo_Total'].std() / costo_prom_aco
    tiempo_aco = datos_aco['Tiempo_s'].mean()
    iter_aco = datos_aco['Iteracion_Mejor'].mean()
    
    print(f"\n{'='*90}")
    print(f" TABLA FINAL COMPARATIVA: SA vs ACO (Corridas de Validación)")
    print(f"{'='*90}")
    print(f"{'Métrica':<30} | {'Simulated Annealing':<25} | {'Ant Colony Optimization':<25}")
    print(f"{'-'*30}-+-{'-'*25}-+-{'-'*25}")
    print(f"{'Mejor Configuración':<30} | {campeon_sa:<25} | {campeon_aco:<25}")
    print(f"{'Tasa de Factibilidad':<30} | {tasa_fact_sa:>24.1f}% | {tasa_fact_aco:>24.1f}%")
    print(f"{'Costo Promedio':<30} | {costo_prom_sa:>25.0f} | {costo_prom_aco:>25.0f}")
    print(f"{'Mejor Costo Encontrado':<30} | {mejor_costo_sa:>25.0f} | {mejor_costo_aco:>25.0f}")
    print(f"{'Coeficiente de Variación':<30} | {cv_sa:>25.4f} | {cv_aco:>25.4f}")
    print(f"{'Tiempo Promedio (s)':<30} | {tiempo_sa:>25.2f} | {tiempo_aco:>25.2f}")
    print(f"{'Iteración de Convergencia':<30} | {iter_sa:>25.0f} | {iter_aco:>25.0f}")
    print(f"{'='*90}\n")

def main():
    print("Cargando y unificando archivos CSV...")
    
    # Cargar y unir los archivos de SA
    df_sa_b1 = pd.read_csv('resultados_SA_experimentos.csv')
    df_sa_b2 = pd.read_csv('resultados_SA_experimentos_bloque2.csv')
    df_sa = pd.concat([df_sa_b1, df_sa_b2], ignore_index=True)
    
    # Cargar y unir los archivos de ACO
    df_aco_b1 = pd.read_csv('resultados_ACO_experimentos.csv')
    df_aco_b2 = pd.read_csv('resultados_ACO_experimentos_bloque2.csv')
    df_aco = pd.concat([df_aco_b1, df_aco_b2], ignore_index=True)
    
    # --- CAMBIA ESTOS VALORES POR TUS GANADORES REALES ---
    MEJOR_B1_SA = 'B1_SA_02'
    MEJOR_B2_SA = 'B2_SA_09' # Actualizar cuando termine el script de SA
    
    MEJOR_B1_ACO = 'B1_ACO_07'
    MEJOR_B2_ACO = 'B2_ACO_08' # Actualizar con el ganador de tu bloque 2
    
    print("\nGenerando Diagramas de Caja...")
    generar_boxplots(df_sa, "Simulated_Annealing", "Linea_Base", MEJOR_B1_SA, MEJOR_B2_SA)
    generar_boxplots(df_aco, "Ant_Colony", "Linea_Base", MEJOR_B1_ACO, MEJOR_B2_ACO)
    
    print("\nGenerando Tabla Comparativa Final...")
    generar_tabla_comparativa(df_sa, df_aco, MEJOR_B2_SA, MEJOR_B2_ACO)

if __name__ == "__main__":
    main()