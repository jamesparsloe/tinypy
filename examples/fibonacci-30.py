def fibonacci(n: int) -> int:
    if n < 2:
        return n
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


print("30th Fibonacci number is:")
print(fibonacci(30))