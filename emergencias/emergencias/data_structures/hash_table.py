from models.incident import Incident

class HashTable:
    """
    ADT HashTable: tabla hash propia con encadenamiento separado.
    Almacena incidentes y soporta inserción, búsqueda,
    actualización y eliminación.

    NO usa dict de Python internamente.

    Atributos:
        capacity (int)  : número de buckets
        buckets  (list) : lista de listas (encadenamiento)
        size     (int)  : cantidad de incidentes almacenados
        collisions(int) : total de colisiones registradas

    Complejidades:
        insert  : O(1) promedio, O(n) peor caso
        search  : O(1) promedio, O(n) peor caso
        delete  : O(1) promedio, O(n) peor caso
        update  : O(1) promedio, O(n) peor caso
    """

    def __init__(self, capacity: int = 101):
        """
        Precondición : capacity debe ser un número primo positivo
        Postcondición: tabla inicializada con buckets vacíos
        Complejidad  : O(n) donde n = capacity
        """
        if capacity <= 0:
            raise ValueError("La capacidad debe ser mayor a 0")
        self.capacity   = capacity
        self.buckets    = [[] for _ in range(capacity)]
        self.size       = 0
        self.collisions = 0

    # ─── Función Hash ─────────────────────────────────────────────

    def _hash(self, key: str) -> int:
        """
        Función hash djb2.
        Precondición : key debe ser string no vacío
        Complejidad  : O(k) donde k = largo del key
        """
        if not key:
            raise ValueError("La key no puede estar vacía")
        h = 5381
        for c in key:
            h = ((h << 5) + h) + ord(c)
        return h % self.capacity

    # ─── Operaciones principales ──────────────────────────────────

    def insert(self, incident: Incident) -> None:
        """
        Inserta un incidente en la tabla.
        Si el ID ya existe, lo actualiza.
        Precondición : incident debe ser instancia de Incident
        Postcondición: incidente queda almacenado en su bucket
        Complejidad  : O(1) promedio
        """
        idx    = self._hash(incident.id)
        bucket = self.buckets[idx]

        # Registrar colisión si el bucket no está vacío
        if bucket:
            self.collisions += 1

        # Si ya existe el ID, actualizar
        for i, item in enumerate(bucket):
            if item.id == incident.id:
                bucket[i] = incident
                return

        bucket.append(incident)
        self.size += 1

        # Rehash si el factor de carga supera 0.75
        if self.load_factor() > 0.75:
            self._rehash()

    def search(self, id: str) -> Incident:
        """
        Busca un incidente por ID.
        Precondición : id debe ser string no vacío
        Postcondición: retorna el incidente o None si no existe
        Complejidad  : O(1) promedio
        """
        idx = self._hash(id)
        for item in self.buckets[idx]:
            if item.id == id:
                return item
        return None

    def delete(self, id: str) -> bool:
        """
        Elimina un incidente por ID.
        Precondición : id debe existir en la tabla
        Postcondición: incidente eliminado, size decrementado
        Complejidad  : O(1) promedio
        """
        idx    = self._hash(id)
        bucket = self.buckets[idx]
        for i, item in enumerate(bucket):
            if item.id == id:
                bucket.pop(i)
                self.size -= 1
                return True
        return False

    def update_state(self, id: str, nuevo_estado: str) -> bool:
        """
        Actualiza el estado de un incidente.
        Precondición : id debe existir, estado debe ser válido
        Postcondición: estado del incidente actualizado
        Complejidad  : O(1) promedio
        """
        incident = self.search(id)
        if incident:
            incident.actualizar_estado(nuevo_estado)
            return True
        return False

    # ─── Métricas ─────────────────────────────────────────────────

    def load_factor(self) -> float:
        """
        Calcula el factor de carga.
        factor_carga = size / capacity
        Complejidad: O(1)
        """
        return self.size / self.capacity

    def get_stats(self) -> dict:
        """
        Retorna métricas de la tabla hash.
        Complejidad: O(n) donde n = capacity
        """
        used_buckets = sum(1 for b in self.buckets if b)
        max_bucket   = max(len(b) for b in self.buckets)
        return {
            "size"              : self.size,
            "capacity"          : self.capacity,
            "factor_carga"      : round(self.load_factor(), 4),
            "colisiones"        : self.collisions,
            "buckets_utilizados": used_buckets,
            "max_bucket_size"   : max_bucket
        }

    # ─── Rehash ───────────────────────────────────────────────────

    def _rehash(self) -> None:
        """
        Duplica la capacidad y reinserta todos los elementos.
        Se activa cuando factor_carga > 0.75
        Complejidad: O(n)
        """
        old_buckets   = self.buckets
        self.capacity = self.capacity * 2 + 1
        self.buckets  = [[] for _ in range(self.capacity)]
        self.size     = 0
        self.collisions = 0

        for bucket in old_buckets:
            for item in bucket:
                self.insert(item)

    # ─── Iteración ────────────────────────────────────────────────

    def get_all(self) -> list:
        """
        Retorna todos los incidentes almacenados.
        Complejidad: O(n)
        """
        result = []
        for bucket in self.buckets:
            for item in bucket:
                result.append(item)
        return result

    def __repr__(self):
        return (f"HashTable(size={self.size}, "
                f"capacity={self.capacity}, "
                f"load_factor={self.load_factor():.4f})")