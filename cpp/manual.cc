#include <iostream>
#include <string>

constexpr int MIN_DEPTH = 4;

class Node
{
public:
    Node *left;
    Node *right;

    Node(Node *l, Node *r)
        : left(l), right(r) {}

    ~Node()
    {
        delete left;
        delete right;
    }

    int itemCheck() const
    {
        if (left == nullptr)
        {
            return 1;
        }
        return 1 + left->itemCheck() + right->itemCheck();
    }
};

Node *bottomUpTree(int depth)
{
    if (depth <= 0)
    {
        return new Node(nullptr, nullptr);
    }
    return new Node(
        bottomUpTree(depth - 1),
        bottomUpTree(depth - 1));
}

int main(int argc, char *argv[])
{
    int maxDepth = 5;
    if (argc > 1)
    {
        maxDepth = std::stoi(argv[1]);
    }

    if (MIN_DEPTH + 2 > maxDepth)
    {
        maxDepth = MIN_DEPTH + 2;
    }

    int stretchDepth = maxDepth + 1;

    Node *stretchTree = bottomUpTree(stretchDepth);
    int check = stretchTree->itemCheck();
    std::cout << "stretch tree of depth " << stretchDepth
              << "\t check: " << check << std::endl;
    delete stretchTree;

    Node *longLivedTree = bottomUpTree(maxDepth);

    for (int depth = MIN_DEPTH; depth <= maxDepth; depth += 2)
    {
        int iterations = 1 << (maxDepth - depth + MIN_DEPTH);
        check = 0;

        for (int i = 0; i < iterations; i++)
        {
            Node *tree = bottomUpTree(depth);
            check += tree->itemCheck();
            delete tree;
        }

        std::cout << iterations << "\t trees of depth " << depth
                  << "\t check: " << check << std::endl;
    }

    std::cout << "long lived tree of depth " << maxDepth
              << "\t check: " << longLivedTree->itemCheck() << std::endl;

    delete longLivedTree;
}
