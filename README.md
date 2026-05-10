Este repositorio contiene el entorno de simulación para el Trabajo Fin de Grado enfocado en la diseño y desarrollo de un gemelo digital con priorización de vehículos de emergencia basado en OpenData. El sistema utiliza la interfaz TraCI para establecer una comunicación bidireccional entre la lógica de control en Python y el motor de micro-simulación SUMO.

REQUISITOS DE INSTALACIÓN

Antes de iniciar el despliegue, asegúrese de contar con el software base necesario:

Python 3.10+: Lenguaje vertebrador del proyecto encargado de la lógica de prioridad.  
Eclipse SUMO (v1.18.0 o superior): Suite de simulación de tráfico microscópico indispensable para la ejecución del modelo virtual.

Configuración del Entorno

Para que la librería TraCI pueda orquestar el simulador, es obligatorio definir la variable de entorno SUMO_HOME. Esta variable permite que los scripts de Python localicen las herramientas binarias de SUMO en el sistema operativo.

En Windows
Busque "Editar las variables de entorno del sistema" en el menú inicio.
En "Variables de entorno", cree una nueva Variable de sistema llamada SUMO_HOME.
Asigne como valor la ruta de instalación de SUMO (por defecto: C:\Program Files (x86)\Eclipse\Sumo).

En Linux / macOS
Añada la siguiente línea al final de su archivo de configuración de shell (.bashrc o .zshrc):
        export SUMO_HOME=/usr/share/sumo

Descarga del repositorio
    git clone https://github.com/paattrdzz/Trabajo-Fin-Grado

Instalación de Dependencias
El proyecto requiere librerías específicas para la gestión de datos y la comunicación con el simulador. Instálelas ejecutando el siguiente comando en la raíz del repositorio:
    pip install -r requirements.txt

Ejecución de la simulación
Para iniciar la simulación con interfaz gráfica (sumo-gui), ejecute dentro de la carpeta clonada:
    python TFG.py






