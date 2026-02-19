import traci

def ejecutar():
    try:
        # 1. Lanzo la interfaz gráfica de SUMO cargando mi archivo de configuración del Distrito Centro
        traci.start(["sumo-gui", "-c", "simulacion_centro.sumocfg"])
        
        # 2. Defino mis vehículos "testigo" para medir los tiempos de las 3 rutas
        objetivos = ["coche_1", "coche_2", "coche_3"]
        tiempos_llegada = {}  # Diccionario para guardar cuándo llega cada uno

        print(">>> Simulación iniciada. Esperando a que los coches lleguen al destino...")

        # 3. Bucle principal: se ejecuta mientras haya vehículos en la simulación
        while traci.simulation.getMinExpectedNumber() > 0:
            traci.simulationStep() # Avanzamos paso a paso (segundo a segundo)
            
            # Obtengo la lista de IDs de todos los coches que están circulando ahora mismo
            vehiculos_actuales = traci.vehicle.getIDList()

            for coche_id in objetivos:
                # Si el coche está en el mapa y todavía no he registrado su tiempo de llegada:
                if coche_id in vehiculos_actuales and coche_id not in tiempos_llegada:
                    
                    # Verifico si el coche ha llegado a su destino (marcado como stop en el .rou.xml)
                    if traci.vehicle.isStopped(coche_id):
                        tiempo_actual = traci.simulation.getTime() # Capturo el segundo exacto
                        tiempos_llegada[coche_id] = tiempo_actual
                        print(f" ¡{coche_id} ha llegado! Tiempo: {tiempo_actual} segundos.")

            # Para no alargar la simulación, si ya tengo los 3 tiempos, corto el bucle
            if len(tiempos_llegada) == 3:
                print(">>> Los 3 coches han llegado a su destino.")
                break

        # 4. Bloque de salida para mostrar los datos finales ordenados
        print("\n" + "="*30)
        print("   RESUMEN DE RESULTADOS")
        print("="*30)
        
        # Ordeno los resultados de menor a mayor tiempo para ver cuál es la ruta más eficiente
        for coche in sorted(tiempos_llegada, key=tiempos_llegada.get):
            print(f" {coche}: {tiempos_llegada[coche]} seg")
        print("="*30)

        # Cierro la conexión con TraCI de forma limpia
        traci.close()

    except traci.exceptions.FatalTraCIError:
        # Control de error por si cierro la ventana de SUMO manualmente antes de acabar
        print("\n[!] La conexión con SUMO se cerró.")
    except Exception as e:
        # Captura de cualquier otro fallo inesperado en el script
        print(f"\n[!] Error inesperado: {e}")

# Punto de entrada para ejecutar la función principal
if __name__ == "__main__":
    ejecutar()