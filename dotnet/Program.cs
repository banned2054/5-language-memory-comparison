public class BinaryTrees
{
    private const int MinDepth = 4;

    private class Node(Node? left, Node? right)
    {
        public int ItemCheck()
        {
            if (left == null)
            {
                return 1;
            }

            return 1 + left.ItemCheck() + right.ItemCheck();
        }
    }

    private static Node BottomUpTree(int depth)
    {
        return depth <= 0 ? new Node(null, null) : new Node(BottomUpTree(depth - 1), BottomUpTree(depth - 1));
    }

    public static void Main(string[] args)
    {
        var maxDepth = 5;
        if (args.Length > 0)
        {
            maxDepth = int.Parse(args[0]);
        }

        if (MinDepth + 2 > maxDepth)
        {
            maxDepth = MinDepth + 2;
        }

        var stretchDepth = maxDepth + 1;

        var check = BottomUpTree(stretchDepth).ItemCheck();
        Console.WriteLine($"stretch tree of depth {stretchDepth}\t check: {check}");

        var longLivedTree = BottomUpTree(maxDepth);

        for (var depth = MinDepth; depth <= maxDepth; depth += 2)
        {
            var iterations = 1 << (maxDepth - depth + MinDepth);
            check = 0;

            for (var i = 0; i < iterations; i++)
            {
                check += BottomUpTree(depth).ItemCheck();
            }

            Console.WriteLine($"{iterations}\t trees of depth {depth}\t check: {check}");
        }

        Console.WriteLine($"long lived tree of depth {maxDepth}\t check: {longLivedTree.ItemCheck()}");
    }
}
