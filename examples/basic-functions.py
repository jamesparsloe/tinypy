x: int = 10
y: int = 42

x = x + 10

z: int = 50


def foo() -> int:
    return 42


def bar(a: int) -> int:
    return a + 42


def square(b: int) -> int:
    return b * b


def foo1() -> int:
    return 42


print(foo())
print(bar(10))


print("z")
print(z)

print("z squared")
print(square(z))

print(foo())
print(foo1())

# z: int = foo()

# print(y)
# print(z)
