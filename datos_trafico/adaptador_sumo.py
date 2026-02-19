import xml.etree.ElementTree as ET
import requests
import os
from datetime import datetime

def descargar_datos_madrid(ruta_destino):
    """Descarga el XML actualizado del Ayuntamiento"""
    url = "https://informo.madrid.es/informo/tmadrid/pm.xml"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(ruta_destino, 'wb') as f:
                f.write(response.content)
            return True
    except Exception as e:
        print(f"❌ Error descargando datos: {e}")
    return False

def actualizar_rutas_con_datos_reales():
    # 1. Definimos las rutas de los archivos
    # Subimos un nivel para llegar a la carpeta de datos
    ruta_xml_madrid = "../datos_madrid/informacion_trafico.xml"
    ruta_mis_rutas = "misrutas.rou.xml"

    # 2. DESCARGA AUTOMÁTICA
    print(f">>> [{datetime.now().strftime('%H:%M:%S')}] Iniciando actualización completa...")
    if descargar_datos_madrid(ruta_xml_madrid):
        print("✅ Datos de Madrid descargados correctamente.")
    else:
        print("⚠️ No se pudo descargar, se intentará usar el archivo local existente.")

    # 3. MAPEO: Flujo SUMO -> ID Sensor Madrid (Ampliados para realismo)
    mapeo = {
        "f_4297": "4297",   "f_10386": "10386", "f_4307": "4307",
        "f_4259": "4259",   "f_4268": "4268",   "f_4262": "4262",
        "f_7133": "7133",   "f_4208": "4208",
        "f_3854": "3854",   "f_4291": "4291"
    }

    try:
        # 4. LEER DATOS REALES DEL AYUNTAMIENTO
        tree_madrid = ET.parse(ruta_xml_madrid)
        root_madrid = tree_madrid.getroot()
        
        datos_sensores = {}
        for pm in root_madrid.findall('pm'):
            id_sensor = pm.find('idelem').text
            if id_sensor in mapeo.values():
                datos_sensores[id_sensor] = pm.find('intensidad').text

        # 5. CARGAR Y ACTUALIZAR TU ARCHIVO DE RUTAS DE SUMO
        tree_rutas = ET.parse(ruta_mis_rutas)
        root_rutas = tree_rutas.getroot()

        actualizados = 0
        for flow in root_rutas.findall('flow'):
            flow_id = flow.get('id')
            if flow_id in mapeo:
                id_sensor_real = mapeo[flow_id]
                
                # Obtenemos el valor del sensor (por defecto "0" si no existe)
                valor_crudo = datos_sensores.get(id_sensor_real, "0")
                
                # --- VALIDACIÓN DE SEGURIDAD PARA SUMO ---
                # Si la intensidad es 0 o negativa, SUMO da error de "repetition rate"
                # Forzamos un mínimo de 1 vehículo/hora para mantener la simulación viva
                try:
                    valor_int = int(valor_crudo)
                    if valor_int <= 0:
                        nueva_intensidad = "1"
                    else:
                        nueva_intensidad = str(valor_int)
                except ValueError:
                    # Si el dato no es un número (ej. "N/A"), ponemos un valor base
                    nueva_intensidad = "1"
                
                # Aplicamos el cambio al atributo del XML
                flow.set('vehsPerHour', nueva_intensidad)
                print(f"   - {flow_id} (Sensor {id_sensor_real}): {nueva_intensidad} veh/h")
                actualizados += 1

        # 6. GUARDAR CAMBIOS EN EL DISCO
        tree_rutas.write(ruta_mis_rutas, encoding='UTF-8', xml_declaration=True)
        print(f"\n✅ ÉXITO: {actualizados} flujos actualizados en '{ruta_mis_rutas}'.")
        print("Ya puedes lanzar la simulación en SUMO.")

    except Exception as e:
        print(f"❌ Error en el proceso de adaptación: {e}")

if __name__ == "__main__":
    actualizar_rutas_con_datos_reales()