import requests
from lxml import etree
import os
import time
import schedule
import urllib3

# --- CONFIGURACIÓN DE URL Y ARCHIVOS ---
URL_INCIDENCIAS = "https://mc30.es/xml-data/incidencias.xml" 
LOG_FILE_PATH = "log_incidencias_historicas.xml"


def descargar_y_registrar_novedades():
    """Descarga el XML, detecta nuevas incidencias y las añade al log histórico."""
    print(f"[{time.strftime('%H:%M:%S')}] Descargando incidencias de tiempo real...")
    
    try:
        # 1. DESCARGA (verify=False para evitar el error del certificado SSL)
        response = requests.get(URL_INCIDENCIAS, timeout=10, verify=False)
        response.raise_for_status()
        root_actual = etree.fromstring(response.content)
        
        # 2. CARGA DEL LOG HISTÓRICO
        if os.path.exists(LOG_FILE_PATH):
            parser = etree.XMLParser(remove_blank_text=True)
            root_historico = etree.parse(LOG_FILE_PATH, parser).getroot()
        else:
            # Si el archivo no existe, lo creamos 
            root_historico = etree.Element("IncidenciasHistoricas")
        
        # Obtener los IDs de las incidencias que ya tenemos en el log
        incidencias_historicas_ids = {
            incidencia.find("Identificador").text 
            for incidencia in root_historico.xpath("//Incidencia")
            if incidencia.find("Identificador") is not None
        }
        
        nuevas_incidencias_encontradas = 0

        # 3. REGISTRO
        # Iteramos sobre las incidencias del feed actual
        for incidencia_element in root_actual.xpath("//Incidencia"):
            
            identificador_element = incidencia_element.find("Identificador")
            
            # Si la incidencia tiene identificador y no está en el histórico
            if identificador_element is not None:
                identificador = identificador_element.text
                
                if identificador not in incidencias_historicas_ids:
                    
                    # 4. ALMACENAMIENTO
                    # Añadimos el elemento de incidencia completo al log
                    root_historico.append(incidencia_element)
                    incidencias_historicas_ids.add(identificador)
                    nuevas_incidencias_encontradas += 1
        
        # 5. GUARDAR EL LOG ACTUALIZADO
        if nuevas_incidencias_encontradas > 0:
            tree = etree.ElementTree(root_historico)
            tree.write(LOG_FILE_PATH, pretty_print=True, encoding='utf-8', xml_declaration=True)
            print(f"Log actualizado. {nuevas_incidencias_encontradas} nuevas incidencias añadidas al log.")
        else:
            print(" No se encontraron nuevas incidencias en el feed. Esperando 5 minutos.")
            
    except requests.exceptions.RequestException as e:
        print(f" Error de red al descargar: {e}")
    except Exception as e:
        print(f" Error al procesar el XML: {e}")


def main():
    """Configura el bucle de ejecución cada 5 minutos."""
    
    # Ejecutamos la función inmediatamente al inicio
    descargar_y_registrar_novedades() 
    
    # Programamos la tarea para que se ejecute cada 5 minutos
    schedule.every(5).minutes.do(descargar_y_registrar_novedades)
    
    print("\n=======================================================")
    print("Iniciando monitoreo de incidencias (cada 5 minutos)...")
    print(f"El log histórico se guarda en: {LOG_FILE_PATH}")
    print("=======================================================")

    # Bucle principal para que schedule pueda ejecutar las tareas programadas
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()