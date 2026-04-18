# 1) Генератор квадратов чисел от 0 до n
# yield возвращает значения по одному, а не весь список сразу
def generate_squares(n):
    for i in range(n + 1):
        yield i * i
print("Squares up to N:")
for value in generate_squares(5):
    print(value)


# 2) Генератор четных чисел от 0 до n
# str(i) нужен для join, потому что join объединяет только строки
def even_numbers(n):
    for i in range(0, n + 1):
        if i % 2 == 0:
            yield str(i)
n = int(input("Enter n for even numbers: "))
print(",".join(even_numbers(n)))


# 3) Числа от 0 до n, которые делятся и на 3, и на 4
def divisible_by_3_and_4(n):
    for i in range(n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i
n = int(input("Enter n for numbers divisible by 3 and 4: "))
for num in divisible_by_3_and_4(n):
    print(num)


# 4) Генератор квадратов в диапазоне [a, b]
def squares(a, b):
    for i in range(a, b + 1):
        yield i * i
print("Squares from a to b:")
for value in squares(3, 7):
    print(value)


# 5) Генератор обратного отсчета от n до 0
def countdown(n):
    while n >= 0:
        yield n
        n -= 1
print("Countdown from n to 0:")
for value in countdown(10):
    print(value)
