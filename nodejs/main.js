class Node {
  constructor(left = null, right = null) {
    this.left = left;
    this.right = right;
  }

  itemCheck() {
    if (this.left === null) {
      return 1;
    }
    return 1 + this.left.itemCheck() + this.right.itemCheck();
  }
}

function bottomUpTree(depth) {
  if (depth <= 0) {
    return new Node();
  }
  return new Node(bottomUpTree(depth - 1), bottomUpTree(depth - 1));
}

const MIN_DEPTH = 4;

function main() {
  let maxDepth = parseInt(process.argv[2], 10);
  if (Number.isNaN(maxDepth)) {
    maxDepth = 5;
  }

  if (MIN_DEPTH + 2 > maxDepth) {
    maxDepth = MIN_DEPTH + 2;
  }
  const stretchDepth = maxDepth + 1;

  let check = bottomUpTree(stretchDepth).itemCheck();
  console.log(`stretch tree of depth ${stretchDepth}\t check: ${check}`);

  const longLivedTree = bottomUpTree(maxDepth);

  for (let depth = MIN_DEPTH; depth <= maxDepth; depth += 2) {
    const iterations = 1 << (maxDepth - depth + MIN_DEPTH);
    check = 0;

    for (let i = 0; i < iterations; i += 1) {
      check += bottomUpTree(depth).itemCheck();
    }

    console.log(`${iterations}\t trees of depth ${depth}\t check: ${check}`);
  }

  console.log(
    `long lived tree of depth ${maxDepth}\t check: ${longLivedTree.itemCheck()}`,
  );
}

main();
