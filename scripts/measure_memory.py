import argparse
import json
import resource
import subprocess
import sys
import time
from typing import Any, Dict, Optional


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="运行指定命令并打印其峰值 RSS（基于 ru_maxrss）。"
    )
    parser.add_argument(
        "--cwd",
        help="执行目标命令的工作目录。",
    )
    parser.add_argument(
        "--quiet-child",
        action="store_true",
        help="测量时静默子进程的标准输出/错误。",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="以 JSON 形式输出测量结果，方便脚本解析。",
    )
    parser.add_argument(
        "--json-file",
        help="将测量结果写入指定文件（JSON 格式）。",
    )
    parser.add_argument(
        "cmd",
        nargs=argparse.REMAINDER,
        help="需要运行的命令（若包含 -- 请使用 `-- <cmd>` 的方式传入）。",
    )
    args = parser.parse_args()
    if not args.cmd:
        parser.error("请提供需要运行的命令。")
    if args.cmd[0] == "--":
        args.cmd = args.cmd[1:]
    return args


def run_and_measure(
    cmd: list[str],
    cwd: Optional[str] = None,
    suppress_output: bool = False,
    env: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    stdout = subprocess.DEVNULL if suppress_output else None
    stderr = subprocess.DEVNULL if suppress_output else None

    try:
        proc = subprocess.Popen(cmd, cwd=cwd, stdout=stdout, stderr=stderr, env=env)
    except FileNotFoundError as exc:
        return {
            "exit_code": 127,
            "peak_kb": 0.0,
            "peak_mb": 0.0,
            "elapsed": 0.0,
            "error": str(exc),
        }

    start = time.time()
    ret = proc.wait()
    end = time.time()

    usage = resource.getrusage(resource.RUSAGE_CHILDREN)
    raw_max = float(usage.ru_maxrss or 0.0)
    if sys.platform == "darwin":
        peak_kb = raw_max / 1024.0
    else:
        peak_kb = raw_max

    elapsed = end - start
    return {
        "exit_code": ret,
        "peak_kb": peak_kb,
        "peak_mb": peak_kb / 1024.0 if peak_kb else 0.0,
        "elapsed": elapsed,
    }


def main() -> int:
    args = parse_args()
    result = run_and_measure(
        args.cmd,
        cwd=args.cwd,
        suppress_output=args.quiet_child,
    )

    serialized = json.dumps(result)

    if args.json:
        print(serialized)
    else:
        print(f"Peak RSS: {result['peak_kb']:.0f} KB ({result['peak_mb']:.2f} MB)")

    if args.json_file:
        with open(args.json_file, "w", encoding="utf-8") as fh:
            fh.write(serialized)

    return int(result["exit_code"])


if __name__ == "__main__":
    raise SystemExit(main())
