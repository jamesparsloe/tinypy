x: bool = True
y: int = 42

y = y + 10

# print("x = " + x)
# print("y = " + y)

if x:

    print("I'm the truthy branch!")
    print("Hello!")
    print(x)
    y = y + 10
    # was flaky on newlines


else:

    # unreachable
    print("I'm the else branch")

print("y = " + y)
