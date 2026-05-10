# 🚑 Gemelo Digital para la Gestión de Emergencias (Madrid Centro)

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![SUMO](https://img.shields.io/badge/Simulador-Eclipse%20SUMO-orange?style=flat-square)](https://eclipse.dev/sumo/)
[![OpenData](https://img.shields.io/badge/Data-Madrid%20Open%20Data-blue?style=flat-square)](https://datos.madrid.es/)

[cite_start]Este proyecto implementa un **Gemelo Digital** utilizando **SUMO** (Simulation of Urban MObility) [cite: 63] [cite_start]y datos de **Open Data Madrid** [cite: 58] para optimizar el tránsito de vehículos de emergencia en el Distrito Centro. [cite_start]El sistema utiliza la interfaz **TraCI** para establecer una comunicación bidireccional entre la lógica de control en Python y el entorno virtual[cite: 326, 327].

---

## 🛠️ 1. Requisitos e Instalación

Para que el sistema funcione correctamente, siga estos pasos en orden:

### **Paso A: Software Base**
* [cite_start]**Python 3.10+**: Lenguaje vertebrador encargado de la lógica de prioridad[cite: 332].
* [cite_start]**Eclipse SUMO**: Motor de simulación microscópica indispensable[cite: 227].

### **Paso B: Configuración de Variable de Entorno (CRÍTICO)** ⚠️
El script de Python requiere saber dónde está instalado SUMO. Sin este paso, el sistema no podrá localizar las herramientas binarias del simulador.
* **Windows**: Crear una variable de entorno de sistema llamada `SUMO_HOME` que apunte a la carpeta de instalación (Ejemplo: `C:\Program Files (x86)\Eclipse\Sumo`).
* **Linux/macOS**: Añadir al final de su archivo `.bashrc` o `.zshrc` la línea: `export SUMO_HOME=/usr/share/sumo`.

### **Paso C: Descarga e Instalación de Dependencias**
Primero, descargue el proyecto desde GitHub. Después, abra una terminal dentro de la carpeta del proyecto e instale las librerías necesarias (`traci`, `pandas`, `requests`):

```bash
# 1. Clonar el repositorio
git clone [https://github.com/paattrdzz/Trabajo-Fin-Grado.git](https://github.com/paattrdzz/Trabajo-Fin-Grado.git)

# 2. Entrar en la carpeta
cd Trabajo-Fin-Grado

# 3. Instalar librerías
pip install -r requirements.txt

Ejecución de la simulación
Para iniciar la simulación con interfaz gráfica (sumo-gui), ejecute dentro de la carpeta clonada:
    python TFG.py






