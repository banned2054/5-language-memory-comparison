#include <iostream>
#include <memory>
#include <string>

constexpr int MIN_DEPTH = 4;

struct Node
{
    std::unique_ptr<Node> left;
    std::unique_ptr<Node> right;

    Node(std::unique_ptr<Node> l, std::unique_ptr<Node> r)
        : left(std::move(l)), right(std::move(r)) {}

    int itemCheck() const
    {
        if (!left)
            return 1;
        return 1 + left->itemCheck() + right->itemCheck();
    }
};

std::unique_ptr<Node> bottomUpTree(int depth)
{
    if (depth <= 0)
        return std::make_unique<Node>(nullptr, nullptr);
    return std::make_unique<Node>(
        bottomUpTree(depth - 1),
        bottomUpTree(depth - 1));
}

int main(int argc, char *argv[])
{
    int maxDepth = argc > 1 ? std::stoi(argv[1]) : 5;
    if (MIN_DEPTH + 2 > maxDepth)
        maxDepth = MIN_DEPTH + 2;

    int stretchDepth = maxDepth + 1;

    {
        auto stretch = bottomUpTree(stretchDepth);
        std::cout << "stretch tree of depth " << stretchDepth
                  << "\t check: " << stretch->itemCheck() << "\n";
    }

    auto longLived = bottomUpTree(maxDepth);

    for (int depth = MIN_DEPTH; depth <= maxDepth; depth += 2)
    {
        int iterations = 1 << (maxDepth - depth + MIN_DEPTH);
        int check = 0;

        for (int i = 0; i < iterations; i++)
            check += bottomUpTree(depth)->itemCheck();

        std::cout << iterations << "\t trees of depth " << depth
                  << "\t check: " << check << "\n";
    }

    std::cout << "long lived tree of depth " << maxDepth
              << "\t check: " << longLived->itemCheck() << "\n";
}
