# Paso 3: ordenar la lista de frecuencias con los tres algoritmos

import csv
from pathlib import Path

from ordenamientos import ALGORITMOS

CARPETA = Path(__file__).resolve().parent / "resultados"
TOP = 15


def leer_frecuencias():
    with open(CARPETA / "frecuencias.csv", encoding="utf-8") as archivo:
        return [(fila["termino"], int(fila["frecuencia"])) for fila in csv.DictReader(archivo)]


def guardar_ranking(nombre_algoritmo, ranking):
    nombre_archivo = "ranking_" + nombre_algoritmo.lower().replace(" ", "_") + ".csv"
    with open(CARPETA / nombre_archivo, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["posicion", "termino", "frecuencia"])
        for posicion, (termino, frecuencia) in enumerate(ranking, start=1):
            escritor.writerow([posicion, termino, frecuencia])
    return nombre_archivo


def main():
    pares = leer_frecuencias()
    print(f"Términos a ordenar: {len(pares)}\n")

    rankings = {}
    for nombre, algoritmo in ALGORITMOS.items():
        rankings[nombre] = algoritmo(list(pares))  # cada uno recibe una copia
        archivo = guardar_ranking(nombre, rankings[nombre])
        print(f"{nombre:<14} -> resultados/{archivo}")

    resultados = list(rankings.values())
    iguales = all(r == resultados[0] for r in resultados)
    print(f"\n¿Los tres algoritmos dan exactamente el mismo orden? {'SÍ' if iguales else 'NO'}")

    # sorted solo se usa para comprobar
    referencia = sorted(pares, key=lambda par: -par[1])
    print(f"¿Coinciden con el ordenamiento de referencia de Python?  {'SÍ' if resultados[0] == referencia else 'NO'}")

    print(f"\nTop {TOP}:")
    for posicion, (termino, frecuencia) in enumerate(resultados[0][:TOP], start=1):
        print(f"  {posicion:>2}. {termino:<14} {frecuencia}")


if __name__ == "__main__":
    main()
