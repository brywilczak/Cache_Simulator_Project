import random
import matplotlib.pyplot as plt

class Cache:
    def __init__(self, size, associativity, block_size, replacement_policy):
        self.size = size
        self.associativity = associativity
        self.block_size = block_size
        self.replacement_policy = replacement_policy
        self.num_sets = size // (associativity * block_size)
        self.cache = [[None] * associativity for _ in range(self.num_sets)]
        self.accesses = 0
        self.hits = 0
        self.hit_rate_history = []

        # For LRU replacement policy
        if self.replacement_policy == "LRU":
            self.access_counter = [[0] * associativity for _ in range(self.num_sets)]

        # For FIFO replacement policy
        if self.replacement_policy == "FIFO":
            self.fifo_queue = [[] for _ in range(self.num_sets)]

    def read(self, address):
        self.accesses += 1
        tag, index = self._extract_tag_and_index(address)
        for i in range(self.associativity):
            if self.cache[index][i] == tag:
                self.hits += 1
                self.hit_rate_history.append(self.get_hit_rate())
                if self.replacement_policy == "LRU":
                    self.access_counter[index][i] = max(self.access_counter[index]) + 1
                return True
        self._replace_block(tag, index)
        self.hit_rate_history.append(self.get_hit_rate())
        return False

    def _replace_block(self, tag, index):
        if None in self.cache[index]:
            empty_slot = self.cache[index].index(None)
            self.cache[index][empty_slot] = tag
            if self.replacement_policy == "LRU":
                self.access_counter[index][empty_slot] = max(self.access_counter[index]) + 1
            if self.replacement_policy == "FIFO":
                self.fifo_queue[index].append(empty_slot)
        else:
            if self.replacement_policy == "LRU":
                min_counter_index = self.access_counter[index].index(min(self.access_counter[index]))
                self.cache[index][min_counter_index] = tag
                self.access_counter[index][min_counter_index] = max(self.access_counter[index]) + 1
            if self.replacement_policy == "FIFO":
                fifo_index = self.fifo_queue[index].pop(0)
                self.cache[index][fifo_index] = tag
                self.fifo_queue[index].append(fifo_index)

    def _extract_tag_and_index(self, address):
        offset_bits = self._log2(self.block_size)
        index_bits = self._log2(self.num_sets)
        tag = address >> (offset_bits + index_bits)
        index_mask = (1 << index_bits) - 1
        index = (address >> offset_bits) & index_mask
        return tag, index

    def _log2(self, x):
        return x.bit_length() - 1 if x > 0 else 0

    def get_hit_rate(self):
        return self.hits / self.accesses if self.accesses > 0 else 0

    def get_miss_rate(self):
        return 1 - self.get_hit_rate()


# Test cases
def basic_cache_configuration_test():
    cache = Cache(size=16384, associativity=1, block_size=64, replacement_policy="LRU")
    memory_access_patterns = [0, 64, 128, 64, 192, 256, 320, 64]
    for address in memory_access_patterns:
        cache.read(address)
    print("Basic Cache Configuration Test:")
    print("Cache Hits:", cache.hits)
    print("Cache Misses:", cache.accesses - cache.hits)
    print("Hit Rate:", cache.get_hit_rate())
    print("Miss Rate:", cache.get_miss_rate())

def cache_associativity_test():
    cache = Cache(size=16384, associativity=4, block_size=64, replacement_policy="LRU")
    memory_access_patterns = [0, 64, 128, 192, 256, 320, 384, 448]
    for address in memory_access_patterns:
        cache.read(address)
    print("Cache Associativity Test:")
    print("Cache Hits:", cache.hits)
    print("Cache Misses:", cache.accesses - cache.hits)
    print("Hit Rate:", cache.get_hit_rate())
    print("Miss Rate:", cache.get_miss_rate())

def cache_replacement_policy_test():
    cache = Cache(size=8192, associativity=1, block_size=64, replacement_policy="FIFO")
    memory_access_patterns = [0, 64, 128, 192, 256, 320, 384, 448, 512, 576]
    for address in memory_access_patterns:
        cache.read(address)
    print("Cache Replacement Policy Test:")
    print("Cache Hits:", cache.hits)
    print("Cache Misses:", cache.accesses - cache.hits)
    print("Hit Rate:", cache.get_hit_rate())
    print("Miss Rate:", cache.get_miss_rate())

def visualize_cache_behavior(cache):
    plt.plot(range(1, cache.accesses + 1), cache.hit_rate_history, marker='o')
    plt.title("Cache Hit Rate Over Time")
    plt.xlabel("Accesses")
    plt.ylabel("Hit Rate")
    plt.show()

# Run test cases
basic_cache_configuration_test()
cache_associativity_test()
cache_replacement_policy_test()

# Visualize cache behavior
cache = Cache(size=16384, associativity=1, block_size=64, replacement_policy="LRU")
memory_access_patterns = [0, 64, 128, 64, 192, 256, 320, 64]
for address in memory_access_patterns:
    cache.read(address)
visualize_cache_behavior(cache)
