public class BinaryTrees {

    private static final int MIN_DEPTH = 4;

    private static class Node {
        private final Node left;
        private final Node right;

        Node(Node left, Node right) {
            this.left = left;
            this.right = right;
        }

        int itemCheck() {
            if (left == null) {
                return 1;
            }
            return 1 + left.itemCheck() + right.itemCheck();
        }
    }

    private static Node bottomUpTree(int depth) {
        if (depth <= 0) {
            return new Node(null, null);
        }
        return new Node(bottomUpTree(depth - 1), bottomUpTree(depth - 1));
    }

    public static void main(String[] args) {
        int maxDepth = 5;
        if (args.length > 0) {
            maxDepth = Integer.parseInt(args[0]);
        }

        if (MIN_DEPTH + 2 > maxDepth) {
            maxDepth = MIN_DEPTH + 2;
        }
        int stretchDepth = maxDepth + 1;

        int check = bottomUpTree(stretchDepth).itemCheck();
        System.out.printf("stretch tree of depth %d\t check: %d%n", stretchDepth, check);

        Node longLivedTree = bottomUpTree(maxDepth);

        for (int depth = MIN_DEPTH; depth <= maxDepth; depth += 2) {
            int iterations = 1 << (maxDepth - depth + MIN_DEPTH);
            check = 0;

            for (int i = 0; i < iterations; i++) {
                check += bottomUpTree(depth).itemCheck();
            }

            System.out.printf("%d\t trees of depth %d\t check: %d%n", iterations, depth, check);
        }

        System.out.printf("long lived tree of depth %d\t check: %d%n", maxDepth, longLivedTree.itemCheck());
    }
}
