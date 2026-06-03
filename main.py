import random
import matplotlib.pyplot as plt

data_points = []

for i in range(500):
    x = random.uniform(0, 100)
    y = random.uniform(0, 100)
    data_points.append((x, y))

print("So diem du lieu:", len(data_points))


class CANNode:
    def __init__(self, node_id, xmin, xmax, ymin, ymax):
        self.node_id = node_id
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax

    def __str__(self):
        return (
            f"Node {self.node_id}: "
            f"({self.xmin:.1f}, {self.ymin:.1f}) -> "
            f"({self.xmax:.1f}, {self.ymax:.1f})"
        )


def split_zone(node, node_id):

    width = node.xmax - node.xmin
    height = node.ymax - node.ymin

    if width >= height:

        mid = (node.xmin + node.xmax) / 2

        joined_node = CANNode(
            node_id,
            mid,
            node.xmax,
            node.ymin,
            node.ymax
        )

        node.xmax = mid

    else:

        mid = (node.ymin + node.ymax) / 2

        joined_node = CANNode(
            node_id,
            node.xmin,
            node.xmax,
            mid,
            node.ymax
        )

        node.ymax = mid

    return joined_node


network_nodes = []

network_nodes.append(
    CANNode(1, 0, 100, 0, 100)
)

for i in range(2, 5):

    selected_node = random.choice(network_nodes)

    joined_node = split_zone(
        selected_node,
        i
    )

    network_nodes.append(joined_node)

print("\nDanh sach node:\n")

for node in network_nodes:
    print(node)

fig, ax = plt.subplots()

for node in network_nodes:

    width = node.xmax - node.xmin
    height = node.ymax - node.ymin

    rectangle = plt.Rectangle(
        (node.xmin, node.ymin),
        width,
        height,
        fill=False
    )

    ax.add_patch(rectangle)

    ax.text(
        node.xmin + width / 2,
        node.ymin + height / 2,
        f"N{node.node_id}",
        ha="center"
    )

ax.set_xlim(0, 100)
ax.set_ylim(0, 100)

ax.set_title("CAN 2D Overlay Network")

plt.show()