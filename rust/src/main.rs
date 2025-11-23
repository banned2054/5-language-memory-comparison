use std::env;

const MIN_DEPTH: i32 = 4;

#[derive(Default)]
struct Node {
    left: Option<Box<Node>>,
    right: Option<Box<Node>>,
}

impl Node {
    fn bottom_up_tree(depth: i32) -> Box<Node> {
        if depth <= 0 {
            Box::new(Node {
                left: None,
                right: None,
            })
        } else {
            let left = Node::bottom_up_tree(depth - 1);
            let right = Node::bottom_up_tree(depth - 1);
            Box::new(Node {
                left: Some(left),
                right: Some(right),
            })
        }
    }

    fn item_check(&self) -> i32 {
        if let Some(left) = &self.left {
            1 + left.item_check() + self.right.as_ref().unwrap().item_check()
        } else {
            1
        }
    }
}

fn parse_target() -> i32 {
    env::args()
        .nth(1)
        .and_then(|value| value.parse::<i32>().ok())
        .unwrap_or(5)
}

fn main() {
    let mut max_depth = parse_target();
    if MIN_DEPTH + 2 > max_depth {
        max_depth = MIN_DEPTH + 2;
    }
    let stretch_depth = max_depth + 1;

    let check = Node::bottom_up_tree(stretch_depth).item_check();
    println!("stretch tree of depth {}\t check: {}", stretch_depth, check);

    let long_lived_tree = Node::bottom_up_tree(max_depth);

    let mut depth = MIN_DEPTH;
    while depth <= max_depth {
        let iterations = 1 << (max_depth - depth + MIN_DEPTH);
        let mut check = 0;

        for _ in 0..iterations {
            check += Node::bottom_up_tree(depth).item_check();
        }

        println!(
            "{}\t trees of depth {}\t check: {}",
            iterations, depth, check
        );

        depth += 2;
    }

    println!(
        "long lived tree of depth {}\t check: {}",
        max_depth,
        long_lived_tree.item_check()
    );
}
