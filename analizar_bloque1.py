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

    # 1. EVALUACIÓN Y ESTADÍSTICAS ESPECÍFICAS DE LA LÍNEA BASE
    # Buscamos variaciones comunes del nombre de la línea base ('Linea_Base', 'linea_base', etc.)
    df_linea_base = df[df['ID_Config'].str.lower().isin(['linea_base', 'lineabase', 'base'])]
    
    if not df_linea_base.empty:
        print(f"\n{'='*90}")
        print(f" ESTADÍSTICAS DETALLADAS DE LA LÍNEA BASE - {nombre_algoritmo.upper()}")
        print(f"{'='*90}")
        
        lb_resumen = df_linea_base.groupby('ID_Config').agg(
            Costo_Promedio=('Costo_Total', 'mean'),
            Min_Costo=('Costo_Total', 'min'),
            Max_Costo=('Costo_Total', 'max'),
            Desviacion_Std=('Costo_Total', 'std'),
            Iteracion_Convergencia=('Iteracion_Mejor', 'mean'),
            Tasa_Factibilidad=('Es_Factible', lambda x: x.mean() * 100),
            Tiempo_Promedio=('Tiempo_s', 'mean')
        ).reset_index()
        
        lb_columnas = ['ID_Config', 'Min_Costo', 'Max_Costo', 'Desviacion_Std', 'Iteracion_Convergencia', 'Tasa_Factibilidad', 'Costo_Promedio']
        lb_formato = {
            'Min_Costo': lambda x: f"{x:.0f}",
            'Max_Costo': lambda x: f"{x:.0f}",
            'Desviacion_Std': lambda x: f"{x:.4f}",
            'Iteracion_Convergencia': lambda x: f"{x:.1f}",
            'Tasa_Factibilidad': lambda x: f"{x:.1f}%",
            'Costo_Promedio': lambda x: f"{x:.0f}"
        }
        print(lb_resumen[lb_columnas].to_string(index=False, formatters=lb_formato))
        print(f"{'='*90}\n")

    # 2. EVALUACIÓN Y RANKING EXCLUSIVO DEL BLOQUE 1 (Excluyendo la línea base)
    df_bloque1 = df[~df['ID_Config'].str.lower().isin(['linea_base', 'lineabase', 'base'])]

    if df_bloque1.empty:
        print(f"No se encontraron datos del Bloque 1 para {nombre_algoritmo}.")
        return

    resumen_b1 = df_bloque1.groupby('ID_Config').agg(
        Costo_Promedio=('Costo_Total', 'mean'),
        Mejor_Costo=('Costo_Total', 'min'),
        Peor_Costo=('Costo_Total', 'max'),
        Desviacion_Std=('Costo_Total', 'std'),
        Tasa_Factibilidad=('Es_Factible', lambda x: x.mean() * 100),
        Tiempo_Promedio=('Tiempo_s', 'mean'),
        Iteracion_Promedio=('Iteracion_Mejor', 'mean')
    ).reset_index()

    # Calcular el Coeficiente de Variación (CV) = Desviación Estándar / Media
    resumen_b1['Coef_Variacion'] = resumen_b1['Desviacion_Std'] / resumen_b1['Costo_Promedio']

    # Criterio de selección para el ranking del Bloque 1
    resumen_b1 = resumen_b1.sort_values(
        by=['Tasa_Factibilidad', 'Costo_Promedio', 'Coef_Variacion'], 
        ascending=[False, True, True]
    )

    print(f"{'='*90}")
    print(f" RANKING DE CONFIGURACIONES - {nombre_algoritmo.upper()} (Únicamente Bloque 1)")
    print(f"{'='*90}")
    
    columnas_mostrar = ['ID_Config', 'Tasa_Factibilidad', 'Costo_Promedio', 'Mejor_Costo', 'Coef_Variacion', 'Tiempo_Promedio']
    formato = {
        'Tasa_Factibilidad': lambda x: f"{x:.1f}%", 
        'Costo_Promedio': lambda x: f"{x:.0f}", 
        'Coef_Variacion': lambda x: f"{x:.4f}", 
        'Tiempo_Promedio': lambda x: f"{x:.2f}s"
    }
    
    print(resumen_b1[columnas_mostrar].to_string(index=False, formatters=formato))
    print(f"{'='*90}\n")

if __name__ == "__main__":
    analizar_y_rankear('resultados_SA_experimentos.csv', 'Simulated Annealing')
    analizar_y_rankear('resultados_ACO_experimentos.csv', 'Ant Colony Optimization')