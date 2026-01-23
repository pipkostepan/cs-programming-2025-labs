# Система управления автозаправочной станцией (АЗС)
# Автор: студент 1 курса, группа ПИ-101
# Компания: НефтеСофт
# Дата: 23 января 2026 г.

import json
import os
from datetime import datetime

# Файлы данных
TANKS_FILE = "tanks.json"
STATS_FILE = "stats.json"
HISTORY_FILE = "history.json"

# Цены на топливо (руб/л)
PRICES = {
    "АИ-92": 52.0,
    "АИ-95": 58.3,
    "АИ-98": 64.7,
    "ДТ": 56.0
}

# Минимальный уровень топлива (в литрах), при котором цистерна отключается
MIN_TANK_LEVEL = 2000

# Схема подключения колонок к цистернам
COLUMNS = {
    1: ["АИ-92", "АИ-95"],
    2: ["АИ-92", "АИ-95"],
    3: ["АИ-92", "АИ-95", "АИ-98", "ДТ"],
    4: ["АИ-92", "АИ-95", "АИ-98", "ДТ"],
    5: ["АИ-92", "АИ-95", "АИ-98", "ДТ"],
    6: ["АИ-92", "АИ-95", "АИ-98", "ДТ"],
    7: ["АИ-95", "ДТ"],
    8: ["АИ-95", "ДТ"]
}

# Инициализация данных при первом запуске
def init_data():
    if not os.path.exists(TANKS_FILE):
        tanks = [
            {"id": 1, "fuel": "АИ-92", "max_volume": 20000, "current": 15000, "enabled": True},
            {"id": 2, "fuel": "АИ-95", "max_volume": 20000, "current": 18000, "enabled": True},
            {"id": 3, "fuel": "АИ-95", "max_volume": 20000, "current": 1000, "enabled": False},  # ниже порога
            {"id": 4, "fuel": "АИ-98", "max_volume": 15000, "current": 10000, "enabled": True},
            {"id": 5, "fuel": "ДТ", "max_volume": 25000, "current": 20000, "enabled": True}
        ]
        save_tanks(tanks)

    if not os.path.exists(STATS_FILE):
        stats = {
            "total_income": 0.0,
            "cars_served": 0,
            "fuel_sold": {f: 0 for f in PRICES},
            "fuel_transactions": {f: 0 for f in PRICES}
        }
        save_stats(stats)

    if not os.path.exists(HISTORY_FILE):
        history = []
        save_history(history)

