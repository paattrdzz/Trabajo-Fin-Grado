import traci
from datetime import datetime
import time
import subprocess
import os
from control_semaforos import dar_paso_emergencias

def ejecutar_adaptador():
    print("\n>>> Sincronizando datos con el Ayuntamiento...")
    try:
        # Usamos cwd para que el adaptador se ejecute "sentado" en su propia carpeta
        subprocess.run(["python", "adaptador_sumo.py"], cwd="datos_trafico", check=True)
        print(">>> Datos actualizados correctamente.")
    except Exception as e:
        print(f"[!] Error al actualizar datos: {e}")

def ejecutar():
    try:
        
        respuesta = input("¿Desea activar el sistema de prioridad semafórica para emergencias? (s/n): ").lower()
        prioridad_activa = True if respuesta == 's' else False
        
        if prioridad_activa:
            print("\n>>> MODO: Prioridad de emergencias ACTIVA.")
        else:
            print("\n>>> MODO: Simulación de tráfico estándar (Sin prioridad).")


        # 1. Primera actualización
        ejecutar_adaptador()

        # 2. Iniciamos SUMO
        traci.start(["sumo-gui", "-c", "simulacion_centro.sumocfg", "--start"])
        
        while True: 
            ahora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            # Lista de tus coches policía/emergencia
            objetivos = ["coche_1", "coche_2", "coche_3", "coche_4", "coche_5", "coche_6"]
            tiempos_llegada = {}

            print(f"\n>>> Nueva ejecución iniciada el: {ahora}")
            
            while traci.simulation.getMinExpectedNumber() > 0:
                traci.simulationStep()
                vehiculos_actuales = traci.vehicle.getIDList()

                if prioridad_activa:
                    dar_paso_emergencias(vehiculos_actuales)
                
                for coche_id in objetivos:
                    if coche_id in vehiculos_actuales and coche_id not in tiempos_llegada:
                        if traci.vehicle.isStopped(coche_id):
                            tiempo_actual = traci.simulation.getTime()
                            tiempos_llegada[coche_id] = tiempo_actual
                            print(f"  🏁 {coche_id} ha llegado! Tiempo: {tiempo_actual:.2f} s")

                if len(tiempos_llegada) == 6:
                    break

            # Resumen de resultados
            print("\n" + "═"*45)
            print(f"   RESUMEN DE RESULTADOS ({ahora})")
            print("═"*45)
            for coche in sorted(tiempos_llegada, key=tiempos_llegada.get):
                print(f" {coche.ljust(12)}: {tiempos_llegada[coche]:.2f} seg")
            print("═"*45)

            # 5. RECARGA DINÁMICA
            print("\n[INFO] Esperando 30s para actualizar tráfico y reiniciar...")
            time.sleep(30) 
            
            ejecutar_adaptador()
            traci.load(["-c", "simulacion_centro.sumocfg", "--start"]) 

    except traci.exceptions.FatalTraCIError:
        print("\n[!] La conexión con SUMO se cerró.")
    except Exception as e:
        print(f"\n[!] Error inesperado: {e}")
    finally:
    # Esto asegura que el "teléfono" se cuelgue bien pase lo que pase
        try:
            traci.close()
            print(">>> Conexión cerrada correctamente.")
        except traci.exceptions.FatalTraCIError:
            pass # Si ya estaba cerrado, no hacemos nada

if __name__ == "__main__":
    ejecutar()