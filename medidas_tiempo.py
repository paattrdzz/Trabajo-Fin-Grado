import traci

def ejecutar():
    try:
        # 1. Iniciamos SUMO con tu archivo de configuración
        # (Asegúrate de que el nombre del archivo .sumocfg sea el correcto)
        traci.start(["sumo-gui", "-c", "simulacion_centro.sumocfg"])
        
        # 2. Preparamos las herramientas de medición
        objetivos = ["coche_1", "coche_2", "coche_3"]
        tiempos_llegada = {}

        print(">>> Simulación iniciada. Esperando a que los coches lleguen al destino...")

        # 3. Bucle principal de la simulación
        while traci.simulation.getMinExpectedNumber() > 0:
            traci.simulationStep() # Avanzar un segundo en la simulación
            
            vehiculos_actuales = traci.vehicle.getIDList()

            for coche_id in objetivos:
                # Si el coche está en el mapa y aún no hemos registrado su tiempo...
                if coche_id in vehiculos_actuales and coche_id not in tiempos_llegada:
                    
                    # Comprobamos si ha llegado a su parada (isStopped)
                    if traci.vehicle.isStopped(coche_id):
                        tiempo_actual = traci.simulation.getTime()
                        tiempos_llegada[coche_id] = tiempo_actual
                        print(f"✅ ¡{coche_id} ha llegado! Tiempo: {tiempo_actual} segundos.")

            # Si ya tenemos los tiempos de los 3, podemos cerrar si queremos
            if len(tiempos_llegada) == 3:
                print(">>> Los 3 coches han llegado a su destino.")
                break

        # 4. Resumen final para tu TFG
        print("\n" + "="*30)
        print("   RESUMEN DE RESULTADOS")
        print("="*30)
        # Ordenamos los resultados de más rápido a más lento
        for coche in sorted(tiempos_llegada, key=tiempos_llegada.get):
            print(f"📍 {coche}: {tiempos_llegada[coche]} seg")
        print("="*30)

        traci.close()

    except traci.exceptions.FatalTraCIError:
        # Esto evita las letras rojas feas si cierras SUMO a mano
        print("\n[!] La conexión con SUMO se cerró.")
    except Exception as e:
        print(f"\n[!] Error inesperado: {e}")

if __name__ == "__main__":
    ejecutar()
