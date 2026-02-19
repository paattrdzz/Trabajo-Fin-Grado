import pandas as pd
import xml.etree.ElementTree as ET
import requests
from datetime import datetime # Librería para gestionar fechas y horas

def descargar_datos_madrid():
    # URL oficial del Ayuntamiento de Madrid con los datos de tráfico en tiempo real
    url = "https://informo.madrid.es/informo/tmadrid/pm.xml"
    
    # Capturo el momento exacto de la petición para tener constancia en el log
    ahora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    print(f">>> Conectando con el Ayuntamiento de Madrid...")
    
    try:
        # Realizo la descarga del archivo XML
        response = requests.get(url)
        if response.status_code == 200:
            # Si la descarga es exitosa, sobreescribo el archivo local para tenerlo actualizado
            with open('informacion_trafico.xml', 'wb') as f:
                f.write(response.content)
            print("Datos descargados y actualizados correctamente.")
        else:
            print("Error: No se pudo conectar con el servidor.")
    except Exception as e:
        print(f"Error en la descarga: {e}")

def obtener_datos_madrid():
    # Ejecuto la descarga antes de cualquier procesamiento
    descargar_datos_madrid()
    
    # Formateo de fecha para el encabezado del reporte final
    fecha_tabla = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

    # Cargo el CSV local que contiene la ubicación y nombres de los sensores de Madrid
    df_ubicaciones = pd.read_csv('pmed_ubicacion_12-2025.csv', sep=';', encoding='latin-1')
    
    # Filtro los datos para trabajar únicamente con el Distrito 1 (Centro), que es el área de mi red en SUMO
    sensores_centro = df_ubicaciones[df_ubicaciones['distrito'] == 1].copy()

    try:
        # Parseo el archivo XML recién descargado con la información dinámica de tráfico
        tree = ET.parse('informacion_trafico.xml')
        root = tree.getroot()
        
        # Creo un diccionario auxiliar para almacenar Intensidad y Carga indexados por el ID del sensor
        dict_datos = {}
        for pm in root.findall('pm'):
            id_id = pm.find('idelem').text
            inte = pm.find('intensidad').text
            carg = pm.find('carga').text
            dict_datos[id_id] = {'Intensidad': inte, 'Carga': carg}

        # Convierto los IDs a string para asegurar que el cruce de datos entre CSV y XML sea exacto
        sensores_centro['id'] = sensores_centro['id'].astype(int).astype(str)
        
        # Mapeo la intensidad y la carga desde el diccionario al DataFrame de sensores del centro
        sensores_centro['Intensidad'] = sensores_centro['id'].apply(lambda x: dict_datos.get(x, {}).get('Intensidad', 'N/A'))
        sensores_centro['Carga %'] = sensores_centro['id'].apply(lambda x: dict_datos.get(x, {}).get('Carga', 'N/A'))

        # --- GENERACIÓN DE LA SALIDA POR CONSOLA ---
        print("\n" + "="*85)
        print(f" ESTADO DEL TRÁFICO EN TIEMPO REAL - DISTRITO CENTRO")
        print(f" Descargado el: {fecha_tabla}")
        print("="*85)
        
        # Filtro para mostrar solo los sensores que tienen datos reportados en este momento
        resultado = sensores_centro[sensores_centro['Intensidad'] != 'N/A']
        
        # Muestro el top 20 de sensores (incluyendo Gran Vía, Callao, etc.)
        print(resultado[['id', 'nombre', 'Intensidad', 'Carga %']].head(50))
        print("="*85)

    except Exception as e:
        print(f"Error al procesar datos: {e}")

# Bloque de ejecución principal
if __name__ == "__main__":
    obtener_datos_madrid()