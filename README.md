# 🚑 Gemelo Digital para la Gestión de Emergencias (Madrid Centro)

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![SUMO](https://img.shields.io/badge/Simulador-Eclipse%20SUMO-orange?style=flat-square)](https://eclipse.dev/sumo/)

Este proyecto implementa un **Gemelo Digital** utilizando **SUMO** (Simulation of Urban MObility) y datos de **Open Data Madrid** para optimizar el tránsito de vehículos de emergencia en el Distrito Centro. El sistema utiliza la interfaz **TraCI** para establecer una comunicación bidireccional entre la lógica de control en Python y el entorno virtual.

---

## 🛠️ 1. Requisitos e Instalación

Para que el sistema funcione correctamente, siga estos pasos en orden:

### **Paso A: Software Base**
* **Python 3.10+**: Lenguaje vertebrador encargado de la lógica de prioridad.
* **Eclipse SUMO**: Motor de simulación microscópica indispensable.

### **Paso B: Configuración de Variable de Entorno (IMPORTANTE)** ⚠️
El script de Python requiere saber dónde está instalado SUMO. Sin este paso, el sistema no podrá localizar las herramientas binarias del simulador.
* **Windows**: Crear una variable de entorno de sistema llamada `SUMO_HOME` que apunte a la carpeta de instalación (Ejemplo: `C:\Program Files (x86)\Eclipse\Sumo`).
* **Linux/macOS**: Añadir al final de su archivo `.bashrc` o `.zshrc` la línea: `export SUMO_HOME=/usr/share/sumo`.

### **Paso C: Descarga e Instalación de Dependencias**
Primero, descargue el proyecto desde GitHub. Después, abra una terminal dentro de la carpeta del proyecto e instale las librerías necesarias (`traci`, `pandas`, `requests`):

```bash
# 1. Clonar el repositorio
git clone https://github.com/paattrdzz/Trabajo-Fin-Grado.git

# 2. Entrar en la carpeta
cd Trabajo-Fin-Grado

# 3. Instalar librerías
pip install -r requirements.txt

# 4. Ejecutar la simulación
python TFG.py


Autora: Patricia Rodríguez Casado

Escuela: Escuela Técnica Superior de Ingenieros de Telecomunicación (ETSIT-UPM)

Tutor: Mario Sanz Rodrigo

Año: 2026
