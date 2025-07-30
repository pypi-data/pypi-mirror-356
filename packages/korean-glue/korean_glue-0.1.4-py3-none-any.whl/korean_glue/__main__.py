import argparse
import re
from .engine import attach

EXAMPLES = [
    "kglue '철수(은/는)'",
    "kglue 'K(이/가)'",
    "kglue '3(을/를)'",
]

PATTERN = re.compile(r"(.+)\(([^()]+)\)")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="kglue",
        description="Attach Korean josa",
    )
    parser.add_argument("expression", nargs="?", help="WORD(PATTERN)")
    args = parser.parse_args(argv)

    if not args.expression:
        parser.print_usage()
        example_text = "\n".join(f"  {ex}" for ex in EXAMPLES)
        print("\nExamples:\n" + example_text)
        return

    match = PATTERN.fullmatch(args.expression)
    if not match:
        parser.error("expression must be in WORD(PATTERN) format")
    word, pattern = match.groups()
    print(attach(word, pattern))


if __name__ == "__main__":
    main()
