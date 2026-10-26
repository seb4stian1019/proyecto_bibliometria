# Paso 5: top 15 de cada algoritmo

import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from ordenamientos import ALGORITMOS

CARPETA = Path(__file__).resolve().parent / "resultados"
TOP = 15


def archivo_ranking(nombre_algoritmo):
    return CARPETA / ("ranking_" + nombre_algoritmo.lower().replace(" ", "_") + ".csv")


def leer_ranking(nombre_algoritmo):
    with open(archivo_ranking(nombre_algoritmo), encoding="utf-8") as archivo:
        return [(fila["termino"], int(fila["frecuencia"])) for fila in csv.DictReader(archivo)]


def guardar_comparacion(tops, coinciden):
    nombres = list(tops)
    with open(CARPETA / "top15_comparacion.csv", "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        encabezado = ["posicion"]
        for nombre in nombres:
            clave = nombre.lower().replace(" sort", "")
            encabezado += [f"{clave}_termino", f"{clave}_frecuencia"]
        escritor.writerow(encabezado + ["coinciden"])
        for i in range(TOP):
            fila = [i + 1]
            for nombre in nombres:
                fila += list(tops[nombre][i])
            escritor.writerow(fila + ["sí" if coinciden[i] else "no"])


def grafico_top15(top, siguiente):
    terminos = [t for t, _ in top][::-1]
    frecuencias = [f for _, f in top][::-1]
    empate = siguiente[1] == top[-1][1]  # el puesto 16 empata con el 15
    colores = ["#8FAADC" if empate and f == top[-1][1] else "#2E5597" for f in frecuencias]

    fig, eje = plt.subplots(figsize=(7, 5.2), dpi=150)
    barras = eje.barh(terminos, frecuencias, color=colores)
    for barra, valor in zip(barras, frecuencias):
        eje.annotate(str(valor), (valor, barra.get_y() + barra.get_height() / 2),
                     xytext=(4, 0), textcoords="offset points", va="center", fontsize=9)
    eje.set_xlabel("Frecuencia en los 20 abstracts")
    eje.set_title("Los 15 términos más frecuentes del corpus\n(resultado idéntico con Counting, Radix y Bucket Sort)", fontsize=11)
    eje.set_xlim(0, max(frecuencias) * 1.12)
    eje.spines[["top", "right"]].set_visible(False)
    if empate:
        eje.text(0.98, 0.03, f"Tono claro: empatados con {top[-1][1]} apariciones;\n"
                             f"«{siguiente[0]}» (también {siguiente[1]}) queda en el puesto {TOP + 1}.",
                 transform=eje.transAxes, ha="right", va="bottom", fontsize=8, color="#404040")
    fig.tight_layout()
    fig.savefig(CARPETA / "grafico_top15.png")
    plt.close(fig)


def main():
    rankings = {nombre: leer_ranking(nombre) for nombre in ALGORITMOS}
    tops = {nombre: ranking[:TOP] for nombre, ranking in rankings.items()}

    # los tres deben coincidir en cada posicion
    coinciden = [len({tops[nombre][i] for nombre in tops}) == 1 for i in range(TOP)]

    nombres = list(tops)
    print(f"{'Pos.':<6}" + "".join(f"{n:<20}" for n in nombres) + "¿Coinciden?")
    for i in range(TOP):
        celdas = "".join(f"{tops[n][i][0] + ' (' + str(tops[n][i][1]) + ')':<20}" for n in nombres)
        print(f"{i + 1:<6}{celdas}{'sí' if coinciden[i] else 'NO'}")

    print(f"\nPosiciones del top {TOP} en las que coinciden los tres algoritmos: {sum(coinciden)} de {TOP}")
    todo_igual = all(r == rankings[nombres[0]] for r in rankings.values())
    print(f"¿Coinciden también en el ranking completo ({len(rankings[nombres[0]])} términos)? {'SÍ' if todo_igual else 'NO'}")

    guardar_comparacion(tops, coinciden)
    referencia = rankings[nombres[0]]
    grafico_top15(referencia[:TOP], referencia[TOP])
    print("\nTabla y gráfico guardados en resultados/ (top15_comparacion.csv, grafico_top15.png)")


if __name__ == "__main__":
    main()
