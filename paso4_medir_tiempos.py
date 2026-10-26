# Paso 4: tiempos de ejecucion de los tres algoritmos

import csv
import gc
import platform
import random
import statistics
import time
from datetime import datetime
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

from ordenamientos import ALGORITMOS
from paso3_ordenar import leer_frecuencias

CARPETA = Path(__file__).resolve().parent / "resultados"

REPETICIONES = 1000
CALENTAMIENTO = 20

TAMANOS = [1_000, 2_000, 5_000, 10_000, 20_000, 50_000, 100_000]


def repeticiones_escala(n):
    # mas repeticiones para las listas pequenas
    return max(15, 300_000 // n)


SEMILLA = 2026
COLORES = {"Counting Sort": "#2E5597", "Radix Sort": "#C55A11", "Bucket Sort": "#548235"}


def medir_una_vez(algoritmo, pares):
    copia = list(pares)  # la copia no se mide
    inicio = time.perf_counter_ns()
    algoritmo(copia)
    fin = time.perf_counter_ns()
    return (fin - inicio) / 1_000_000  # ns a ms


def medir(pares, repeticiones, calentamiento):
    nombres = list(ALGORITMOS)
    for nombre in nombres:
        for _ in range(calentamiento):
            ALGORITMOS[nombre](list(pares))

    tiempos = {nombre: [] for nombre in nombres}
    gc.collect()
    gc.disable()  # sin recolector de basura mientras se mide
    try:
        for _ in range(repeticiones):
            random.shuffle(nombres)  # orden aleatorio en cada ronda
            for nombre in nombres:
                tiempos[nombre].append(medir_una_vez(ALGORITMOS[nombre], pares))
    finally:
        gc.enable()
    return tiempos


def resumir(muestras):
    return {
        "mediana": statistics.median(muestras),
        "media": statistics.mean(muestras),
        "desviacion": statistics.stdev(muestras),
        "minimo": min(muestras),
        "maximo": max(muestras),
    }


def lista_de_prueba(n, frecuencias_corpus):
    # frecuencias sorteadas de las del corpus
    return [(f"t{i}", f) for i, f in enumerate(random.choices(frecuencias_corpus, k=n))]


DECIMAL = FuncFormatter(lambda v, _: f"{v:g}".replace(".", ","))
MILES = FuncFormatter(lambda v, _: f"{int(v):,}".replace(",", "."))


def grafico_corpus(resumenes, n, k):
    nombres = list(resumenes)
    medianas = [resumenes[a]["mediana"] for a in nombres]
    fig, eje = plt.subplots(figsize=(7, 4.2), dpi=150)
    barras = eje.bar(nombres, medianas, color=[COLORES[a] for a in nombres], width=0.55)
    for barra, valor in zip(barras, medianas):
        eje.annotate(f"{valor:.3f} ms".replace(".", ","), (barra.get_x() + barra.get_width() / 2, valor),
                     ha="center", va="bottom", xytext=(0, 4), textcoords="offset points", fontsize=10)
    eje.set_ylabel("Tiempo (ms, mediana)")
    eje.set_title(f"Tiempo de ordenamiento de la lista del corpus (n = {n}, k = {k})", fontsize=11)
    eje.set_ylim(0, max(medianas) * 1.2)
    eje.yaxis.set_major_formatter(DECIMAL)
    eje.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(CARPETA / "grafico_tiempos_corpus.png")
    plt.close(fig)


def grafico_escalabilidad(filas):
    fig, eje = plt.subplots(figsize=(7, 4.2), dpi=150)
    for nombre in ALGORITMOS:
        puntos = [(f["n"], f["mediana_ms"]) for f in filas if f["algoritmo"] == nombre]
        eje.plot([x for x, _ in puntos], [y for _, y in puntos], marker="o",
                 color=COLORES[nombre], label=nombre)
    eje.set_xlabel("Número de términos (n)")
    eje.set_ylabel("Tiempo (ms, mediana)")
    eje.set_title("Crecimiento del tiempo al aumentar n (k = 86)", fontsize=11)
    eje.xaxis.set_major_formatter(MILES)
    eje.yaxis.set_major_formatter(DECIMAL)
    eje.grid(alpha=0.3)
    eje.legend()
    eje.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(CARPETA / "grafico_escalabilidad.png")
    plt.close(fig)


def main():
    random.seed(SEMILLA)
    pares = leer_frecuencias()
    n = len(pares)
    k = max(f for _, f in pares)

    # lista del corpus
    print(f"Midiendo sobre la lista del corpus (n = {n}, k = {k}), {REPETICIONES} repeticiones...")
    resumenes = {nombre: resumir(m) for nombre, m in medir(pares, REPETICIONES, CALENTAMIENTO).items()}

    with open(CARPETA / "tiempos_corpus.csv", "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["algoritmo", "mediana_ms", "media_ms", "desviacion_ms", "minimo_ms", "maximo_ms", "repeticiones"])
        for nombre, r in resumenes.items():
            escritor.writerow([nombre] + [f"{r[c]:.4f}" for c in ("mediana", "media", "desviacion", "minimo", "maximo")] + [REPETICIONES])

    print(f"\n{'Algoritmo':<14}{'Mediana':>10}{'Media':>10}{'Desv.':>10}{'Mínimo':>10}   (ms)")
    for nombre, r in resumenes.items():
        print(f"{nombre:<14}{r['mediana']:>10.4f}{r['media']:>10.4f}{r['desviacion']:>10.4f}{r['minimo']:>10.4f}")
    grafico_corpus(resumenes, n, k)

    # listas mas grandes
    print(f"\nMidiendo con listas de {TAMANOS[0]:,} a {TAMANOS[-1]:,} términos...".replace(",", "."))
    frecuencias_corpus = [f for _, f in pares]
    filas = []
    for tamano in TAMANOS:
        lista = lista_de_prueba(tamano, frecuencias_corpus)
        for nombre, muestras in medir(lista, repeticiones_escala(tamano), 5).items():
            filas.append({"algoritmo": nombre, "n": tamano, "mediana_ms": statistics.median(muestras)})

    with open(CARPETA / "tiempos_escalabilidad.csv", "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["algoritmo", "n", "mediana_ms"])
        for f in filas:
            escritor.writerow([f["algoritmo"], f["n"], f"{f['mediana_ms']:.4f}"])

    # tiempo por termino y ajuste a una recta
    print(f"\n{'Algoritmo':<14}{'µs/término (n menor)':>22}{'µs/término (n mayor)':>22}{'R²':>9}")
    with open(CARPETA / "ajuste_lineal.csv", "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["algoritmo", "us_por_termino_n_menor", "us_por_termino_n_mayor", "pendiente_ms_por_termino", "r2"])
        for nombre in ALGORITMOS:
            xs = [f["n"] for f in filas if f["algoritmo"] == nombre]
            ys = [f["mediana_ms"] for f in filas if f["algoritmo"] == nombre]
            pendiente, _ = statistics.linear_regression(xs, ys)
            r2 = statistics.correlation(xs, ys) ** 2
            por_termino_menor = ys[0] * 1000 / xs[0]
            por_termino_mayor = ys[-1] * 1000 / xs[-1]
            escritor.writerow([nombre, f"{por_termino_menor:.4f}", f"{por_termino_mayor:.4f}", f"{pendiente:.8f}", f"{r2:.4f}"])
            print(f"{nombre:<14}{por_termino_menor:>22.3f}{por_termino_mayor:>22.3f}{r2:>9.4f}")
    grafico_escalabilidad(filas)

    (CARPETA / "entorno.txt").write_text(
        f"Fecha: {datetime.now():%Y-%m-%d %H:%M}\n"
        f"Sistema: {platform.platform()}\n"
        f"Procesador: {platform.processor() or platform.machine()}\n"
        f"Python: {platform.python_version()}\n", encoding="utf-8")
    print("\nTablas, gráficos y datos del equipo guardados en resultados/")


if __name__ == "__main__":
    main()
