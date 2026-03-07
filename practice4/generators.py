# 1. Generator that generates squares up to N
def generate_squares(n):
    for i in range(n + 1):
        yield i * i
print("Squares up to N:")
for value in generate_squares(5):
    print(value)


# 2. Print even numbers between 0 and n in comma separated form
def even_numbers(n):
    for i in range(0, n + 1):
        if i % 2 == 0:
            yield str(i)
n = int(input("Enter n for even numbers: "))
print(",".join(even_numbers(n)))


# 3. Numbers divisible by 3 and 4 between 0 and n
def divisible_by_3_and_4(n):
    for i in range(n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i
n = int(input("Enter n for numbers divisible by 3 and 4: "))
for num in divisible_by_3_and_4(n):
    print(num)


# 4. Generator squares from a to b
def squares(a, b):
    for i in range(a, b + 1):
        yield i * i
print("Squares from a to b:")
for value in squares(3, 7):
    print(value)


# 5. Generator from n down to 0
def countdown(n):
    while n >= 0:
        yield n
        n -= 1
print("Countdown from n to 0:")
for value in countdown(10):
    print(value)