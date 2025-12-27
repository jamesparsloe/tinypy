# Test elif statements

def grade(score: int) -> str:
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"

print(grade(95))
print(grade(85))
print(grade(75))
print(grade(65))
print(grade(55))

# Nested elif
x: int = 0

if x > 0:
    print("positive")
elif x < 0:
    print("negative")
else:
    print("zero")
