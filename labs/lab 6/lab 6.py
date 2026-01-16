# Задание 1
def n(val, a, b):
    if a == 'h' and b == 'm':
        return val * 60
    elif a == 'm' and b == 'h':
        return val / 60
    elif a == 's' and b == 'h':
        return val / 3600
    elif a == 'h' and b == 's':
        return val * 3600
    elif a == 'm' and b == 's':
        return val * 60
    elif a == 's' and b == 'm':
        return val / 60
    else:
        return val
# Задание 2
def bank_profit(a, n):
    if a < 30000:
        return "Ошибка"
    add_rate = min((a // 10000) * 0.003, 0.05)
    if n <= 3:
        base_rate = 0.03
    elif n <= 6:
        base_rate = 0.05
    else:
        base_rate = 0.02
    
    total_rate = base_rate + add_rate
    total = a * ((1 + total_rate) ** n)
    profit = total - a
    return round(profit, 2)
#Задание 3
def n(a, b):
    res = []
    for num in range(a, b+1):
        if num > 1:
            ress = True
            for i in range(2, num):
                if num % i == 0:
                    ress = False
                    break
            if ress:
                res.append(num)
    return res