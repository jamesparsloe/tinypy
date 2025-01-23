import sys
from tinypy.parser import parse
from tinypy.interpreter import interpret


__version__ = "0.1.0"
USAGE = "usage: tinypy or tinypy script.py"


def run(source: str):
    interpret(source)


def run_repl():
    print(f"tinypy {__version__}")
    while True:
        try:
            source = input(">>> ")
            run(source)
        except EOFError:
            print()
            break


def run_script(file: str):
    with open(file, "r") as f:
        source = f.read()

    run(source)


def main() -> None:
    args = sys.argv[1:]

    # TODO correct error codes
    if len(args) == 0:
        run_repl()
    elif len(args) == 1:
        if args[0] in ("-v", "--version"):
            print(f"tinypy {__version__}")
        elif args[0] in ("-h", "--help"):
            print(USAGE)
        else:
            run_script(args[0])
    else:
        print(USAGE)
