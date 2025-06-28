## Task 1: Maximum‑Flow in a Logistics Network  
**Goal:** Maximize delivery from terminals → warehouses → stores.  
**Graph:**  
- **Nodes:** S (source), T1 & T2 (terminals), W1–W4 (warehouses), M1–M14 (stores), T (sink)  
- **Edges & capacities:**  
  - S→T1, S→T2: ∞  
  - T1→W1: 25, T1→W2: 20, T1→W3: 15  
  - T2→W2: 10, T2→W3: 15, T2→W4: 30  
  - W1→M1: 15, W1→M2: 10, W1→M3: 20  
  - W2→M4: 15, W2→M5: 10, W2→M6: 25  
  - W3→M7: 20, W3→M8: 15, W3→M9: 10  
  - W4→M10: 20, W4→M11: 10, W4→M12: 15, W4→M13: 5, W4→M14: 10  
  - M*→T: ∞  
**Algorithm:** Edmonds–Karp (BFS for shortest augmenting path; update residual capacities until no augmenting path).  
**Deliverables:**  
- Total max‑flow value  
- Table of flows T1→Mi and T2→Mi (including zeros)  
- Analysis: which terminal ships most; key bottlenecks; under‑served stores and capacity‐upgrade suggestions; network improvements.

---

## Task 2: Range‑Query Performance — OOBTree vs. dict  
**Goal:** Compare 100 price‐range queries on a large product set.  
**Data:** `generated_items_data.csv` with columns `ID`, `Name`, `Category`, `Price`.  
**Structures:**  
- **dict:** key = ID → item  
- **OOBTree:** key = Price → list of items  
**Insertion:** add items to both structures.  
**Queries:**  
- `range_query_dict`: linear scan of `d.values()` filtering by `low ≤ Price ≤ high`  
- `range_query_tree`: slice `tree.items(min=low, max=high)` and concatenate lists  
**Benchmark:** generate 100 random `[low, high]` between min/max price; measure total time with `timeit`:  
