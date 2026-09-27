# Métodos de Búsqueda IA: Programación de Exámenes Universitarios

Proyecto desarrollado en Python para la implementación y experimentación de métodos de búsqueda metaheurísticos (Enfriamiento Simulado - SA y Optimización por Colonias de Hormigas - ACO) aplicados a un problema de optimización combinatoria.

## Contexto del Proyecto

El objetivo de este proyecto es resolver el problema de **Programación de Exámenes Universitarios**. El sistema debe asignar a cada examen una franja horaria y un aula, minimizando los conflictos y maximizando la eficiencia de los recursos. 

El problema se evalúa mediante una función objetivo que penaliza:
1. **Restricciones Duras ($H$):** Cruces de horarios para estudiantes, superación de aforos de aulas, o asignaciones en horarios no permitidos (deben ser 0 para que la solución sea factible).
2. **Restricciones Blandas:** Estudiantes con más de un examen el mismo día ($C_{dia}$) y asientos vacíos en las aulas utilizadas ($P_{libres}$).

---

## Arquitectura y Componentes Clave

El proyecto está modularizado en tres capas principales:

### 1. Modelos de Datos (`modelos.py` y `lector_excel.py`)
Mapeo orientado a objetos de los datos de entrada:
*   **`Examen`**: Identificador, cantidad de estudiantes, duración y franjas permitidas.
*   **`Franja`**: Identificador único, día de la semana y horario.
*   **`Aula`**: Identificador, capacidad máxima y franjas disponibles.
*   **`Matricula`**: Relación estudiante-examen para calcular conflictos.

### 2. Función Objetivo (`funcion_objetivo.py`)
La clase `EvaluadorFO` se encarga de calcular el costo estandarizado de cualquier horario generado, validando la matriz de conflictos y penalizando las violaciones duras y blandas según la fórmula: 
$Costo = 100000 \cdot H + 100 \cdot C_{dia} + P_{libres}$

### 3. Algoritmos y Experimentación
*   **`simulated_annealing.py`**: Implementación del algoritmo de Enfriamiento Simulado.
*   **`ant_colony_opt.py`**: Implementación de Optimización por Colonia de Hormigas (ACO).
*   **Scripts de Prueba (`testSA.py`, `testACO.py`)**: Motores de ejecución automatizada que corren bloques experimentales de 30 corridas, exportando resultados a archivos `.csv` y generando gráficas de convergencia.
*   **`analizar_bloque1.py`**: Script de procesamiento de datos con Pandas para clasificar las configuraciones campeonas basándose en factibilidad, costo y coeficiente de variación.

---

## Requisitos

- Python 3.12 o superior
- Git
- pip

## Estructura del proyecto

METODOS DE BUSQUEDA IA/
├── data/                           # Archivos de datos de Excel (instancias)
├── .gitignore                      # Exclusión de entornos virtuales y resultados
├── README.md                       # Documentación del proyecto
├── analizar_bloque1.py             # Script de análisis de resultados en consola
├── ant_colony_opt.py               # Lógica del algoritmo ACO
├── funcion_objetivo.py             # Clase EvaluadorFO para cálculo de costos
├── lector_excel.py                 # Lectura con pandas y mapeo de datos
├── modelos.py                      # Definición de las clases de datos
├── requirements.txt                # Dependencias de Python
├── simulated_annealing.py          # Lógica del algoritmo SA
├── testACO.py                      # Script de experimentación para ACO
└── testSA.py                       # Script de experimentación para SA

*(Nota: Los archivos `.csv` de resultados y las gráficas `.png` se generan automáticamente durante la ejecución y son ignorados por Git para mantener limpio el repositorio).*

---

## Instalación

### 1. Clonar el repositorio

git clone https://github.com/AlfonsoMSDL/Metodos-de-busqueda-IA.git
cd "Metodos de busqueda IA"

### 2. Crear y activar el entorno virtual

Se recomienda utilizar un entorno virtual para evitar conflictos con las dependencias del sistema.

# Crear entorno
python3 -m venv .venv

# Activar en Linux/macOS
source .venv/bin/activate

# Activar en Windows
.venv\Scripts\activate

*(Cuando el entorno esté activo, aparecerá `(.venv)` al inicio de la terminal).*

### 3. Instalar las dependencias

python -m pip install -r requirements.txt

Principales librerías utilizadas: `pandas`, `openpyxl`, `numpy`, `matplotlib`.

---

## Ejecución de Experimentos

El proyecto está diseñado para correr experimentos por bloques (Línea Base, Bloque 1, Bloque 2). Para ejecutar las pruebas automatizadas de 30 corridas, asegúrate de tener el entorno virtual activado y los archivos `.xlsx` dentro de la carpeta `data/`.

**Para correr Enfriamiento Simulado:**
python testSA.py

**Para correr Optimización por Colonia de Hormigas:**
python testACO.py

**Para analizar los resultados y rankear las mejores configuraciones:**
python analizar_bloque1.py

## Desarrollo y Control de Versiones

Cada vez que vuelvas a trabajar en el proyecto:
cd "Metodos de busqueda IA"
source .venv/bin/activate

Al terminar de trabajar, desactiva el entorno:
deactivate

Si instalas nuevas dependencias durante el desarrollo, actualiza el archivo de requerimientos:
pip freeze > requirements.txt