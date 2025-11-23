## Binary Trees 内存基准

这一套示例统一实现了 [binary-trees](https://benchmarksgame-team.pages.debian.net/benchmarksgame/description/binarytrees.html) 基准：\
每个程序都会根据参数 `maxDepth`：

1. 构造一棵短命的 “stretch tree” 并立即丢弃；
2. 保留一棵长寿的 `longLivedTree`；
3. 针对 `minDepth=4` 到 `maxDepth`（步长为 2）的所有深度，批量构造 `2^(maxDepth-depth+minDepth)` 棵满二叉树并遍历；
4. 打印每轮的 `itemCheck` 结果作为正确性校验。

这个模式与真实高负载业务——例如 Web 请求、Kafka 消费、流式计算、游戏服等 “不断创建/销毁短命对象并伴随少量长命对象”——的内存压力非常接近，因此可用来比较 Go、Java、Node.js、Python、Rust 的分配与 GC 行为。

目录结构：

- `go/main.go`（Go modules：`go/go.mod`）
- `java/BinaryTrees.java`
- `nodejs/main.js`（依赖由 `nodejs/package.json` 管理）
- `python/main.py`（Python 依赖位于 `python/requirements.txt`）
- `rust/src/main.rs`（Cargo 管理）

### 依赖

- Go 1.25+
- Java 21+
- Node.js 18+
- Python 3.9+
- Rust 1.74+（需要 Cargo）

首次克隆仓库后，可运行以下脚本安装所有语言的依赖（Python 包、npm 模块、Go/Cargo 缓存）：

```bash
cd concurrency-memory-bench
python3 scripts/bootstrap_env.py
```


### 一键批量运行

`scripts/run_benchmarks.py` 会：

1. 预先构建 Go 与 Rust 的二进制；
2. 编译 Java 示例；
3. 对每个指定的 `maxDepth` 依次运行各语言实现；
4. 使用 `scripts/measure_memory.py` 记录峰值 RSS，运行期间会直接透传各语言程序的 stdout/stderr，最后只输出内存表格。

示例：

```bash
cd concurrency-memory-bench
python3 scripts/run_benchmarks.py --depths 10 16
```

输出：

```
语言      | 树深度 | 峰值 RSS (MB)
---------+-----+--------------
Go       | 10  | 5.66
Java     | 10  | 44.42
Node.js  | 10  | 42.64
Python   | 10  | 7.53
Rust     | 10  | 1.42
Go       | 16  | 17.73
Java     | 16  | 343.58
Node.js  | 16  | 85.80
Python   | 16  | 19.66
Rust     | 16  | 8.17
```

参数说明：

- `--depths`（默认 `10 16`）控制要跑的 `maxDepth` 列表。
- `--python` 可指定另一套 Python 解释器来运行脚本。

### 单独运行示例

各语言都接受一个可选的 `maxDepth` 参数，默认 5。

#### Go

```bash
cd concurrency-memory-bench/go
GOCACHE=$PWD/.gocache go build -o binarytrees main.go
./binarytrees 16
```

#### Java

```bash
cd concurrency-memory-bench/java
javac BinaryTrees.java
java BinaryTrees 16
```

#### Node.js

```bash
cd concurrency-memory-bench/nodejs
node main.js 16
```

#### Python

```bash
cd concurrency-memory-bench/python
python3 main.py 16
```

#### Rust

```bash
cd concurrency-memory-bench/rust
source "$HOME/.cargo/env"
cargo run --release -- 16
```

### 内存测量脚本

`scripts/measure_memory.py` 负责执行命令并在进程退出后打印峰值 RSS（来自 `ru_maxrss`），可独立使用：

```bash
python3 scripts/measure_memory.py --cwd go -- ./binarytrees 16
python3 scripts/measure_memory.py --cwd java --quiet-child --json -- java BinaryTrees 16
```

可选参数：

- `--quiet-child`：静默子进程 stdout/stderr。
- `--json`：直接打印 JSON，便于脚本处理。
- `--json-file`：把 JSON 结果写入指定文件，适合在显示子进程输出时使用。

### 探索方向

- 调整 `--depths` 以观察更大/更小树的内存占用变化。
- 对单个语言运行 `perf`, `pprof`, `jcmd VM.native_memory` 等工具，深入剖析不同阶段的内存组成。
- 将 `minDepth`、`iterations`、节点结构等参数改造为贴近自己业务的数据结构，测试自定义场景。*** End Patch*** End Patch
