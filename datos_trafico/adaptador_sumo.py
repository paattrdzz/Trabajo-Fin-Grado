
def actualizar_rutas_con_datos_reales():
    # ... (parte de descarga de datos) ...
    
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
                
                # ESTA ES LA LÍNEA CLAVE
                print(f"   📊 {flow_id} -> {nueva_intensidad.rjust(4)} veh/h (Sensor {id_sensor_real})")
                
                flow.set('vehsPerHour', nueva_intensidad)
                actualizados += 1

        tree_rutas.write(RUTA_MIS_RUTAS, encoding='UTF-8', xml_declaration=True)
        print(f"✅ ÉXITO: {actualizados} flujos actualizados.")

    except Exception as e:
        print(f"❌ Error interno: {e}")