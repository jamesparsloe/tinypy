x: bool = True

print(x == True)
print(x != True)

# Test not operator
y: bool = not x
print("not x")
print(y)

# Test and operator
a: bool = True
b: bool = False
print("True and False")
print(a and b)
print("True and True")
print(True and True)

# Test or operator
print("True or False")
print(a or b)
print("False or False")
print(False or False)

# Test complex expressions
print("not (True and False)")
print(not (True and False))
print("True and (False or True)")
print(True and (False or True))

# Test with comparisons
m: int = 4
n: int = 5
print("(m < n) and (n > 0)")
print((m < n) and (n > 0))
print("(m > n) or (n == 5)")
print((m > n) or (n == 5))
