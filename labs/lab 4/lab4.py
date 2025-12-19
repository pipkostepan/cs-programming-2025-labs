# Задание 1
temperature = float(input('Введите температуру: '))
if temperature < 20:
    print('Кондиционер включен')
else:
    print('Кондиционер выключен')

#Задание 2
month = int(input("Введите номер месяца: "))
if month == 12 or month == 1 or month == 2:
    print("Зима")
elif month == 3 or month == 4 or month == 5:
    print("Весна")
elif month == 6 or month == 7 or month == 8:
    print("Лето")
elif month == 9 or month == 10 or month == 11:
    print("Осень")
print("Неверный номер месяца")

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
errors = []
if len(password) < 8:
    errors.append("слишком короткий")
if not any(c.isupper() for c in password):
    errors.append("нет заглавных букв")
if not any(c.islower() for c in password):
    errors.append("нет строчных букв")
if not any(c.isdigit() for c in password):
    errors.append("нет цифр")
if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?/" for c in password):
    errors.append("нет специальных символов")
if errors:
    print(f"Пароль ненадежный: {', '.join(errors)}")
else:
    print("Пароль надежный!")

#Задание 6
year = int(input("Введите год: "))
if year % 4 == 0:
    if year % 100 == 0 and year % 400 != 0:
        print(f"{year} - не високосный год")
    else:
        print(f"{year} - високосный год")
else:
    print(f"{year} - не високосный год")

#Задание 7
a=float(input("Введите первое число: "))
b=float(input("Введите второе число: "))
c=float(input("Введите третье число: "))
if a <=b and a<=c:
    minimim=a
elif b<=a and b<=c:
    minimim=b
else:
    minimim=c
print(f"Наименьшее число: {minimim}")

#Задание 8
s=float(input('Введите сумму покупки: '))
if s<=1000:
    discount=0
elif s<=5000:
    discount=5
elif s<=10000:
    discount=10
else:
    discount=15
z=s*(1-discount/100)
print(f'Ваша скидка: {discount}%')
print(f'К оплате: {z}руб')

#Задание 9
hour = int(input("Введите час: "))
if 0 <= hour <= 5:
    print("Ночь")
elif 6 <= hour <= 11:
    print("Утро")
elif 12 <= hour <= 17:
    print("День")
elif 18 <= hour <= 23:
    print("Вечер")
else:
    print("Неверное время")

#Задание 10
n=int(input("Введите число: "))
if n < 2:
    print(f'{n} - составное число')
else:
    i=2
    while i < n:
        if n % i ==0:
            print(f'{n} - составное число')
            i=n
        i=i+1
    else:
        if n >= 2 and i == n:
            print(f'{n} - простое число')