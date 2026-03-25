import math

DELETED = ("__DELETED__", None)

class HashMap:
    def __init__(self, size=300001):  # Large size
        self.size = size
        self.count = 0
        self.table = [None] * self.size

        # Stats
        self.insert_probes = 0
        self.search_probes = 0
        self.insert_ops = 0
        self.search_ops = 0
        self.collisions = 0

    # Hash Functions
    def _hash1(self, key):
        return hash(key) % self.size

    def _hash2(self, key):
        return 1 + (hash(key) % (self.size - 1))

    # Insert function to add a key, value pair into the HashMap
    def insert(self, key, value):
        index = self._hash1(key)
        step = self._hash2(key)

        probes = 0

        while self.table[index] is not None and self.table[index] != DELETED:
            if self.table[index][0] == key:
                self.table[index] = (key, value)
                return

            index = (index + step) % self.size
            probes += 1
            self.collisions += 1

        self.table[index] = (key, value)
        self.count += 1

        self.insert_probes += probes
        self.insert_ops += 1

        if self.load_factor() > 0.7:
            self._resize()

    # Searches for a value via a key
    def search(self, key):
        index = self._hash1(key)
        step = self._hash2(key)

        probes = 0

        while self.table[index] is not None:
            if self.table[index] != DELETED and self.table[index][0] == key:
                self.search_probes += probes
                self.search_ops += 1
                return self.table[index][1]

            index = (index + step) % self.size
            probes += 1

        self.search_probes += probes
        self.search_ops += 1
        return None

    # Calculates the load factor
    def load_factor(self):
        return self.count / self.size

    # Resizes the HashMap
    def _resize(self):
        old_table = self.table
        self.size *= 2
        self.table = [None] * self.size
        self.count = 0

        for item in old_table:
            if item and item != DELETED:
                self.insert(item[0], item[1])

    # Stats function = Gets Load Factor, Number of Collisions, and Average Probes for Inserting and Searching
    def get_stats(self):
        return {
            "load_factor": self.load_factor(),
            "avg_insert_probes": self.insert_probes / max(1, self.insert_ops),
            "avg_search_probes": self.search_probes / max(1, self.search_ops),
            "collisions": self.collisions
        }