import pandas as pd
import numpy as np

def analizar_y_rankear(archivo_csv, nombre_algoritmo):
    try:
        df = pd.read_csv(archivo_csv)
    except FileNotFoundError:
        print(f"No se encontró el archivo: {archivo_csv}")
        return

    # Convertir la columna 'Factible' a valores numéricos para sacar el porcentaje
    df['Es_Factible'] = df['Factible'].apply(lambda x: 1 if x == 'SI' else 0)

    # Agrupar por ID_Config y calcular exactamente lo que pide la guía
    resumen = df.groupby('ID_Config').agg(
        Costo_Promedio=('Costo_Total', 'mean'),
        Mejor_Costo=('Costo_Total', 'min'),
        Peor_Costo=('Costo_Total', 'max'),
        Desviacion_Std=('Costo_Total', 'std'),
        Tasa_Factibilidad=('Es_Factible', lambda x: x.mean() * 100),
        Tiempo_Promedio=('Tiempo_s', 'mean'),
        Iteracion_Promedio=('Iteracion_Mejor', 'mean')
    ).reset_index()

    # Calcular el Coeficiente de Variación (CV) = Desviación Estándar / Media
    resumen['Coef_Variacion'] = resumen['Desviacion_Std'] / resumen['Costo_Promedio']

    # CRITERIO DE SELECCIÓN DE CAMPEONES:
    # 1. Mayor tasa de factibilidad (Queremos horarios válidos)
    # 2. Menor costo promedio (Desempate por calidad de la solución)
    # 3. Menor coeficiente de variación (Desempate por estabilidad)
    resumen = resumen.sort_values(
        by=['Tasa_Factibilidad', 'Costo_Promedio', 'Coef_Variacion'], 
        ascending=[False, True, True]
    )

    # Imprimir la tabla de resultados de forma legible
    print(f"\n{'='*90}")
    print(f" RANKING DE CONFIGURACIONES - {nombre_algoritmo.upper()} (Bloque 1)")
    print(f"{'='*90}")
    
    # Formatear columnas para la visualización en consola
    columnas_mostrar = ['ID_Config', 'Tasa_Factibilidad', 'Costo_Promedio', 'Mejor_Costo', 'Coef_Variacion', 'Tiempo_Promedio']
    formato = {
        'Tasa_Factibilidad': lambda x: f"{x:.1f}%", 
        'Costo_Promedio': lambda x: f"{x:.0f}", 
        'Coef_Variacion': lambda x: f"{x:.4f}", 
        'Tiempo_Promedio': lambda x: f"{x:.2f}s"
    }
    
    print(resumen[columnas_mostrar].to_string(index=False, formatters=formato))
    print(f"{'='*90}\n")

if __name__ == "__main__":
    analizar_y_rankear('resultados_SA_experimentos.csv', 'Simulated Annealing')
    analizar_y_rankear('resultados_ACO_experimentos.csv', 'Ant Colony Optimization')