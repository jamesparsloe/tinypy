# Test modulo and floor division operators

x: int = 17
y: int = 5

# Modulo operator
remainder: int = x % y
print(remainder)

# Floor division
quotient: int = x // y
print(quotient)

# Check: quotient * divisor + remainder = dividend
check: int = quotient * y + remainder
print(check)

# Works with floats too
a: float = 7.5
b: float = 2.0
print(a // b)
print(a % b)
