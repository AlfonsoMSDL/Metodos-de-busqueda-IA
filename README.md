# Métodos de Búsqueda IA

Proyecto desarrollado en Python para la implementación y experimentación de métodos de búsqueda aplicados a problemas de Inteligencia Artificial.

## Requisitos

- Python 3.12 o superior
- Git
- pip

## Estructura del proyecto

```text
METODOS DE BUSQUEDA IA/
├── data/               # Archivos de datos utilizados por el programa
├── lector_excel.py     # Lectura y procesamiento de los datos de Excel
├── main.py             # Punto de entrada del programa
├── modelos.py          # Modelos y estructuras utilizadas por el programa
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

El programa utiliza archivos de Excel como fuente de datos.

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
