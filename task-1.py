import random
import time
from lru import LRUCache

def make_queries(n, q, hot_pool=30, p_hot=0.95, p_update=0.03):
    hot = [(random.randint(0, n//2), random.randint(n//2, n-1))
           for _ in range(hot_pool)]
    queries = []
    for _ in range(q):
        if random.random() < p_update:        # ~3% запитів — Update
            idx = random.randint(0, n-1)
            val = random.randint(1, 100)
            queries.append(("Update", idx, val))
        else:                                 # ~97% — Range
            if random.random() < p_hot:       # 95% — «гарячі» діапазони
                left, right = random.choice(hot)
            else:                             # 5% — випадкові діапазони
                left = random.randint(0, n-1)
                right = random.randint(left, n-1)
            queries.append(("Range", left, right))
    return queries

def range_sum_no_cache(array: list[int], left: int, right: int) -> int:
    sum = 0
    for i in range(left, right + 1):
       sum += array[i]
    return sum

def update_no_cache(array: list[int], index: int, value: int) -> None | IndexError:
    if 0 <= index < len(array):
        array[index] = value
    return None

def range_sum_with_cache(array: list[int], left: int, right: int):
    global cache
    key = (left, right)
    cached_value = cache.get(key)
    if cached_value != -1:
        return cached_value
    
    sum = 0
    for i in range(left, right + 1):
        sum += array[i]

    cache.put(key, sum)
    return sum

def update_with_cache(array: list[int], index: int, value: int):
    global cache

    if 0 <= index < len(array):
        array[index] = value
        for (left, right) in cache.cache:
            if left <= index <= right:
                cache.remove((left, right))
                return None
    return None


def no_cache_time_count():
    start_time = time.perf_counter()

    for command in commands_list:
        if command[0] == "Range":
            range_sum_no_cache(array, command[1], command[2])
        else:
            update_no_cache(array, command[1], command[2])

    execution_time = time.perf_counter() - start_time
    return execution_time

def with_cache_time_count():
    start_time = time.perf_counter()
    for command in commands_list:
        if command[0] == "Range":
            range_sum_with_cache(array, command[1], command[2])
        else:
            update_with_cache(array, command[1], command[2])

    execution_time = time.perf_counter() - start_time
    return execution_time


if __name__ == "__main__":
    n = 100_000
    q = 50_000

    array = [random.randint(1, 100) for _ in range(n)]
    commands_list = make_queries(n, q)
    cache = LRUCache(1000)

    t1 = no_cache_time_count()
    t2 = with_cache_time_count()

    print(f"Без кешу : {t1:.2f} c")
    print(f"LRU-кеш  : {t2:.2f} c  (прискорення ×{t1/t2:.2f})")