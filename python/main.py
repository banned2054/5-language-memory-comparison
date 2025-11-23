import sys


class Node:
    __slots__ = ("left", "right")

    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

    def item_check(self):
        if self.left is None:
            return 1
        return 1 + self.left.item_check() + self.right.item_check()


def bottom_up_tree(depth: int) -> Node:
    if depth <= 0:
        return Node()
    return Node(bottom_up_tree(depth - 1), bottom_up_tree(depth - 1))


MIN_DEPTH = 4


def main(max_depth: int) -> None:
    if MIN_DEPTH + 2 > max_depth:
        max_depth = MIN_DEPTH + 2
    stretch_depth = max_depth + 1

    check = bottom_up_tree(stretch_depth).item_check()
    print(f"stretch tree of depth {stretch_depth}\t check: {check}")

    long_lived_tree = bottom_up_tree(max_depth)

    for depth in range(MIN_DEPTH, max_depth + 1, 2):
        iterations = 1 << (max_depth - depth + MIN_DEPTH)
        check = 0

        for _ in range(iterations):
            check += bottom_up_tree(depth).item_check()

        print(f"{iterations}\t trees of depth {depth}\t check: {check}")

    print(
        f"long lived tree of depth {max_depth}\t check: {long_lived_tree.item_check()}"
    )


if __name__ == "__main__":
    if len(sys.argv) > 1:
        max_depth = int(sys.argv[1])
    else:
        max_depth = 5

    main(max_depth)
