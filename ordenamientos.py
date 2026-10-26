# Algoritmos de ordenamiento no basados en comparaciones.
# Ordenan una lista de pares (termino, frecuencia) de mayor a menor frecuencia.


def counting_sort(pares):
    if not pares:
        return []
    k = max(f for _, f in pares)

    # contar cuantos terminos hay con cada frecuencia
    conteo = [0] * (k + 1)
    for _, f in pares:
        conteo[f] += 1

    # posicion donde empieza cada frecuencia en la salida, de k a 0 para que quede descendente
    inicio = [0] * (k + 1)
    posicion = 0
    for f in range(k, -1, -1):
        inicio[f] = posicion
        posicion += conteo[f]

    # se ubica cada termino recorriendo en el orden original, asi es estable
    salida = [None] * len(pares)
    for par in pares:
        f = par[1]
        salida[inicio[f]] = par
        inicio[f] += 1
    return salida


def radix_sort(pares, base=10):
    if not pares:
        return []
    k = max(f for _, f in pares)

    resultado = list(pares)
    exp = 1
    # una pasada por cada digito de k, empezando por las unidades
    while k // exp > 0:
        cajas = [[] for _ in range(base)]
        for par in resultado:
            digito = (par[1] // exp) % base
            cajas[digito].append(par)
        # se recogen de la caja 9 a la 0 para que quede descendente
        resultado = [par for d in range(base - 1, -1, -1) for par in cajas[d]]
        exp *= base
    return resultado


def insercion_descendente(caja):
    for j in range(1, len(caja)):
        actual = caja[j]
        i = j - 1
        # solo se corren los de menor frecuencia, asi los empates no cambian de orden
        while i >= 0 and caja[i][1] < actual[1]:
            caja[i + 1] = caja[i]
            i -= 1
        caja[i + 1] = actual


def bucket_sort(pares):
    n = len(pares)
    if n == 0:
        return []
    k = max(f for _, f in pares)

    # n cajas, la caja de cada termino se calcula con su frecuencia
    cajas = [[] for _ in range(n)]
    for par in pares:
        cajas[par[1] * n // (k + 1)].append(par)

    for caja in cajas:
        insercion_descendente(caja)

    # se juntan de la ultima caja a la primera
    return [par for caja in reversed(cajas) for par in caja]


ALGORITMOS = {
    "Counting Sort": counting_sort,
    "Radix Sort": radix_sort,
    "Bucket Sort": bucket_sort,
}
