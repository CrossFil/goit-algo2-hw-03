import csv
import random
import timeit
import os
from BTrees.OOBTree import OOBTree

def load_items(filename):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(base_dir, filename)
    items = []
    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row['Price'] = float(row['Price'])
            row['ID'] = int(row['ID'])
            items.append(row)
    return items

def add_item_to_dict(d, item):
    d[item['ID']] = item


def add_item_to_trees(tree_by_id, tree_by_price, item):
    # Index by ID
    tree_by_id[item['ID']] = item
    # Index by Price: append to list
    price = item['Price']
    if price in tree_by_price:
        tree_by_price[price].append(item)
    else:
        tree_by_price[price] = [item]

# Range query implementations

def range_query_dict(d, low, high):
    return [item for item in d.values() if low <= item['Price'] <= high]


def range_query_tree(tree_by_price, low, high):
    # Use OOBTree slicing by price key
    items = []
    for price, items_list in tree_by_price.items(min=low, max=high):
        items.extend(items_list)
    return items

# Benchmark setup
def benchmark_structures(filename, num_queries=100):
    items = load_items(filename)

    # Prepare data structures: dict and two OOBTrees (by ID and by Price)
    d = {}
    tree_by_id = OOBTree()
    tree_by_price = OOBTree()
    for item in items:
        add_item_to_dict(d, item)
        add_item_to_trees(tree_by_id, tree_by_price, item)

    # Prepare random price ranges
    prices = [item['Price'] for item in items]
    min_price, max_price = min(prices), max(prices)
    ranges = [(random.uniform(min_price, max_price), random.uniform(min_price, max_price)) for _ in range(num_queries)]
    ranges = [(min(a, b), max(a, b)) for a, b in ranges]

    # Globals for timeit
    globals_dict = {
        'd': d,
        'tree_by_price': tree_by_price,
        'ranges': ranges,
        'range_query_dict': range_query_dict,
        'range_query_tree': range_query_tree
    }

    # Execute benchmarks
    time_dict = timeit.timeit('for low, high in ranges: range_query_dict(d, low, high)', globals=globals_dict, number=1)
    time_tree = timeit.timeit('for low, high in ranges: range_query_tree(tree_by_price, low, high)', globals=globals_dict, number=1)

    print(f"Total range_query time for OOBTree (by Price index): {time_tree:.6f} seconds")
    print(f"Total range_query time for Dict: {time_dict:.6f} seconds")

if __name__ == '__main__':
    benchmark_structures('generated_items_data.csv')

# Total range_query time for OOBTree (by Price index): 0.573440 seconds
# Total range_query time for Dict: 0.751095 seconds