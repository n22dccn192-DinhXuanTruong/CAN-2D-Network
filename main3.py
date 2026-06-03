import random
import matplotlib.pyplot as plt

random.seed(42)
data_points = [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(500)]


class CANNode:
    def __init__(self, node_id, xmin, xmax, ymin, ymax):
        self.node_id = node_id
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.neighbors = []

    def contains(self, x, y):
        return self.xmin <= x <= self.xmax and self.ymin <= y <= self.ymax

    def center(self):
        cx = (self.xmin + self.xmax) / 2
        cy = (self.ymin + self.ymax) / 2
        return cx, cy

    def area(self):
        return (self.xmax - self.xmin) * (self.ymax - self.ymin)

    def __str__(self):
        return f"Node {self.node_id}: ({self.xmin:.1f},{self.ymin:.1f}) -> ({self.xmax:.1f},{self.ymax:.1f})"


def get_node(nodes, nid):
    for n in nodes:
        if n.node_id == nid:
            return n
    return None


def split_zone(node, new_id, axis):
    if axis == 0:
        mid = (node.xmin + node.xmax) / 2
        new_node = CANNode(new_id, mid, node.xmax, node.ymin, node.ymax)
        node.xmax = mid
    else:
        mid = (node.ymin + node.ymax) / 2
        new_node = CANNode(new_id, node.xmin, node.xmax, mid, node.ymax)
        node.ymax = mid
    return new_node


def build_neighbors(nodes):
    for n in nodes:
        n.neighbors = []
    for i in range(len(nodes)):
        for j in range(len(nodes)):
            if i == j:
                continue
            a = nodes[i]
            b = nodes[j]
            x_touch = abs(a.xmax - b.xmin) < 1e-9 or abs(b.xmax - a.xmin) < 1e-9
            y_touch = abs(a.ymax - b.ymin) < 1e-9 or abs(b.ymax - a.ymin) < 1e-9
            x_overlap = a.xmin < b.xmax - 1e-9 and a.xmax > b.xmin + 1e-9
            y_overlap = a.ymin < b.ymax - 1e-9 and a.ymax > b.ymin + 1e-9
            if (x_touch and y_overlap) or (y_touch and x_overlap):
                nodes[i].neighbors.append(b.node_id)


def route(nodes, x, y):
    steps = 0
    current = nodes[0]
    visited = set()

    while True:
        steps += 1
        visited.add(current.node_id)

        if current.contains(x, y):
            return current, steps

        cx, cy = current.center()
        best = current
        best_dist = abs(cx - x) + abs(cy - y)

        for nid in current.neighbors:
            nb = get_node(nodes, nid)
            if nb is None or nb.node_id in visited:
                continue
            nx, ny = nb.center()
            d = abs(nx - x) + abs(ny - y)
            if d < best_dist:
                best_dist = d
                best = nb

        if best.node_id == current.node_id:
            return current, steps

        current = best


network = [CANNode(1, 0, 100, 0, 100)]
split_log = []

for i in range(2, 11):
    target = max(network, key=lambda n: n.area())
    axis = i % 2
    new_node = split_zone(target, i, axis)
    network.append(new_node)
    build_neighbors(network)
    split_log.append((i, str(target), str(new_node)))

build_neighbors(network)

print("KET QUA ROUTING")
print("-------------------")
tx, ty = random.uniform(0, 100), random.uniform(0, 100)
owner, steps = route(network, tx, ty)
print(f"Toa do tim: ({tx:.2f}, {ty:.2f})")
print(f"Node so huu: {owner.node_id}")
print(f"So buoc routing: {steps}")

print("\nTHONG KE")
print("-------------------")
total = 0
for _ in range(100):
    x, y = random.uniform(0, 100), random.uniform(0, 100)
    _, s = route(network, x, y)
    total += s
print("Average Routing Steps =", round(total / 100, 2))

print("\nPHAN BO DU LIEU")
print("-------------------")
for node in network:
    cnt = sum(1 for x, y in data_points if node.contains(x, y))
    print(f"  {node}  =>  {cnt} diem")

print("\nLICH SU SPLIT")
print("-------------------")
for step, old, new in split_log:
    print(f"  Node {step} join: {old}  |  moi: {new}")

fig, axes = plt.subplots(2, 5, figsize=(16, 7))
axes = axes.flatten()

tmp = [CANNode(1, 0, 100, 0, 100)]
build_neighbors(tmp)

for idx, ax in enumerate(axes):
    if idx > 0:
        step_i = split_log[idx - 1][0]
        sel = max(tmp, key=lambda n: n.area())
        ax_dir = step_i % 2
        nn = split_zone(sel, step_i, ax_dir)
        tmp.append(nn)
        build_neighbors(tmp)

    for node in tmp:
        w = node.xmax - node.xmin
        h = node.ymax - node.ymin
        rect = plt.Rectangle((node.xmin, node.ymin), w, h,
                              linewidth=1.2, edgecolor="black", facecolor="white")
        ax.add_patch(rect)
        ax.text(node.xmin + w/2, node.ymin + h/2, f"N{node.node_id}",
                ha="center", va="center", fontsize=8)

    for x, y in data_points:
        ax.plot(x, y, ".", markersize=1.2, color="black", alpha=0.3)

    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_xticks([])
    ax.set_yticks([])
    if idx == 0:
        ax.set_title("Node 1 (ban dau)", fontsize=8)
    else:
        ax.set_title(f"Node {split_log[idx-1][0]} join", fontsize=8)

plt.suptitle("CAN 2D - Qua trinh split zone", fontsize=12)
plt.tight_layout()

fig2, ax2 = plt.subplots(figsize=(7, 7))
for node in network:
    w = node.xmax - node.xmin
    h = node.ymax - node.ymin
    rect = plt.Rectangle((node.xmin, node.ymin), w, h,
                          linewidth=1.5, edgecolor="black", facecolor="white")
    ax2.add_patch(rect)
    ax2.text(node.xmin + w/2, node.ymin + h/2, f"N{node.node_id}",
             ha="center", va="center", fontsize=9)

for x, y in data_points:
    ax2.plot(x, y, ".", markersize=2, color="black", alpha=0.4)

ax2.plot(tx, ty, "ko", markersize=8, label=f"Query ({tx:.1f}, {ty:.1f})")
ax2.legend()
ax2.set_xlim(0, 100)
ax2.set_ylim(0, 100)
ax2.set_title("CAN 2D - Trang thai cuoi (10 nodes)")
ax2.set_xlabel("Price (x)")
ax2.set_ylabel("Rating (y)")

plt.tight_layout()
plt.show()