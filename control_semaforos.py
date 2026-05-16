import traci
import warnings

def dar_paso_emergencias(vehiculos_actuales):
    """
    Detecta vehículos de emergencia, enciende sus luces azules 
    y busca la fase verde automáticamente.
    """
    policias = ["coche_1", "coche_2", "coche_3"] 
    
    for policia in policias:
        if policia in vehiculos_actuales:
            semaforos = traci.vehicle.getNextTLS(policia)
            
            if len(semaforos) > 0:
                tls_id = semaforos[0][0]       
                tls_index = semaforos[0][1]    
                distancia = semaforos[0][2]    
                
                if distancia < 150:
                    try:
                        # Silenciamos el Warning de versión de SUMO
                        with warnings.catch_warnings():
                            warnings.simplefilter("ignore")
                            logicas = traci.trafficlight.getCompleteRedYellowGreenDefinition(tls_id)
                        
                        if logicas:
                            fases = logicas[0].phases
                            
                            for num_fase, fase in enumerate(fases):
                                estado_luces = fase.state 
                                
                                if estado_luces[tls_index].lower() == 'g':
                                    traci.trafficlight.setPhase(tls_id, num_fase)
                                    break 
                                    
                    except traci.exceptions.TraCIException:
                        pass