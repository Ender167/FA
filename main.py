
class Node:
    def __init__(self, key):
        self.key = key
        self.next = None

    def __str__(self):
        return str(self.key)


class HashTable:
    def __init__(self, capacity):
        self.capacity = capacity
        self.size = 0
        self.table = [None] * capacity

    def _hash(self, key):
        return hash(key) % self.capacity

    def add(self, key):
        index = self._hash(key)

        if self.table[index] is None:
            self.table[index] = Node(key)
            #self.size += 1
        else:
            current = self.table[index]
            while current:
                if current.key == key:
                    return
                current = current.next
            new_node = Node(key)
            new_node.next = self.table[index]
            self.table[index] = new_node
            #self.size += 1

        self.size += 1

        loadFactor = self.computeLoadFactor()
        #print("Load factor is:" + str(loadFactor))

        if loadFactor > 0.75:
            #print("Calling rehash function, load factor=" + str(loadFactor) + ", element " + str(key))
            self.rehash()

    def lookup(self, key):
        index = self._hash(key)

        current = self.table[index]
        while current:
            if current.key == key:
                return True
            current = current.next

        return False

    def rehash(self):
        #rehashes the hash table by doubling the capacity and
        #calling the hash function again for each element

        self.capacity = self.capacity * 2

        copyNodes = []

        for el in self.table:
            current = el
            while current:
                copyNodes.append(current.key)
                current = current.next

        self.table.clear()
        self.table = [None] * self.capacity

        for el in copyNodes:
            self.add(el)


    def computeLoadFactor(self):
        #returns the current load factor of the hash table
        if self.size > 0:
            return self.size / self.capacity
        return 0

    def __len__(self):
        return self.size

    def __contains__(self, key):
        try:
            self.lookup(key)
            return True
        except KeyError:
            return False


if __name__ == '__main__':
    ht = HashTable(100)

    #adding over 100 elements in the symbol table
    ht.add("a")
    ht.add("b")
    ht.add("c")
    ht.add("d")
    ht.add("e")
    ht.add("f")
    ht.add("g")
    ht.add("h")
    ht.add("i")
    ht.add("j")

    for i in range(0, 100):
        ht.add(i)

    #print the resulting symbol table
    for el in ht.table:
        current = el
        print(current, end=" ")
        while current:
            current = current.next
            print(current)
        print("\n")


    print("Is i in the symbol table? " + str(ht.lookup("i")))
    print("Is 50 in the symbol table? " + str(ht.lookup(50)))
    print("Is 102 in the symbol table? " + str(ht.lookup(102)))

