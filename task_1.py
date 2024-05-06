class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(self.size)]

    def hash_function(self, key):
        return hash(key) % self.size

    def insert(self, key, value):
        key_hash = self.hash_function(key)
        key_value = [key, value]

        if self.table[key_hash] is None:
            self.table[key_hash] = list([key_value])
            return True
        else:
            for pair in self.table[key_hash]:
                if pair[0] == key:
                    pair[1] = value
                    return True
            self.table[key_hash].append(key_value)
            return True

    def get(self, key):
        key_hash = self.hash_function(key)
        if self.table[key_hash] is not None:
            for pair in self.table[key_hash]:
                if pair[0] == key:
                    return pair[1]
        return None
    def delete(self, key):
        key_hash = self.hash_function(key)
        if len(self.table[key_hash]) > 0:
            index = 0
            for key_val, val in self.table[key_hash]:
                if key_val == key:
                    self.table[key_hash].pop(index)
                    return True
                index += 1
            return False
        else:
            return False
    
    def __str__(self):
        out = ""
        for item in self.table:
            if len(item) != 0:
               for key,val in item:
                    out += f"{key}  {val}" + "\n"
        return out


# Тестуємо нашу хеш-таблицю:
H = None
H = HashTable(5)
H.insert("apple", 10)
H.insert("orange", 20)
H.insert("banana", 30)
print("Initial table:")
print(H)
print("Table after deletion of 'apple':")
H.delete("apple")
print(H)

