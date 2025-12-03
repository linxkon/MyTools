"""Command-line typing practice tool based on tab-delimited vocabulary files.

Features
--------
* Load terms from a ``<term>\t<meaning>`` text file while ignoring blank lines and comments.
* Offer ordered or random practice modes.
* Automatically repeat incorrect answers when ``--repeat-wrong`` is set.
* Track per-question timing to report average speed and accuracy at the end of a session.

Usage
-----
python Data_tools/typing_practice.py --data data.txt --mode random --repeat-wrong
"""

import argparse
import random
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List


@dataclass
class Entry:
    term: str
    meaning: str


@dataclass
class PracticeResult:
    total: int
    correct: int
    incorrect: int
    total_time: float

    @property
    def accuracy(self) -> float:
        return (self.correct / self.total * 100) if self.total else 0.0

    @property
    def average_speed(self) -> float:
        return (self.total_time / self.total) if self.total else 0.0


def load_entries(path: Path) -> List[Entry]:
    """Load entries from a tab-delimited file.

    Lines starting with ``#`` and blank lines are ignored.
    """
    entries: List[Entry] = []
    with path.open("r", encoding="utf-8") as fh:
        for line_no, raw_line in enumerate(fh, start=1):
            line = raw_line.rstrip("\n")
            if not line or line.lstrip().startswith("#"):
                continue

            if "\t" not in line:
                raise ValueError(
                    f"Line {line_no} in {path} is missing a tab delimiter: {line!r}"
                )

            term, meaning = line.split("\t", maxsplit=1)
            entries.append(Entry(term=term.strip(), meaning=meaning.strip()))

    if not entries:
        raise ValueError(f"No valid entries found in {path}")

    return entries


def iter_round(entries: Iterable[Entry], shuffle: bool) -> Iterable[Entry]:
    items = list(entries)
    if shuffle:
        random.shuffle(items)
    return items


def practice(entries: List[Entry], shuffle: bool, cycles: int, repeat_wrong: bool) -> PracticeResult:
    total = 0
    correct = 0
    total_time = 0.0

    remaining: List[Entry] = []
    for cycle in range(1, cycles + 1):
        remaining.extend(iter_round(entries, shuffle))
        if shuffle:
            random.shuffle(remaining)

        while remaining:
            entry = remaining.pop(0)
            print(f"\n解释：{entry.meaning}")
            start = time.perf_counter()
            try:
                user_input = input("请输入对应内容： ").strip()
            except EOFError:
                print("\n接收到 EOF，结束练习。")
                return PracticeResult(total=total, correct=correct, incorrect=total - correct, total_time=total_time)
            except KeyboardInterrupt:
                print("\n练习被中断。")
                return PracticeResult(total=total, correct=correct, incorrect=total - correct, total_time=total_time)

            elapsed = time.perf_counter() - start
            total += 1
            total_time += elapsed

            if user_input == entry.term:
                correct += 1
                print("✔ 正确！")
            else:
                print(f"✘ 错误。正确答案： {entry.term}")
                if repeat_wrong:
                    remaining.append(entry)

    incorrect = total - correct
    return PracticeResult(total=total, correct=correct, incorrect=incorrect, total_time=total_time)


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="键盘打字练习工具")
    parser.add_argument(
        "--data",
        type=Path,
        default=Path(__file__).with_name("typing_sample.txt"),
        help="词库文件路径，格式为 <term>\\t<meaning>",
    )
    parser.add_argument(
        "--mode",
        choices=["ordered", "random"],
        default="ordered",
        help="练习顺序：ordered 按照文件顺序，random 随机排序",
    )
    parser.add_argument(
        "--cycles",
        type=int,
        default=1,
        help="循环练习的轮数（不含错题重练）",
    )
    parser.add_argument(
        "--repeat-wrong",
        action="store_true",
        help="是否将错题加入队列直至答对",
    )
    return parser.parse_args(argv)


def main(argv: List[str]) -> int:
    args = parse_args(argv)

    try:
        entries = load_entries(args.data)
    except Exception as exc:  # pragma: no cover - CLI feedback
        print(f"加载词库失败: {exc}", file=sys.stderr)
        return 1

    print(
        "开始练习： {count} 条，模式：{mode}，循环：{cycles} 轮，错题重练：{repeat}".format(
            count=len(entries),
            mode="随机" if args.mode == "random" else "顺序",
            cycles=args.cycles,
            repeat="开启" if args.repeat_wrong else "关闭",
        )
    )

    result = practice(
        entries=entries,
        shuffle=args.mode == "random",
        cycles=max(args.cycles, 1),
        repeat_wrong=args.repeat_wrong,
    )

    print("\n练习结束：")
    print(f"总题数：{result.total}")
    print(f"正确：{result.correct}")
    print(f"错误：{result.incorrect}")
    print(f"准确率：{result.accuracy:.2f}%")
    print(f"平均速度：{result.average_speed:.2f} 秒/题")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
