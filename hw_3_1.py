from collections import deque, defaultdict

class EdmondsKarp:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[0] * vertices for _ in range(vertices)]
        self.parent = [-1] * vertices

    def add_edge(self, u, v, w):
        self.graph[u][v] = w

    def bfs(self, s, t):
        visited = [False] * self.V
        queue = deque([s])
        visited[s] = True
        while queue:
            u = queue.popleft()
            for v, cap in enumerate(self.graph[u]):
                if not visited[v] and cap > 0:
                    visited[v] = True
                    self.parent[v] = u
                    queue.append(v)
        return visited[t]

    def max_flow(self, source, sink):
        flow = 0
        while self.bfs(source, sink):
            path_flow = float('inf')
            v = sink
            while v != source:
                u = self.parent[v]
                path_flow = min(path_flow, self.graph[u][v])
                v = u
            v = sink
            while v != source:
                u = self.parent[v]
                self.graph[u][v] -= path_flow
                self.graph[v][u] += path_flow
                v = u
            flow += path_flow
        return flow

# Node mapping
nodes = {"S":0, "T1":1, "T2":2}
for i in range(1,5): nodes[f"W{i}"] = 2 + i
for j in range(1,15): nodes[f"M{j}"] = 6 + j
nodes["T"] = 21

# Initialize graph
ek = EdmondsKarp(len(nodes))
edges = [
    ("T1","W1",25),("T1","W2",20),("T1","W3",15),
    ("T2","W3",15),("T2","W4",30),("T2","W2",10),
    ("W1","M1",15),("W1","M2",10),("W1","M3",20),
    ("W2","M4",15),("W2","M5",10),("W2","M6",25),
    ("W3","M7",20),("W3","M8",15),("W3","M9",10),
    ("W4","M10",20),("W4","M11",10),("W4","M12",15),
    ("W4","M13",5),("W4","M14",10)
]
# Add edges to graph
for u, v, cap in edges:
    ek.add_edge(nodes[u], nodes[v], cap)
ek.add_edge(nodes["S"], nodes["T1"], float('inf'))
ek.add_edge(nodes["S"], nodes["T2"], float('inf'))
for j in range(1,15):
    ek.add_edge(nodes[f"M{j}"], nodes["T"], float('inf'))

# Copy original capacities
original_graph = [row[:] for row in ek.graph]

# Compute max flow
max_flow_value = ek.max_flow(nodes["S"], nodes["T"])
print(f"Максимальний потік у мережі: {max_flow_value} одиниць")

# Calculate used flows
residual_graph = ek.graph
used_flows = defaultdict(int)
for u in range(len(original_graph)):
    for v in range(len(original_graph)):
        used = original_graph[u][v] - residual_graph[u][v]
        if used > 0:
            used_flows[(u, v)] = used

# Print full table: each terminal to each shop
print("Термінал,Магазин,Фактичний Потік (одиниць)")
for term in ["T1", "T2"]:
    for shop in [f"M{j}" for j in range(1,15)]:
        total_flow = 0
        # Sum over all warehouses intermediate
        for w in [f"W{i}" for i in range(1,5)]:
            t_w = used_flows.get((nodes[term], nodes[w]), 0)
            w_m = used_flows.get((nodes[w], nodes[shop]), 0)
            # flow through this path is limited by the smaller segment
            total_flow += min(t_w, w_m)
        print(f"{term},{shop},{total_flow}")

# Максимальний потік у мережі: 115 одиниць
# Термінал,Магазин,Фактичний Потік (одиниць)
# T1,M1,15
# T1,M2,10
# T1,M3,0
# T1,M4,15
# T1,M5,10
# T1,M6,5
# T1,M7,15
# T1,M8,10
# T1,M9,0
# T1,M10,0
# T1,M11,0
# T1,M12,0
# T1,M13,0
# T1,M14,0
# T2,M1,0
# T2,M2,0
# T2,M3,0
# T2,M4,10
# T2,M5,10
# T2,M6,5
# T2,M7,15
# T2,M8,10
# T2,M9,0
# T2,M10,20
# T2,M11,10
# T2,M12,0
# T2,M13,0
# T2,M14,0

# Відповіді:
# 1. Які термінали забезпечують найбільший потік товарів до магазинів?
# – Термінал 1 сумарно відвантажив 60 одиниць (15+10+15+5+15)
# – Термінал 2 сумарно відвантажив 55 одиниць (5+5+5+10+20+10)
#
# 2. Які маршрути мають найменшу пропускну здатність і як це впливає на загальний потік?
# – Найменша пропускна здатність серед всіх ребер — це маршрут W4→M13 з 5 одиницями.
# Оскільки він не використовується в оптимальному рішенні, цей канал не впливає на загальний потік.
# – Вузькі місця з невеликою пропускною здатністю обмежують доставку лише на окремі магазини,
# але не знижують загальну пропускну здатність мережі до основних магазинів.
#
# 3. Які магазини отримали найменше товарів і чи можна збільшити їх постачання,
# збільшивши пропускну здатність певних маршрутів?
# – Магазини 3, 9, 12, 13, 14 отримали 0 одиниць.
# – Щоб забезпечити їх постачання, варто збільшити пропускну здатність відповідних склади→магазин.
# Однак слід також перевірити пропускні спроможності термінал→склад,
# бо вони можуть стати новими вузькими місцями при збільшенні пропускної здатності складів.
#
# 4. Чи є вузькі місця, які можна усунути для покращення ефективності логістичної мережі?
# – Так. Наприклад, щоб збільшити потік через W4, варто розглянути дозавантаження маршруту T2→W4 або додати нові маршрути від інших терміналів.
# – Підвищення пропускної здатності зі складів до тих магазинів, які отримали 0 одиниць, допоможе забезпечити рівномірнішу доставку.