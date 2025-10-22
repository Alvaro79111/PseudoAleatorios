# Proyecto Pseudoaleatorios

Generador y analizador de números pseudoaleatorios en Python. Incluye algoritmos clásicos, interfaz gráfica y utilidades para simulación y análisis estadístico.

---

## Características principales
- Generadores: Cuadrados Medios, Productos Medios, Multiplicador Constante
- Interfaz gráfica con Tkinter
- Análisis estadístico y visualización
- Modular y extensible

---

## Requisitos

- Python 3.7 o superior (recomendado 3.12)
- Las siguientes librerías:
  - numpy
  - scipy
  - matplotlib
  - pandas
  - openpyxl
  - pillow
  - tkinter (incluida en la mayoría de instalaciones de Python)

---

## Instalación

1. Clona este repositorio o descarga los archivos.

2. Navega a la carpeta del proyecto en tu terminal:

```powershell
cd ruta\al\proyecto
```

3. Crea y activa un entorno virtual (recomendado):

**En Windows (PowerShell):**
```powershell

py -m venv .venv
.\.venv\Scripts\Activate.ps1
```
Si tienes errores al activar, ejecuta en modo administrador:
```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```
Responde S para permitir la ejecución.

**En Linux/MacOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

4. Instala las dependencias:

```bash
pip install -r requirements.txt
```

Si falta alguna librería, instálala manualmente:
```bash
pip install matplotlib pandas openpyxl pillow
```

---

## Uso

Para ejecutar el script principal, asegúrate de estar en el entorno virtual y en la carpeta del proyecto, luego corre:

```powershell
C:/Users/Alvaro/Desktop/Proyectos_Sumulacion/PseudoAleatorios/.venv/Scripts/python.exe psedoaleatorios.py
```

--- 

## Estructura del proyecto

```
PseudoAleatorios/
├── pseudoaleatorios/           # Módulos principales
│   ├── generadores/           # Algoritmos de generación
│   ├── interfaces/            # Interfaces y distribuciones
│   ├── gui.py                 # Interfaz gráfica
│   ├── generators.py          # Lógica de generadores
│   └── tests.py               # Pruebas
├── psedoaleatorios.py         # Script principal
├── requirements.txt           # Dependencias
└── README.md                  # Documentación
```

---

## Notas

- El script usa tkinter para la interfaz gráfica.
- Si usas otro entorno virtual, ajusta la ruta del ejecutable.
- Para pruebas, ejecuta:
```powershell
C:/Users/Alvaro/Desktop/Proyectos_Sumulacion/PseudoAleatorios/.venv/Scripts/python.exe pseudoaleatorios/tests.py
```

---

## Autor
Alvaro

---

## Licencia
MIT