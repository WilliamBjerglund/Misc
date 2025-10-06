"""
A very basic HashTable implementation with dynamic scaling using multiplication method
"""


import math


class HashTable:
    def __init__(self, size=8):
        self.table = [None] * size
        self.count = 0
        self.max_load = 0.7
        self.min_load = 0.2

    def _hash(self, key):
        """My own hash function using knuths multiplicative method"""
        key_str = str(key).encode('utf-8')
        knuth_const = int(2654435769)
        hash_value = 0
        for byte in key_str:
            hash_value = (hash_value * knuth_const + byte) & 0xFFFFFFFF # 0xFFFFFFFF = limit of 32 bit uint
        return hash_value

    def _find(self, key):
        table_size = len(self.table)
        hash_value = self._hash(key)
        index = hash_value % table_size
        # Linear probing
        for _ in range(table_size):
            if self.table[index] is None:
                return index, False
            elif self.table[index] != "TOMBSTONE" and self.table[index][0] == key:
                return index, True
            index = (index + 1) % table_size
        return index, False

    def _resize(self, new_size):
        old_table = self.table
        self.table = [None] * new_size
        self.count = 0
        # Rehash all existing items to new table
        for item in old_table:
            if item and item != "TOMBSTONE":
                index, _ = self._find(item[0])
                self.table[index] = item
                self.count += 1

    def insert(self, key, value):
        if (self.count + 1) / len(self.table) > self.max_load:
            self._resize(len(self.table) * 2)
        # If load factor is too low, shrink the table
        index, found = self._find(key)
        self.table[index] = (key, value)
        if not found:
            self.count += 1

    def get(self, key):
        index, found = self._find(key)
        return self.table[index][1] if found else None
    
    def delete(self, key):
        index, found = self._find(key)
        if found:
            self.table[index] = "TOMBSTONE"
            self.count -= 1
            if len(self.table) > 8 and self.count / len(self.table) < self.min_load:
                self._resize(len(self.table) // 2)
            return True
        return False
    

    # Python Magic
    def __len__(self):
        "Allows len(hash_table) to return number of items"
        return self.count
    
    def __setitem__(self, key, value):
        """Allows us to use different syntax than hash_table.insert(key, value)"""
        self.insert(key, value)
    
    def __getitem__(self, key):
        """Again syntax switch"""
        value = self.get(key)
        if value is None:
            raise KeyError(key)  # Raise error if key doesn't exist (like real dict)
        return value

    def __delitem__(self, key):
        """Syntax switch"""
        if not self.delete(key):
            raise KeyError(key)
        
