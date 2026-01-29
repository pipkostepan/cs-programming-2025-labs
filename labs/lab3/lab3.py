##1
name =input("Введите имя: ")
age = input("Введите возраст: ")
for i in range(10):
    print(f"Меня зовут {name} и мне {age} лет")

##2
number = int(input("Введите число от 1 до 9: "))
if number>9 and number<0:
    print:("не то число")
else:    
    print(f"Таблица умножения для числа {number}:")
    for i in range(1, 11):
        result = number * i
        print(f"{number} * {i} = {result}")

##3
print("Каждое третье число от 0 до 100:")
for i in range(0, 101, 3):
    print(i, end=" ")
print()

##4
n = int(input("Введите число: "))
factorial = 1
for i in range(1, n + 1):
    factorial=factorial*i
print(f"Факториал числа {n} равен {factorial}")

##5
i = 20
print("Числа от 20 до 0:")
while i >= 0: 
    print(i, end=" ")
    i -= 1
print()

##6
n = int(input("Введите число: "))
a, b = 0, 1
print("Числа Фибоначчи:")
while a <= n:
    print(a, end=" ")
    c = a+b
    a = b
    b = c

##7
word = input("Введите слово: ")
result = ""
number = 1
for letter in word:
    result += letter + str(number)
    number += 1
print(result)

##8
while True:
    s = int(input("Введите первое число: "))
    b = int(input("Введите второе число: "))
    sum = s + b
    print("Сумма равна:", sum)