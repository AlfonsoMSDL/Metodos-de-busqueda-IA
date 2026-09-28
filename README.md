# Optimización de Horarios de Exámenes Universitarios (SA vs ACO)

Este proyecto aplica técnicas de Inteligencia Artificial para automatizar y optimizar la asignación de franjas horarias y aulas para exámenes universitarios. Se realiza una comparación exhaustiva entre dos algoritmos metaheurísticos: **Simulated Annealing (SA)** y **Ant Colony Optimization (ACO)**.

## 📌 El Problema Logístico

Cada fin de semestre, las universidades se enfrentan al reto de programar cientos de exámenes. Hacerlo manualmente o sin optimización genera ineficiencias y problemas para los estudiantes. Este proyecto modela este desafío a través de una **Función Objetivo** que evalúa dos tipos de restricciones:

* **Restricciones Duras (Inviolables):**
  1. Ningún estudiante puede tener dos exámenes a la misma hora (Cruces).
  2. La cantidad de estudiantes no puede superar la capacidad del aula asignada (Aforo).
  *Nota: Si se viola alguna de estas restricciones, el horario es inválido (Factibilidad = 0).*

* **Restricciones Blandas (Calidad del Horario):**
  1. Minimizar la cantidad de estudiantes con múltiples exámenes el mismo día.
  2. Minimizar el desperdicio de espacio físico (sillas vacías).

## 🚀 La Solución

Para resolver este problema de optimización combinatoria, implementamos dos enfoques:

1. **Simulated Annealing (SA):** Un algoritmo de búsqueda local inspirado en el enfriamiento de metales, que modifica un horario inicial iterativamente, aceptando peores soluciones temporalmente para escapar de óptimos locales.
2. **Ant Colony Optimization (ACO):** Un algoritmo constructivo inspirado en el comportamiento de las hormigas, donde múltiples agentes construyen horarios paso a paso guiados por una memoria colectiva (feromonas) y heurísticas locales.

## 📂 Estructura del Proyecto

* `data/`: Carpeta que contiene los archivos de entrada (e.g., base de datos en Excel).
* `lector_excel.py`: Módulo encargado de extraer y procesar los datos de entrada.
* `modelos.py`: Define las estructuras de datos (clases de Estudiantes, Exámenes, Aulas).
* `funcion_objetivo.py`: Lógica matemática para calcular los costos y penalizaciones.
* `simulated_annealing.py`: Implementación del algoritmo SA.
* `ant_colony_opt.py`: Implementación del algoritmo ACO.
* `testSA.py` / `testACO.py`: Scripts principales para ejecutar los experimentos masivos.
* `analizar_bloques.py`: Script para procesar los resultados (CSV) y rankear las configuraciones.
* `comparacion_final.py`: Script que toma a los campeones absolutos para generar los gráficos comparativos.
* `requirements.txt`: Dependencias necesarias para ejecutar el proyecto.

## 📋 Configuraciones Iniciales (Copiar y Pegar)

Para iniciar los experimentos, inserta estos diccionarios en tus archivos `testSA.py` y `testACO.py`. 
*Nota: Solo se proveen la Línea Base y el Bloque 1, ya que el Bloque 2 debe diseñarse a partir de los resultados obtenidos aquí.*

### Para `testSA.py`
```python
# --- LÍNEA BASE SA ---
config_base_sa = [
    {"id": "Linea_Base_SA", "T_inicial": 10000, "alfa": 0.95, "T_final": 1.0, "iteraciones": 100}
]

# --- BLOQUE 1: Exploración SA ---
configuraciones_b1_sa = [
    {"id": "B1_SA_01", "T_inicial": 100000, "alfa": 0.90, "T_final": 0.1, "iteraciones": 200},
    {"id": "B1_SA_02", "T_inicial": 5000000, "alfa": 0.995, "T_final": 0.1, "iteraciones": 600},
    {"id": "B1_SA_05", "T_inicial": 2500000, "alfa": 0.98, "T_final": 0.1, "iteraciones": 400},
    {"id": "B1_SA_09", "T_inicial": 1000000, "alfa": 0.99, "T_final": 0.1, "iteraciones": 300}
    # Añade más configuraciones explorando rangos amplios de temperatura y enfriamiento.
]
```

