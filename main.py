import paso1_extraer_abstracts
import paso2_frecuencias
import paso3_ordenar
import paso4_medir_tiempos
import paso5_top15


def main():
    print("=== Paso 1: extraer los abstracts de los PDF ===")
    paso1_extraer_abstracts.main()

    print("\n=== Paso 2: contar la frecuencia de cada término ===")
    paso2_frecuencias.main()

    print("\n=== Paso 3: ordenar con Counting Sort, Radix Sort y Bucket Sort ===")
    paso3_ordenar.main()

    print("\n=== Paso 4: medir los tiempos de ejecución ===")
    paso4_medir_tiempos.main()

    print("\n=== Paso 5: validación con el top 15 de cada algoritmo ===")
    paso5_top15.main()


if __name__ == "__main__":
    main()
