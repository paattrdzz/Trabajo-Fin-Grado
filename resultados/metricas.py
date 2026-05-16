import csv
import os
from collections import defaultdict

ARCHIVO = "resultados/resultados.csv"


def tipo_coche(coche_id):
    """
    Devuelve el tipo de vehículo
    """
    if coche_id in ["coche_1", "coche_2", "coche_3"]:
        return "EMERGENCIA"
    else:
        return "NORMAL"


def guardar_resultados(tiempos_llegada, modo, fecha):
    archivo_existe = os.path.isfile(ARCHIVO)

    with open(ARCHIVO, mode="a", newline="") as f:
        writer = csv.writer(f)

        # Cabecera
        if not archivo_existe:
            writer.writerow([
                "fecha",
                "modo",
                "tipo",
                "coche",
                "tiempo"
            ])

        # Guardar cada coche
        for coche, tiempo in tiempos_llegada.items():

            writer.writerow([
                fecha,
                modo,
                tipo_coche(coche),
                coche,
                tiempo
            ])


def mostrar_medias():
    if not os.path.isfile(ARCHIVO):
        print("\nNo hay resultados guardados todavía.")
        return

    datos = defaultdict(list)

    with open(ARCHIVO, mode="r") as f:
        reader = csv.DictReader(f)

        for fila in reader:
            clave = (
                fila["modo"],
                fila["tipo"],
                fila["coche"]
            )

            datos[clave].append(float(fila["tiempo"]))

    print("\n" + "═"*50)
    print("        MEDIA GLOBAL DE RESULTADOS")
    print("═"*50)

    modos = sorted(set(k[0] for k in datos.keys()))

    for modo in modos:

        print(f"\n>>> {modo}")

        for tipo in ["EMERGENCIA", "NORMAL"]:

            print(f"\n  [{tipo}]")

            coches = sorted(
                k[2]
                for k in datos.keys()
                if k[0] == modo and k[1] == tipo
            )

            for coche in coches:

                tiempos = datos[(modo, tipo, coche)]

                media = sum(tiempos) / len(tiempos)

                print(f"   {coche.ljust(10)} -> {media:.2f} s")