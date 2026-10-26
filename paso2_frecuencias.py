# Paso 2: frecuencia de cada termino en los abstracts

import csv
import json
import re
from pathlib import Path

CARPETA = Path(__file__).resolve().parent / "resultados"

STOPWORDS = {
    # articulos y conjunciones
    "a", "an", "the", "and", "or", "but", "nor", "so", "yet", "if", "because",
    "as", "than", "then", "whether", "either", "neither", "both", "since",
    # preposiciones
    "of", "in", "on", "at", "by", "for", "with", "about", "against", "between",
    "into", "through", "during", "before", "after", "above", "below", "to",
    "from", "up", "down", "out", "off", "over", "under", "among", "within",
    "without", "across", "upon", "via", "per", "towards", "toward",
    # pronombres y determinantes
    "i", "me", "my", "we", "our", "ours", "you", "your", "he", "him", "his",
    "she", "her", "it", "its", "they", "them", "their", "theirs", "this",
    "that", "these", "those", "what", "which", "who", "whom", "whose",
    "each", "few", "more", "most", "other", "some", "such", "any", "all",
    "own", "same", "no", "not", "only", "very", "too", "also",
    # verbos auxiliares
    "am", "is", "are", "was", "were", "be", "been", "being", "have", "has",
    "had", "having", "do", "does", "did", "doing", "can", "could", "will",
    "would", "shall", "should", "may", "might", "must",
    # adverbios
    "here", "there", "when", "where", "why", "how", "again", "further",
    "once", "just", "now", "however", "therefore", "thus", "while", "until",
    # ruido del corpus
    "ii", "iii", "iv", "co",
}


def tokenizar(texto):
    return re.findall(r"[a-z]+", texto.lower())


def es_termino_valido(palabra):
    # se dejan las de 2 letras para no perder "ai"
    return len(palabra) > 1 and palabra not in STOPWORDS


def contar_frecuencias(abstracts):
    frecuencias = {}
    for abstract in abstracts:
        for palabra in tokenizar(abstract):
            if es_termino_valido(palabra):
                frecuencias[palabra] = frecuencias.get(palabra, 0) + 1
    return frecuencias


def main():
    corpus = json.loads((CARPETA / "abstracts.json").read_text(encoding="utf-8"))
    abstracts = [articulo["abstract"] for articulo in corpus]

    frecuencias = contar_frecuencias(abstracts)

    # se guarda sin ordenar, eso lo hacen los algoritmos en el paso 3
    with open(CARPETA / "frecuencias.csv", "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["termino", "frecuencia"])
        escritor.writerows(frecuencias.items())

    total_palabras = sum(len(tokenizar(a)) for a in abstracts)
    total_terminos = sum(frecuencias.values())
    n = len(frecuencias)
    k = max(frecuencias.values())
    mas_frecuente = max(frecuencias, key=frecuencias.get)
    solo_una_vez = sum(1 for f in frecuencias.values() if f == 1)

    print(f"Palabras en los 20 abstracts           : {total_palabras}")
    print(f"Quedan después de quitar stopwords     : {total_terminos}")
    print(f"Términos distintos (n)                 : {n}")
    print(f"Frecuencia máxima (k)                  : {k}  ('{mas_frecuente}')")
    print(f"Términos que aparecen una sola vez     : {solo_una_vez}")
    print("\nLista guardada en resultados/frecuencias.csv (sin ordenar)")


if __name__ == "__main__":
    main()
