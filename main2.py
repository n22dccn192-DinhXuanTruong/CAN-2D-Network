import random
import matplotlib.pyplot as plt

# =========================
# DATASET
# =========================
data_points = [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(500)]


# =========================
# NODE CLASS
# =========================
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

    def area(self):
        return (self.xmax - self.xmin) * (self.ymax - self.ymin)

    def __str__(self):
        return f"Node {self.node_id}: ({self.xmin:.1f},{self.ymin:.1f}) -> ({self.xmax:.1f},{self.ymax:.1f})"


# =========================
# SPLIT ZONE (STABLE CAN)
# =========================
def split_zone(node, node_id, axis):

    if axis == 0:
        mid = (node.xmin + node.xmax) / 2

        new_node = CANNode(
            node_id,
            mid,
            node.xmax,
            node.ymin,
            node.ymax
        )

        node.xmax = mid

    else:
        mid = (node.ymin + node.ymax) / 2

        new_node = CANNode(
            node_id,
            node.xmin,
            node.xmax,
            mid,
            node.ymax
        )

        node.ymax = mid

    return new_node


# =========================
# BUILD NETWORK (FIXED)
# =========================
network_nodes = []
network_nodes.append(CANNode(1, 0, 100, 0, 100))

for i in range(2, 11):

    # luôn chọn node lớn nhất để split (FIX LỆCH DATA)
    selected = max(network_nodes, key=lambda n: n.area())

    axis = i % 2  # xen kẽ X/Y

    new_node = split_zone(selected, i, axis)
    network_nodes.append(new_node)


# =========================
# NEIGHBORS
# =========================
def build_neighbors(nodes):
    for i in range(len(nodes)):
        nodes[i].neighbors = []

        for j in range(len(nodes)):
            if i == j:
                continue

            a = nodes[i]
            b = nodes[j]

            if not (a.xmax < b.xmin or a.xmin > b.xmax or a.ymax < b.ymin or a.ymin > b.ymax):
                nodes[i].neighbors.append(b.node_id)


build_neighbors(network_nodes)


# =========================
# ROUTING
# =========================
def find_node(x, y):

    steps = 0
    current = network_nodes[0]

    while True:
        steps += 1

        if current.contains(x, y):
            return current, steps

        best = current
        best_dist = abs((current.xmin + current.xmax)/2 - x) + abs((current.ymin + current.ymax)/2 - y)

        for node in network_nodes:
            cx = (node.xmin + node.xmax) / 2
            cy = (node.ymin + node.ymax) / 2

            dist = abs(cx - x) + abs(cy - y)

            if dist < best_dist:
                best_dist = dist
                best = node

        if best == current:
            return current, steps

        current = best


# =========================
# TEST ROUTING
# =========================
tx, ty = random.uniform(0, 100), random.uniform(0, 100)

owner, steps = find_node(tx, ty)

print("\nKET QUA ROUTING")
print("-------------------")
print(f"Toa do: ({tx:.2f}, {ty:.2f})")
print(f"Node: {owner.node_id}")
print(f"Steps: {steps}")


# =========================
# AVERAGE STEPS
# =========================
total = 0

for _ in range(100):
    x, y = random.uniform(0, 100), random.uniform(0, 100)
    _, s = find_node(x, y)
    total += s

print("\nTHONG KE")
print("-------------------")
print("Average Routing Steps =", round(total / 100, 2))


# =========================
# DATA DISTRIBUTION
# =========================
print("\nPHAN BO DU LIEU")
print("-------------------")

for node in network_nodes:
    cnt = sum(1 for x, y in data_points if node.contains(x, y))
    print(f"Node {node.node_id}: {cnt} diem")


# =========================
# VISUALIZATION
# =========================
fig, ax = plt.subplots()

for node in network_nodes:
    w = node.xmax - node.xmin
    h = node.ymax - node.ymin

    ax.add_patch(plt.Rectangle((node.xmin, node.ymin), w, h, fill=False))
    ax.text(node.xmin + w/2, node.ymin + h/2, f"N{node.node_id}", ha="center")

for x, y in data_points:
    ax.plot(x, y, ".", markersize=2)

ax.plot(tx, ty, "ro", markersize=6)

ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.set_title("CAN 2D (Balanced Version)")

plt.show()