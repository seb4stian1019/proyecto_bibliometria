# Análisis de algoritmos en el contexto de la bibliometría (Seguimiento 2026-2)

Ranking de los términos más frecuentes en los abstracts de 20 artículos científicos,
usando algoritmos de ordenamiento no basados en comparaciones.

**Autores:** Samuel Salgado Figueroa y Sebastian Amaya Castaño  
**Curso:** Análisis de Algoritmos, Universidad del Quindío

## Cómo ejecutarlo

1. Instalar las dependencias: `pip install -r requirements.txt`
2. Copiar los 20 PDF en la carpeta `articulos/`
3. Ejecutar: `python main.py`

## Archivos

| Archivo | Qué hace |
|---|---|
| `paso1_extraer_abstracts.py` | Extrae el abstract de cada PDF → `resultados/abstracts.json` |
| `paso2_frecuencias.py` | Cuenta la frecuencia de cada término → `resultados/frecuencias.csv` |
| `ordenamientos.py` | Counting Sort, Radix Sort y Bucket Sort |
| `paso3_ordenar.py` | Ordena con los 3 algoritmos → `resultados/ranking_*.csv` |
| `paso4_medir_tiempos.py` | Mide los tiempos en ms → `resultados/tiempos_*.csv` y gráficos |
| `paso5_top15.py` | Compara el top 15 de los 3 algoritmos → `resultados/top15_comparacion.csv` |
| `main.py` | Ejecuta todos los pasos en orden |
