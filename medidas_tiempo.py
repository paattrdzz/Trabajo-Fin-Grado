import traci

def ejecutar():
    # Iniciamos la simulación
    traci.start(["sumo-gui", "-c", "simulacion_centro.sumocfg"])
    
    tiempo_llegada = 0
    ha_llegado = False

    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        
        # Comprobamos si el coche sigue en la red
        if "coche_1" in traci.vehicle.getIDList():
            # Si el coche está en estado de "parada" (está aparcando)
            if traci.vehicle.isStopped("coche_1") and not ha_llegado:
                tiempo_llegada = traci.simulation.getTime()
                print(f"¡Destino alcanzado! El coche ha tardado: {tiempo_llegada} segundos")
                ha_llegado = True
        
        # Si ya llegó, podemos parar el script de Python o dejarlo correr
        if ha_llegado:
            # Aquí podrías poner traci.close() si quieres que se cierre solo
            pass

    traci.close()

if __name__ == "__main__":
    ejecutar()