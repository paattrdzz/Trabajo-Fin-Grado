Gemelo Digital para la Gestión de Emergencias (Madrid Centro)

Este proyecto implementa un Gemelo Digital utilizando SUMO (Simulation of Urban MObility) y datos de Open Data Madrid para optimizar el tránsito de vehículos de emergencia en el Distrito Centro.


Instrucciones para el despliegue

1. Requisitos Previos
    ● Tener instalado Python 3.8 o superior.
    ● Tener instalado Eclipse SUMO. Puedes descargarlo desde su web oficial.

2. Configuración de la Variable de Entorno (CRÍTICO)
El motor de simulación requiere que el sistema sepa dónde está instalado SUMO. Sin este paso, el script de Python no funcionará.
    ● Windows: Crea una variable de entorno de sistema llamada SUMO_HOME que apunte a la carpeta donde instalaste SUMO (ejemplo: C:\Program Files (x86)\Eclipse\Sumo).
    ● Linux/macOS: Añade al final de tu archivo .bashrc o .zshrc la línea: export SUMO_HOME=/usr/share/sumo.

3. Instalación de Librerías
Abre una terminal en la carpeta del proyecto y ejecuta el siguiente comando para instalar las dependencias necesarias (traci, pandas, requests):

pip install -r requirements.txt

4. Cómo Ejecutar la Simulación
Una vez configurado todo, lanza el script principal para abrir la interfaz gráfica de SUMO y ver la lógica de prioridad en funcionamiento:
python TFG.py

📊 Sobre el TFG

Este trabajo utiliza rutas relativas para todos los archivos de configuración (.net.xml, .rou.xml,.sumocfg), lo que garantiza que el proyecto sea portable y reproducible en cualquier entorno detrabajo.

Archivo/Carpeta Descripción

main.py Script principal que conecta Python con SUMO mediante TraCI.

requirements.txt Lista de dependencias de software necesarias.

red/ Contiene la red vial del Distrito Centro y las rutas de tráfico. 


