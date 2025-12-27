# Test exponentiation operator

print(2 ** 3)
print(2 ** 10)
print(3.0 ** 2.0)

# Right-associative: 2 ** 3 ** 2 = 2 ** 9 = 512
print(2 ** 3 ** 2)

# Precedence: -2 ** 2 = -(2 ** 2) = -4
print(-2 ** 2)

# Power function using recursion
def power(base: int, exp: int) -> int:
    if exp == 0:
        return 1
    else:
        return base * power(base, exp - 1)

print(power(2, 10))
