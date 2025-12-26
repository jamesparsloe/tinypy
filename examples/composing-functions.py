def add(a: int, b: int) -> int:
    return a + b


def mul(a: int, b: int) -> int:
    return a * b


def main() -> None:
    a: int = 10
    b: int = 20

    c: int = add(a, b)
    d: int = mul(3, c)

    print(d)


main()
