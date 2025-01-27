x: bool = False

print("x = " + x)


if x:
    print("I'm the truthy branch!")
else:
    print("I'm the else branch")

y: bool = True

print("y = " + y)

if y:
    print("Hello, this is y")

print(x)


if x:
    print("Unreachable")
else:
    if y:
        print("Nested!")
