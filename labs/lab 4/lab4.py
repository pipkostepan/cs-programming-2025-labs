# Задание 1
temperature = float(input('Введите температуру: '))
if temperature < 23:
    print('Кондиционер включен')
else:
    print('Кондиционер выключен')

# Задние 2
month=int(input("Введите номер месяца: "))
if month in [12, 1, 2]:
    print('Зима')
if month in [3, 4, 5]:
    print('Весна')
if month in [6, 7, 8]:
    print('Лето')
if month in [9, 10, 11]:
    print('Осень')
else:
    print('Ошибка: такого месяца нет')

#Задание 3
try:
    age = int(input("Введите возраст собаки: "))
    if age < 1:
        print("Ошибка: Возраст должен быть не меньше 1")
    elif age > 22:
        print("Ошибка: Возраст должен быть не больше 22")
    else:
        if age <= 2:
            x = age * 10.5
        else:
            x = 21 + (age - 2) * 4
        print(f"Собачий возраст {age} лет = {x} человеческих лет")
except ValueError:
    print("Ошибка: введено не число")

#Задание 4
num = int(input("Введите число: "))
if num % 2 == 0 and num % 3 == 0:
    print("Число делится на 6")
else:
    print("Не делится на 6") 

#Задание 5
password = input("Введите пароль: ")
m = ""
if len(password) < 8:
    m = m + "слишком короткий, "
if not any(c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" for c in password):
    m = m + "нет заглавных букв, "
if not any(c in "abcdefghijklmnopqrstuvwxyz" for c in password):
    m = m + "нет строчных букв, "
if not any(c in "0123456789" for c in password):
    m = m + "нет цифр, "
if not any(c in "!@#$%^&*()_+=-[]{};:'\",.<>?/" for c in password):
    m = m + "нет специальных символов, "
if m:
    print("Пароль ненадежный:", m[:-2])
else:
    print("Пароль надежный!")