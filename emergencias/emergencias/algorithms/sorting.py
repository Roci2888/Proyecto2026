import time
import copy

# ─── MergeSort ────────────────────────────────────────────────────

def merge_sort(arr: list, key=lambda x: x, reverse: bool = False) -> list:
    """
    Algoritmo MergeSort — divide y conquista.
    Precondición : arr debe ser una lista
    Postcondición: retorna nueva lista ordenada
    Complejidad  : O(n log n) siempre
    Espacio      : O(n)
    """
    if len(arr) <= 1:
        return arr

    mid   = len(arr) // 2
    left  = merge_sort(arr[:mid], key, reverse)
    right = merge_sort(arr[mid:], key, reverse)

    return _merge(left, right, key, reverse)

def _merge(left: list, right: list, key, reverse: bool) -> list:
    """Combina dos listas ordenadas. Complejidad: O(n)"""
    result = []
    i = j  = 0

    while i < len(left) and j < len(right):
        left_val  = key(left[i])
        right_val = key(right[j])

        if (left_val <= right_val) if not reverse else (left_val >= right_val):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result

# ─── QuickSort ────────────────────────────────────────────────────

def quick_sort(arr: list, key=lambda x: x, reverse: bool = False) -> list:
    """
    Algoritmo QuickSort — divide y conquista con pivote.
    Precondición : arr debe ser una lista
    Postcondición: retorna nueva lista ordenada
    Complejidad  : O(n log n) promedio, O(n²) peor caso
    Espacio      : O(log n)
    """
    if len(arr) <= 1:
        return arr

    pivot  = key(arr[len(arr) // 2])
    left   = [x for x in arr if key(x) < pivot]
    middle = [x for x in arr if key(x) == pivot]
    right  = [x for x in arr if key(x) > pivot]

    if not reverse:
        return quick_sort(left, key) + middle + quick_sort(right, key)
    else:
        return quick_sort(right, key, True) + middle + quick_sort(left, key, True)

# ─── Reportes ordenados ───────────────────────────────────────────

def sort_by_timestamp(incidents: list, algorithm: str = "merge") -> list:
    """
    Ordena incidentes por tiempo — más antiguos primero.
    Complejidad: O(n log n)
    """
    key = lambda x: x.timestamp
    if algorithm == "merge":
        return merge_sort(incidents, key=key)
    return quick_sort(incidents, key=key)

def sort_by_priority(incidents: list, algorithm: str = "merge") -> list:
    """
    Ordena incidentes por prioridad — más críticos primero.
    Complejidad: O(n log n)
    """
    key = lambda x: x.prioridad
    if algorithm == "merge":
        return merge_sort(incidents, key=key, reverse=True)
    return quick_sort(incidents, key=key, reverse=True)

def sort_by_zone(incidents: list, algorithm: str = "merge") -> list:
    """
    Agrupa y ordena zonas por frecuencia de incidentes.
    Complejidad: O(n log n)
    """
    # Contar incidentes por zona
    freq = {}
    for inc in incidents:
        freq[inc.ubicacion] = freq.get(inc.ubicacion, 0) + 1

    # Ordenar zonas por frecuencia
    zones = [{"zona": z, "cantidad": c} for z, c in freq.items()]
    key   = lambda x: x["cantidad"]

    if algorithm == "merge":
        return merge_sort(zones, key=key, reverse=True)
    return quick_sort(zones, key=key, reverse=True)

# ─── Benchmark ────────────────────────────────────────────────────

def benchmark(incidents: list, key=lambda x: x.prioridad) -> dict:
    """
    Compara el rendimiento de MergeSort vs QuickSort.
    Precondición : incidents debe tener al menos 1 elemento
    Postcondición: retorna tiempos de ejecución de ambos algoritmos
    Complejidad  : O(n log n)
    """
    arr1 = copy.deepcopy(incidents)
    arr2 = copy.deepcopy(incidents)

    # Medir MergeSort
    t0      = time.perf_counter()
    merge_sort(arr1, key=key)
    t_merge = time.perf_counter() - t0

    # Medir QuickSort
    t0      = time.perf_counter()
    quick_sort(arr2, key=key)
    t_quick = time.perf_counter() - t0

    return {
        "n"            : len(incidents),
        "merge_sort_s" : round(t_merge, 6),
        "quick_sort_s" : round(t_quick, 6),
        "ganador"      : "MergeSort" if t_merge < t_quick else "QuickSort"
    }