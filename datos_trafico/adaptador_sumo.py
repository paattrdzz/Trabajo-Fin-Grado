import xml.etree.ElementTree as ET
import os
import requests
from datetime import datetime


# DEFINIMOS LAS RUTAS FUERA (Mejor práctica)
# Como en medidas_tiempo pusiste cwd="datos_trafico", aquí basta con el nombre del archivo
RUTA_XML_MADRID = "../datos_madrid/informacion_trafico.xml"
RUTA_MIS_RUTAS = "misrutas.rou.xml"

mapeo = {
    "f_4297": "4297",
    "f_10386": "10386",
    "f_4307": "4307",
    "f_4259": "4259",
    "f_4268": "4268",
    "f_4262": "4262",
    "f_7133": "7133",
    "f_4208": "4208",
    "f_3854": "3854",
    "f_4291": "4291",  
}

def descargar_datos_madrid():
    url = "https://informo.madrid.es/informo/tmadrid/pm.xml"
    ahora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    print(f">>> [{ahora}] Conectando con el Ayuntamiento de Madrid...")
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            # Guardamos el archivo en la ruta que espera el adaptador
            with open(RUTA_XML_MADRID, 'wb') as f:
                f.write(response.content)
            print("   ✅ Datos descargados y guardados correctamente.")
        else:
            print(f"   ❌ Error: Código de estado {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error en la descarga: {e}")
        return


def actualizar_rutas_con_datos_reales():
    
    descargar_datos_madrid()


    try:
        # Cargamos el XML de Madrid
        tree_madrid = ET.parse(RUTA_XML_MADRID)
        root_madrid = tree_madrid.getroot()
        
        datos_sensores = {}
        for pm in root_madrid.findall('pm'):
            idelem = pm.find('idelem')
            intensidad = pm.find('intensidad')
            if idelem is not None and intensidad is not None:
                datos_sensores[idelem.text] = intensidad.text

        # Cargamos tus rutas de SUMO
        tree_rutas = ET.parse(RUTA_MIS_RUTAS)
        root_rutas = tree_rutas.getroot()

        print(f">>> [PROCESANDO SENSORES]") # Esto debe salir en consola
        actualizados = 0
        for flow in root_rutas.findall('flow'):
            flow_id = flow.get('id')
            if flow_id in mapeo:
                id_sensor_real = mapeo[flow_id]
                valor_crudo = datos_sensores.get(id_sensor_real, "1")
                
                try:
                    valor_int = int(valor_crudo)
                    nueva_intensidad = str(max(1, valor_int))
                except:
                    nueva_intensidad = "1"
                
                print(f"   📊 {flow_id} -> {nueva_intensidad.rjust(4)} veh/h (Sensor {id_sensor_real})")
                
                flow.set('vehsPerHour', nueva_intensidad)
                actualizados += 1

        tree_rutas.write(RUTA_MIS_RUTAS, encoding='UTF-8', xml_declaration=True)
        print(f"✅ ÉXITO: {actualizados} flujos actualizados.")

    except Exception as e:
        print(f"❌ Error interno: {e}")


if __name__ == "__main__":
    actualizar_rutas_con_datos_reales()