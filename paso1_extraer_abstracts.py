# Paso 1: extrae el abstract de cada PDF

import json
import re
import sys
import unicodedata
from pathlib import Path

from pdfminer.high_level import extract_text
from pdfminer.layout import LAParams

BASE = Path(__file__).resolve().parent

# con line_margin en 1.0 el abstract del articulo 14 no sale partido
PARAMETROS = LAParams(line_margin=1.0)


def espaciada(palabra):
    return r"\s*".join(palabra)


# cada editorial escribe distinto el encabezado: "A B S T R A C T", "Abstract" o "Abstract:"
INICIO = re.compile(rf"^\s*(?:{espaciada('ABSTRACT')}|Abstract)\s*:?", re.MULTILINE)

PALABRAS_CLAVE = rf"(?:{espaciada('KEYWORDS')}|Keywords)"

# el abstract termina en las palabras clave, en "Citation:", en la introduccion o en una linea en blanco
FIN = re.compile(
    rf"^\s*(?:{PALABRAS_CLAVE}|Citation:|(?:\d\.\s*)?Introduction\b)|\n\s*\n",
    re.MULTILINE,
)

# rotulos del resumen estructurado de Emerald (articulo 13)
ROTULOS = re.compile(
    r"^(?:Purpose|Design/methodology/approach|Findings|Research limitations/implications"
    r"|Practical implications|Social implications|Originality/value)\s*[–-]\s*",
    re.MULTILINE,
)

PARTIDA = re.compile(r"(\w+)-[ \t]*\n\s*(\w+)")


def normalizar(texto):
    # NFKC cambia las ligaduras (como fi) por letras normales
    return unicodedata.normalize("NFKC", texto).replace("­", "")


def recortar_abstract(texto):
    inicio = INICIO.search(texto)
    if inicio is None:
        return None
    resto = texto[inicio.end():].lstrip()

    # en Elsevier las palabras clave salen antes del abstract
    if re.match(PALABRAS_CLAVE, resto):
        resto = resto[re.search(r"\n\s*\n", resto).end():].lstrip()

    fin = FIN.search(resto)
    return resto[: fin.start()] if fin else resto


def construir_lexico(ruta_pdf):
    texto = normalizar(extract_text(ruta_pdf, laparams=PARAMETROS)).lower()
    return set(re.findall(r"[a-z]+(?:-[a-z]+)*", texto))


def reparar_guiones(abstract, ruta_pdf):
    # une las palabras partidas al final de linea, pero las compuestas (AI-driven) quedan con guion
    if not PARTIDA.search(abstract):
        return abstract
    lexico = construir_lexico(ruta_pdf)

    def decidir(m):
        a, b = m.group(1), m.group(2)
        if (a + b).lower() in lexico:
            return a + b
        if f"{a}-{b}".lower() in lexico:
            return f"{a}-{b}"
        return a + b

    return PARTIDA.sub(decidir, abstract)


def limpiar(abstract):
    abstract = ROTULOS.sub("", abstract)
    return re.sub(r"\s+", " ", abstract).strip()


def extraer_abstract(ruta_pdf):
    pagina1 = normalizar(extract_text(ruta_pdf, page_numbers=[0], laparams=PARAMETROS))
    abstract = recortar_abstract(pagina1)
    if abstract is None:
        return None
    abstract = reparar_guiones(abstract, ruta_pdf)
    return limpiar(abstract)


def numero_articulo(ruta):
    m = re.match(r"\d+", ruta.name)
    return int(m.group()) if m else None


def main():
    carpeta = Path(sys.argv[1]) if len(sys.argv) > 1 else BASE / "articulos"
    pdfs = sorted(carpeta.glob("*.pdf"), key=lambda r: (numero_articulo(r) or 999, r.name))

    corpus = []
    for i, ruta in enumerate(pdfs, start=1):
        abstract = extraer_abstract(ruta)
        if abstract is None:
            print(f"[AVISO] No se encontró el encabezado del abstract en: {ruta.name}")
            continue
        palabras = abstract.split()
        id_articulo = numero_articulo(ruta) or i
        corpus.append({
            "id": id_articulo,
            "archivo": ruta.name,
            "abstract": abstract,
            "palabras": len(palabras),
        })
        print(f"{id_articulo:>2} | {len(palabras):>3} palabras | "
              f"{' '.join(palabras[:5])} ... {' '.join(palabras[-4:])}")

    salida = BASE / "resultados" / "abstracts.json"
    salida.parent.mkdir(exist_ok=True)
    salida.write_text(json.dumps(corpus, ensure_ascii=False, indent=2), encoding="utf-8")
    total = sum(a["palabras"] for a in corpus)
    print(f"\n{len(corpus)} abstracts guardados en resultados/abstracts.json ({total} palabras en total)")


if __name__ == "__main__":
    main()
