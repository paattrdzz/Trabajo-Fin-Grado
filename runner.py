import os
import sys
import traci

# --- TUS DATOS ---
CONFIG_FILE_NAME = "simulacion_centro.sumocfg"

# IDs extraídos de tus imágenes
CALLE_ORIGEN = "4346299#6"   
CALLE_DESTINO = "542325013"  
# -----------------

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Por favor, declara la variable de entorno 'SUMO_HOME'")

def run():
    print(f">> Cargando: {CONFIG_FILE_NAME}")
    
    # 1. Calculamos la ruta
    try:
        ruta_info = traci.simulation.findRoute(CALLE_ORIGEN, CALLE_DESTINO)
        lista_calles = ruta_info.edges
    except Exception as e:
        lista_calles = []
        print(f"Error calculando ruta: {e}")

    if lista_calles:
        print(f"✅ Ruta calculada: {len(lista_calles)} tramos.")
        traci.route.add("ruta_tfg", lista_calles)
        
        # 2. Inyectamos el coche
        try:
            traci.vehicle.add(
                vehID="coche_tfg", 
                routeID="ruta_tfg", 
                depart="1.0",
                departPos="last",
                departLane="best"
            )
            traci.vehicle.setColor("coche_tfg", (255, 0, 0)) # Rojo
            print(">> Coche TFG creado. Buscando hueco para salir...")
        except traci.TraCIException as e:
            print(f"❌ Error al crear coche: {e}")
    else:
        print("❌ No hay ruta válida entre esos dos puntos.")

    # 3. Bucle de simulación y toma de datos
    step = 0
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        
        # --- AQUÍ ESTÁ LO QUE TE INTERESA ---
        if "coche_tfg" in traci.vehicle.getIDList():
            # Sacamos datos en tiempo real
            velocidad_kmh = traci.vehicle.getSpeed("coche_tfg") * 3.6
            calle_actual = traci.vehicle.getRoadID("coche_tfg")
            
            # Imprimimos datos cada 10 pasos
            if step % 10 == 0:
                print(f"[TFG DATA] Paso: {step} | Calle: {calle_actual} | Vel: {velocidad_kmh:.1f} km/h")
        
        else:
            # --- CORRECCIÓN DEL ERROR AQUÍ ---
            # En lugar de pedir la cuenta directa, pedimos la lista y medimos su longitud (len)
            lista_pendientes = traci.simulation.getPendingVehicles()
            pendientes = len(lista_pendientes)
            
            if pendientes > 0 and step % 100 == 0:
                print(f"[ESPERANDO] Hay {pendientes} coches en cola (incluido el tuyo) esperando hueco.")

        step += 1

    traci.close()
    sys.stdout.flush()

if __name__ == "__main__":
    carpeta_actual = os.path.dirname(os.path.abspath(__file__))
    path_config = os.path.join(carpeta_actual, CONFIG_FILE_NAME)

    if not os.path.exists(path_config):
        print(f"¡ERROR! No encuentro {CONFIG_FILE_NAME} en {carpeta_actual}")
    else:
        # --start: arranca solo
        # --quit-on-end: se cierra solo al acabar
        sumoCmd = ["sumo-gui", "-c", path_config, "--start", "--quit-on-end"]
        traci.start(sumoCmd)
        run()