# Сохранение и загрузка данных
def load_tanks():
    with open(TANKS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_tanks(tanks):
    with open(TANKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tanks, f, ensure_ascii=False, indent=2)

def load_stats():
    with open(STATS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_stats(stats):
    with open(STATS_FILE, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

def load_history():
    with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_history(history):
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def log_event(event):
    history = load_history()
    history.append(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {event}")
    save_history(history)

# Получить цистерну по типу топлива и колонке
def get_tank_for_column(column, fuel):
    tanks = load_tanks()
    # Назначение цистерн по логике из ТЗ
    if fuel == "АИ-92":
        return next((t for t in tanks if t["fuel"] == "АИ-92"), None)
    elif fuel == "АИ-98":
        return next((t for t in tanks if t["fuel"] == "АИ-98"), None)
    elif fuel == "ДТ":
        return next((t for t in tanks if t["fuel"] == "ДТ"), None)
    elif fuel == "АИ-95":
        if column <= 4:
            return next((t for t in tanks if t["fuel"] == "АИ-95" and t["id"] == 2), None)
        else:
            return next((t for t in tanks if t["fuel"] == "АИ-95" and t["id"] == 3), None)
    return None

# Проверка и отключение цистерн с низким уровнем
def check_tanks_auto_disable():
    tanks = load_tanks()
    changed = False
    for tank in tanks:
        if tank["current"] < MIN_TANK_LEVEL and tank["enabled"]:
            tank["enabled"] = False
            changed = True
            log_event(f"Цистерна {tank['fuel']} №{tank['id']} отключена (низкий уровень)")
    if changed:
        save_tanks(tanks)

# Вывод предупреждений о выключенных цистернах
def show_warnings():
    tanks = load_tanks()
    disabled = [t for t in tanks if not t["enabled"]]
    if disabled:
        print("ВНИМАНИЕ!")
        print("Обнаружены отключённые цистерны:")
        for t in disabled:
            reason = "низкий уровень топлива" if t["current"] < MIN_TANK_LEVEL else "вручную"
            print(f" - {t['fuel']} №{t['id']} ({reason})")
        print()

# Главное меню
def main_menu():
    print("=" * 40)
    print("АЗС <<СеверНефть>>")
    print("Система управления заправочной станцией")
    print("=" * 40)
    show_warnings()
    print("-" * 40)
    print("Выберите действие:")
    print("1) Обслужить клиента (касса)")
    print("2) Проверить состояние цистерн")
    print("3) Оформить пополнение топлива")
    print("4) Баланс и статистика")
    print("5) История операций")
    print("6) Перекачка топлива между цистернами")
    print("7) Включение / отключение цистерн")
    print("8) Состояние колонок")
    print("9) EMERGENCY - аварийная ситуация")
    print("0) Выход")

# 1. Обслуживание клиента
def serve_client():
    print("\n--- Обслуживание клиента ---\n")
    print("Доступные колонки:")
    for i in range(1, 9):
        print(f"{i}) Колонка {i}")
    try:
        col = int(input("\nВыберите колонку:\n> "))
        if col < 1 or col > 8:
            raise ValueError
    except ValueError:
        print("Неверный номер колонки.")
        input("\nНажмите Enter для возврата в меню...")
        return

    fuels = COLUMNS[col]
    print(f"\nКолонка {col}\n")
    print("Доступные виды топлива:")
    for i, f in enumerate(fuels, 1):
        tank = get_tank_for_column(col, f)
        status = f" (цистерна {f} №{tank['id']})" if tank else " (нет цистерны)"
        print(f"{i}) {f}{status}")

    try:
        choice = int(input("\nВыберите тип топлива:\n> ")) - 1
        if choice < 0 or choice >= len(fuels):
            raise ValueError
        fuel = fuels[choice]
    except (ValueError, IndexError):
        print("Неверный выбор.")
        input("\nНажмите Enter для возврата в меню...")
        return

    tank = get_tank_for_column(col, fuel)
    if not tank:
        print("Ошибка: нет подходящей цистерны.")
        input("\nНажмите Enter для возврата в меню...")
        return

    if not tank["enabled"]:
        print(f"\nОШИБКА:\nЦистерна {fuel} №{tank['id']} отключена.\nОтпуск топлива невозможен.")
        input("\nНажмите Enter для возврата в меню...")
        return

    try:
        liters = float(input("\nВведите количество литров:\n> "))
        if liters <= 0:
            raise ValueError
    except ValueError:
        print("Неверное количество литров.")
        input("\nНажмите Enter для возврата в меню...")
        return

    if tank["current"] < liters:
        print(f"\nОШИБКА:\nНедостаточно топлива в цистерне. Доступно: {tank['current']} л.")
        input("\nНажмите Enter для возврата в меню...")
        return

    cost = liters * PRICES[fuel]
    print(f"\nСтоимость:\n{liters} л × {PRICES[fuel]:.2f} ₽ = {cost:.2f} ₽")
    confirm = input("\nПодтвердить оплату? (y/n)\n> ").strip().lower()
    if confirm != 'y':
        print("Операция отменена.")
        input("\nНажмите Enter для возврата в меню...")
        return

    # Выполняем продажу
    tanks = load_tanks()
    for t in tanks:
        if t["id"] == tank["id"]:
            t["current"] -= liters
            break
    save_tanks(tanks)

    stats = load_stats()
    stats["total_income"] += cost
    stats["cars_served"] += 1
    stats["fuel_sold"][fuel] += liters
    stats["fuel_transactions"][fuel] += 1
    save_stats(stats)

    log_event(f"Продажа: {liters} л {fuel} на колонке {col}, сумма: {cost:.2f} ₽")

    print("\nОперация выполнена успешно.")
    print("Спасибо за покупку!")
    input("\nНажмите Enter для возврата в меню...")

# 2. Состояние цистерн
def show_tanks():
    print("\n--- Состояние цистерн ---\n")
    tanks = load_tanks()
    for i, t in enumerate(tanks, 1):
        status = "ВКЛ" if t["enabled"] else "ВЫКЛ"
        warn = ""
        if not t["enabled"] and t["current"] < MIN_TANK_LEVEL:
            warn = " (ниже порога)"
        print(f"{i}) {t['fuel']} №{t['id']} | {int(t['current'])} / {t['max_volume']} л | {status}{warn}")
    input("\nНажмите Enter для возврата в меню...")

# 3. Пополнение топлива
def refill_tank():
    print("\n--- Оформить пополнение топлива ---\n")
    tanks = load_tanks()
    for i, t in enumerate(tanks, 1):
        print(f"{i}) {t['fuel']} №{t['id']} | {int(t['current'])} / {t['max_volume']} л")
    try:
        idx = int(input("\nВыберите цистерну:\n> ")) - 1
        if idx < 0 or idx >= len(tanks):
            raise ValueError
        tank = tanks[idx]
    except (ValueError, IndexError):
        print("Неверный выбор.")
        input("\nНажмите Enter для возврата в меню...")
        return

    try:
        liters = float(input("Сколько литров добавить?\n> "))
        if liters <= 0:
            raise ValueError
    except ValueError:
        print("Неверное количество.")
        input("\nНажмите Enter для возврата в меню...")
        return

    if tank["current"] + liters > tank["max_volume"]:
        print("Ошибка: превышает максимальный объем цистерны.")
        input("\nНажмите Enter для возврата в меню...")
        return

    tank["current"] += liters
    save_tanks(tanks)
    log_event(f"Пополнение: +{liters} л в {tank['fuel']} №{tank['id']}")
    print("Пополнение успешно оформлено.")
    input("\nНажмите Enter для возврата в меню...")

# 4. Статистика
def show_stats():
    print("\n--- Баланс и статистика ---\n")
    stats = load_stats()
    print(f"Обслужено автомобилей: {stats['cars_served']}")
    print(f"Общий доход: {stats['total_income']:,.2f} ₽\n")
    print("Продано топлива:")
    for fuel in PRICES:
        liters = stats["fuel_sold"][fuel]
        income = liters * PRICES[fuel]
        print(f"{fuel} - {int(liters)} л ({income:,.2f} ₽)")
    input("\nНажмите Enter для возврата в меню...")

# 5. История
def show_history():
    print("\n--- История операций ---\n")
    history = load_history()
    if not history:
        print("История пуста.")
    else:
        for entry in history[-10:]:  # последние 10 записей
            print(entry)
    input("\nНажмите Enter для возврата в меню...")

# 6. Перекачка топлива
def transfer_fuel():
    print("\n--- Перекачка топлива между цистернами ---\n")
    tanks = load_tanks()
    same_fuel = {}
    for t in tanks:
        same_fuel.setdefault(t["fuel"], []).append(t)

    print("Выберите тип топлива для перекачки:")
    fuels = list(same_fuel.keys())
    for i, f in enumerate(fuels, 1):
        print(f"{i}) {f}")
    try:
        f_idx = int(input("\n> ")) - 1
        fuel = fuels[f_idx]
    except (ValueError, IndexError):
        print("Неверный выбор.")
        input("\nНажмите Enter для возврата в меню...")
        return

    candidates = same_fuel[fuel]
    if len(candidates) < 2:
        print("Недостаточно цистерн для перекачки.")
        input("\nНажмите Enter для возврата в меню...")
        return

    print("\nИсточник:")
    for i, t in enumerate(candidates, 1):
        print(f"{i}) {fuel} №{t['id']} | {int(t['current'])} л")
    try:
        src_idx = int(input("\n> ")) - 1
        src = candidates[src_idx]
    except (ValueError, IndexError):
        print("Неверный выбор источника.")
        input("\nНажмите Enter для возврата в меню...")
        return

    print("\nПриёмник:")
    others = [t for t in candidates if t != src]
    for i, t in enumerate(others, 1):
        print(f"{i}) {fuel} №{t['id']} | {int(t['current'])} / {t['max_volume']} л")
    try:
        dst_idx = int(input("\n> ")) - 1
        dst = others[dst_idx]
    except (ValueError, IndexError):
        print("Неверный выбор приёмника.")
        input("\nНажмите Enter для возврата в меню...")
        return

    try:
        liters = float(input("\nСколько литров перекачать?\n> "))
        if liters <= 0 or liters > src["current"]:
            raise ValueError
        if dst["current"] + liters > dst["max_volume"]:
            raise ValueError("Превышает объём приёмника")
    except ValueError as e:
        print(f"Ошибка: {e}")
        input("\nНажмите Enter для возврата в меню...")
        return

    src["current"] -= liters
    dst["current"] += liters
    save_tanks(tanks)
    log_event(f"Перекачка: {liters} л {fuel} из №{src['id']} в №{dst['id']}")
    print("Перекачка успешно выполнена.")
    input("\nНажмите Enter для возврата в меню...")

# 7. Управление цистернами
def manage_tanks():
    print("\n--- Управление цистернами ---\n")
    print("Доступные действия:")
    print("1) Включить цистерну")
    print("2) Отключить цистерну")
    action = input("\n> ").strip()
    tanks = load_tanks()

    if action == "1":
        disabled = [t for t in tanks if not t["enabled"]]
        if not disabled:
            print("Нет отключённых цистерн.")
            input("\nНажмите Enter для возврата в меню...")
            return
        print("\nЦистерны, доступные для включения:")
        for i, t in enumerate(disabled, 1):
            print(f"{i}) {t['fuel']} №{t['id']} | {int(t['current'])} / {t['max_volume']} л")
        try:
            idx = int(input("\nВыберите цистерну:\n> ")) - 1
            tank = disabled[idx]
            if tank["current"] < MIN_TANK_LEVEL:
                print("Нельзя включить: уровень топлива ниже минимального!")
                input("\nНажмите Enter для возврата в меню...")
                return
            for t in tanks:
                if t["id"] == tank["id"]:
                    t["enabled"] = True
                    break
            save_tanks(tanks)
            log_event(f"Цистерна {tank['fuel']} №{tank['id']} включена вручную")
            print(f"Цистерна {tank['fuel']} №{tank['id']} успешно включена.")
        except (ValueError, IndexError):
            print("Неверный выбор.")
    elif action == "2":
        enabled = [t for t in tanks if t["enabled"]]
        if not enabled:
            print("Нет включённых цистерн.")
            input("\nНажмите Enter для возврата в меню...")
            return
        print("\nЦистерны для отключения:")
        for i, t in enumerate(enabled, 1):
            print(f"{i}) {t['fuel']} №{t['id']}")
        try:
            idx = int(input("\nВыберите цистерну:\n> ")) - 1
            tank = enabled[idx]
            for t in tanks:
                if t["id"] == tank["id"]:
                    t["enabled"] = False
                    break
            save_tanks(tanks)
            log_event(f"Цистерна {tank['fuel']} №{tank['id']} отключена вручную")
            print(f"Цистерна {tank['fuel']} №{tank['id']} отключена.")
        except (ValueError, IndexError):
            print("Неверный выбор.")
    else:
        print("Неверное действие.")
    input("\nНажмите Enter для возврата в меню...")

# 8. Состояние колонок
def show_columns():
    print("\n--- Состояние колонок ---\n")
    for col in range(1, 9):
        print(f"Колонка {col}:")
        fuels = COLUMNS[col]
        for f in fuels:
            tank = get_tank_for_column(col, f)
            if tank and tank["enabled"]:
                status = "РАБОТАЕТ"
            else:
                status = "НЕ РАБОТАЕТ"
            print(f"  - {f}: {status}")
        print()
    input("\nНажмите Enter для возврата в меню...")

# 9. Аварийная ситуация
def emergency():
    print("\n!!! АВАРИЙНАЯ СИТУАЦИЯ !!!")
    confirm = input("Подтвердите активацию аварийного режима (YES):\n> ").strip()
    if confirm != "YES":
        print("Аварийный режим не активирован.")
        input("\nНажмите Enter для возврата в меню...")
        return

    tanks = load_tanks()
    for tank in tanks:
        tank["enabled"] = False
    save_tanks(tanks)
    log_event("АВАРИЯ: все цистерны заблокированы. Вызваны аварийные службы.")
    print("\nВсе цистерны заблокированы!")
    print("Имитация вызова МЧС и скорой помощи...")
    print("АЗС остановлена до устранения аварии.")
    input("\nНажмите Enter для возврата в меню...")

# Основной цикл программы
def main():
    init_data()
    while True:
        check_tanks_auto_disable()
        main_menu()
        choice = input("> ").strip()
        if choice == "1":
            serve_client()
        elif choice == "2":
            show_tanks()
        elif choice == "3":
            refill_tank()
        elif choice == "4":
            show_stats()
        elif choice == "5":
            show_history()
        elif choice == "6":
            transfer_fuel()
        elif choice == "7":
            manage_tanks()
        elif choice == "8":
            show_columns()
        elif choice == "9":
            emergency()
        elif choice == "0":
            print("Выход из системы. До свидания!")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")
            input("\nНажмите Enter для продолжения...")
