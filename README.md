# Métodos de Búsqueda IA: Programación de Exámenes Universitarios

Proyecto desarrollado en Python para la implementación y experimentación de métodos de búsqueda metaheurísticos (Enfriamiento Simulado - SA y Optimización por Colonias de Hormigas - ACO) aplicados a un problema de optimización combinatoria.

## Contexto del Proyecto

El objetivo de este proyecto es resolver el problema de **Programación de Exámenes Universitarios**. El sistema debe asignar a cada examen una franja horaria y un aula, minimizando los conflictos y maximizando la eficiencia de los recursos. 

El problema se evalúa mediante una función objetivo que penaliza:
1. **Restricciones Duras ($H$):** Cruces de horarios para estudiantes, superación de aforos de aulas, o asignaciones en horarios no permitidos (deben ser 0 para que la solución sea factible).
2. **Restricciones Blandas:** Estudiantes con más de un examen el mismo día ($C_{dia}$) y asientos vacíos en las aulas utilizadas ($P_{libres}$).

## Modelos de Datos (Clases)

El proyecto utiliza un enfoque orientado a objetos para mapear los datos del archivo Excel a entidades manejables en Python (definidas en `modelos.py`):

*   **`Examen`**: Representa una prueba a programar. Contiene su identificador, cantidad de estudiantes inscritos, duración en minutos y una lista de las franjas (horarios) en las que es permitido programarlo.
*   **`Franja`**: Representa un bloque de tiempo. Contiene su identificador único, el día de la semana y el horario específico.
*   **`Aula`**: Representa el espacio físico. Contiene su identificador, la capacidad máxima de estudiantes y una lista de las franjas en las que está disponible para ser usada.
*   **`Matricula`**: Representa la relación entre un estudiante y un examen, fundamental para calcular los conflictos y cruces de horarios.

---

## Requisitos

- Python 3.12 o superior
- Git
- pip

## Estructura del proyecto

```text
METODOS DE BUSQUEDA IA/
├── data/               # Archivos de datos de Excel (instancias) utilizados por el programa
├── lector_excel.py     # Lectura con pandas y mapeo de los datos hacia los modelos
├── main.py             # Punto de entrada del programa y orquestador
├── modelos.py          # Definición de las clases (Examen, Franja, Aula, Matricula)
├── requirements.txt    # Dependencias de Python
├── .gitignore
└── README.md
```

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/AlfonsoMSDL/Metodos-de-busqueda-IA.git
```

Entrar al proyecto:

```bash
cd "Metodos de busqueda IA"
```

### 2. Crear el entorno virtual

Se recomienda utilizar un entorno virtual para evitar conflictos con las dependencias de Python instaladas en el sistema.

```bash
python3 -m venv .venv
```

### 3. Activar el entorno virtual

En Linux:

```bash
source .venv/bin/activate
```

En Windows:

```bash
.venv\Scripts\activate
```

Cuando el entorno esté activo, aparecerá `(.venv)` al inicio de la terminal.

### 4. Instalar las dependencias

Con el entorno virtual activado:

```bash
python -m pip install -r requirements.txt
```

Las principales dependencias utilizadas son:

- `pandas`
- `openpyxl`

## Ejecución

Con el entorno virtual activado, ejecutar:

```bash
python main.py
```

También se puede ejecutar directamente utilizando el Python del entorno virtual:

```bash
./.venv/bin/python main.py
```

## Datos

Los archivos utilizados por el programa deben encontrarse dentro de la carpeta:

```text
data/
```

El programa utiliza archivos de Excel como fuente de datos (ej. `instancia_examenes_tema02.xlsx`).
Asegúrate de que los archivos necesarios se encuentren en la ubicación esperada antes de ejecutar el programa.

## Desactivar el entorno virtual

Cuando termines de trabajar en el proyecto:

```bash
deactivate
```

## Desarrollo

Cada vez que vuelvas a trabajar en el proyecto:

```bash
cd "Metodos de busqueda IA"
source .venv/bin/activate
python main.py
```

## Dependencias

Si se instala una nueva librería durante el desarrollo, actualizar el archivo `requirements.txt` con:

```bash
pip freeze > requirements.txt
```

Esto permite que otros desarrolladores puedan instalar las mismas dependencias utilizando:

```bash
pip install -r requirements.txt
```

## Control de versiones

El entorno virtual `.venv/`, los archivos `__pycache__/` y otros archivos temporales no deben subirse al repositorio. Estos archivos están excluidos mediante `.gitignore`.