### Para `testACO.py`
```python
# --- LÍNEA BASE ACO ---
config_base_aco = [
    {"id": "Linea_Base_ACO", "num_hormigas": 20, "num_generaciones": 50, "alpha": 1.0, "beta": 1.0, "rho": 0.5, "Q": 100.0}
]

# --- BLOQUE 1: Exploración ACO ---
configuraciones_b1_aco = [
    {"id": "B1_ACO_02", "num_hormigas": 40, "num_generaciones": 150, "alpha": 0.8, "beta": 1.2, "rho": 0.2, "Q": 5000.0},
    {"id": "B1_ACO_03", "num_hormigas": 30, "num_generaciones": 100, "alpha": 1.0, "beta": 2.0, "rho": 0.1, "Q": 1000.0},
    {"id": "B1_ACO_07", "num_hormigas": 50, "num_generaciones": 200, "alpha": 1.2, "beta": 1.5, "rho": 0.01, "Q": 50000.0}
    # Añade más configuraciones variando la evaporación (rho) y el peso heurístico.
]
```

## ⚙️ Guía de Ejecución Paso a Paso (Metodología)

El diseño experimental requiere un flujo estricto donde los resultados de una fase dictan los parámetros de la siguiente. Sigue estos pasos sin saltarte el orden:

### Paso 0: Preparación
Instala las dependencias necesarias ejecutando:
`pip install -r requirements.txt`

### Paso 1: Ejecución del Bloque 1 (Exploración)
En esta fase, los algoritmos exploran un espacio de búsqueda muy amplio. Asegúrate de tener copiadas las configuraciones del Bloque 1 en tus scripts y ejecútalos (por defecto harán 30 corridas por semilla).
`python testSA.py`
`python testACO.py`

### Paso 2: Análisis del Bloque 1 (Identificando al Ganador)
Ejecuta el script de análisis para que el sistema lea los CSV generados y rankee los resultados basándose primero en la **Factibilidad** y luego en el **Costo Medio**.
`python analizar_bloques.py`
*Toma nota mental o escrita de la configuración que quedó en 1° lugar para SA y para ACO.*

### Paso 3: Diseño del Bloque 2 (Ajuste Fino - ¡CRÍTICO!)
**No uses valores aleatorios aquí.** Abre tus scripts `testSA.py` y `testACO.py` y crea las configuraciones para el Bloque 2 (`configuraciones_b2_...`). 
La regla es: **Toma los hiperparámetros del ganador del Bloque 1 y crea variaciones minúsculas alrededor de él.**
* *Ejemplo SA:* Si el ganador del Bloque 1 tenía `alfa: 0.995`, en tu Bloque 2 debes probar variaciones ajustadas como `0.993, 0.994, 0.996`.
* *Ejemplo ACO:* Si el ganador del Bloque 1 tenía `num_hormigas: 50`, prueba en el Bloque 2 con `48, 52, 55`.

### Paso 4: Ejecución y Análisis del Bloque 2
Corre nuevamente los experimentos con tus nuevas configuraciones refinadas y vuelve a analizarlas para encontrar al Campeón Absoluto de cada método.
`python testSA.py`
`python testACO.py`
`python analizar_bloques.py`

### Paso 5: Comparación Final 
Ahora que tienes al mejor representante posible de SA y de ACO, abre `comparacion_final.py`, ingresa los nombres de las configuraciones campeonas (ej. `B2_SA_09` y `B2_ACO_08`) y ejecuta el script.
`python comparacion_final.py`
Esto generará los gráficos comparativos (boxplot, diagramas de barras de tiempo y estabilidad) demostrando el rendimiento final de frente a frente.

## 📊 Interpretación de los Resultados

Al evaluar las salidas en consola o en las diapositivas, ten en cuenta estos 4 pilares:
1. **Tasa de Factibilidad (%):** Es la métrica reina. Mide cuántas veces el algoritmo logró un horario utilizable (cero cruces).
2. **Costo Promedio:** Criterio de desempate. Menor costo indica una mejor calidad de vida para los estudiantes (menos exámenes el mismo día).
3. **Coeficiente de Variación (CV):** Mide la estabilidad y consistencia. Un CV cercano a 0 indica fiabilidad total.
4. **Tiempo Promedio (s):** El costo computacional. Permite evaluar si un algoritmo es escalable o si sufre un "trade-off" (sacrificar calidad por velocidad).