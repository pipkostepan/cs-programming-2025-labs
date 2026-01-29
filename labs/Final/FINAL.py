# Система управления автозаправочной станцией (АЗС)

import json 
import os # подключает модуль для взаимодействия с операционной системой
from datetime import datetime #импортирует только класс datetime из модуля datetime 

# Файлы данных
TANKS_FILE = "tanks.json" # состояние цистерн
STATS_FILE = "stats.json" # статистика продаж
HISTORY_FILE = "history.json" # журнал событий
SYSTEM_FILE = "system.json"  # для хранения состояния аварии

# Цены на топливо (руб/л)
PRICES = {
    "АИ-92": 72.2,
    "АИ-95": 73.3,
    "АИ-98": 78.7,
    "ДТ": 84.0
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

def init_data():
    """Инициализация данных при первом запуске"""
    if not os.path.exists(TANKS_FILE):
        tanks = [
            {"fuel": "АИ-92", "number": 1, "max_volume": 20000, "current": 15000, "enabled": True},
            {"fuel": "АИ-95", "number": 1, "max_volume": 20000, "current": 18000, "enabled": True},
            {"fuel": "АИ-95", "number": 2, "max_volume": 20000, "current": 1000,  "enabled": False},
            {"fuel": "АИ-98", "number": 1, "max_volume": 15000, "current": 10000, "enabled": True},
            {"fuel": "ДТ",    "number": 1, "max_volume": 25000, "current": 20000, "enabled": True}
        ]
        with open(TANKS_FILE, 'w', encoding='utf-8') as f:
            json.dump(tanks, f, ensure_ascii=False, indent=2)

    if not os.path.exists(STATS_FILE):
        stats = {
            "total_income": 0.0,
            "cars_served": 0,
            "fuel_sold": {f: 0.0 for f in PRICES},
            "fuel_transactions": {f: 0 for f in PRICES}
        }
        with open(STATS_FILE, 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)

    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=2)

    if not os.path.exists(SYSTEM_FILE):
        with open(SYSTEM_FILE, 'w', encoding='utf-8') as f:
            json.dump({"emergency": False}, f, ensure_ascii=False, indent=2)

def load_json(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def log_event(event): # добавляет метку времени к каждой записи в истории 
    history = load_json(HISTORY_FILE)
    history.append(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {event}")
    save_json(HISTORY_FILE, history)

def is_emergency(): #Проверяет, активен ли аварийный режим
    return load_json(SYSTEM_FILE)["emergency"]

def set_emergency(active=True): #Устанавливает состояние аварийного режима
    system = load_json(SYSTEM_FILE)
    system["emergency"] = active
    save_json(SYSTEM_FILE, system)

def get_tank_for_column(column, fuel): # Возвращает цистерну, подключенную к колонке и типу топлива
    tanks = load_json(TANKS_FILE)
    if fuel == "АИ-92":
        return next((t for t in tanks if t["fuel"] == "АИ-92"), None)
    elif fuel == "АИ-98":
        return next((t for t in tanks if t["fuel"] == "АИ-98"), None)
    elif fuel == "ДТ":
        return next((t for t in tanks if t["fuel"] == "ДТ"), None)
    elif fuel == "АИ-95":
        if 1 <= column <= 4:
            return next((t for t in tanks if t["fuel"] == "АИ-95" and t["number"] == 1), None)
        elif 5 <= column <= 8:
            return next((t for t in tanks if t["fuel"] == "АИ-95" and t["number"] == 2), None)
    return None

def check_tanks_auto_disable(): #Автоматически отключает цистерны с уровнем ниже MIN_TANK_LEVEL
    tanks = load_json(TANKS_FILE)
    changed = False
    for tank in tanks:
        if tank["current"] < MIN_TANK_LEVEL and tank["enabled"]:
            tank["enabled"] = False
            changed = True
            log_event(f"Цистерна {tank['fuel']} №{tank['number']} отключена (низкий уровень)")
    if changed:
        save_json(TANKS_FILE, tanks)

def show_warnings(): # Показывает предупреждения о выключенных цистернах
    tanks = load_json(TANKS_FILE)
    disabled = [t for t in tanks if not t["enabled"]]
    if disabled:
        print("ВНИМАНИЕ!")
        print("Обнаружены отключённые цистерны:")
        for t in disabled:
            reason = "низкий уровень топлива" if t["current"] < MIN_TANK_LEVEL else "вручную"
            print(f" - {t['fuel']} №{t['number']} ({reason})")
        print()

def main_menu():
    print("=" * 40)
    print("АЗС <<СеверНефть>>")
    print("Система управления заправочной станцией")
    print("=" * 40)

    if is_emergency():
        print("\n !АВАРИЙНЫЙ РЕЖИМ! Все операции кроме выхода из аварии и завершения работы заблокированы.")
    else:
        show_warnings()

    print("-" * 40)
    print("Выберите действие:")
    if is_emergency():
        print("9) ВЫЙТИ из аварийного режима")
        print("0) Выход")
    else:
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

def serve_client():
    if is_emergency():
        print("\nАЗС находится в аварийном режиме. Заправка невозможна.")
        input("\nНажмите Enter для возврата в меню...")
        return

    print("\n--- Обслуживание клиента ---\n")
    print("Доступные колонки:")
    for i in range(1, 9):
        print(f"{i}) Колонка {i}")
    
    try:
        col = int(input("\nВыберите колонку:\n> "))
        if not (1 <= col <= 8):
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
        if tank:
            status = f" (цистерна {f} №{tank['number']})"
        else:
            status = " (нет цистерны)"
        print(f"{i}) {f}{status}")

    try:
        choice = int(input("\nВыберите тип топлива:\n> ")) - 1
        if not (0 <= choice < len(fuels)):
            raise ValueError
        fuel = fuels[choice]
    except (ValueError, IndexError):
        print("Неверный выбор.")
        input("\nНажмите Enter для возврата в меню...")
        return

    tank = get_tank_for_column(col, fuel)
    if tank is None:
        print("Ошибка: нет подходящей цистерны для этого топлива на выбранной колонке.")
        input("\nНажмите Enter для возврата в меню...")
        return

    if not tank["enabled"]:
        print(f"\nОШИБКА:\nЦистерна {fuel} №{tank['number']} отключена.\nОтпуск топлива невозможен.")
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
        print(f"\nОШИБКА:\nНедостаточно топлива. Доступно: {tank['current']:.0f} л.")
        input("\nНажмите Enter для возврата в меню...")
        return

    cost = liters * PRICES[fuel]
    print(f"\nСтоимость:\n{liters:.1f} л × {PRICES[fuel]:.2f} ₽ = {cost:.2f} ₽")
    confirm = input("\nПодтвердить оплату? (y/n)\n> ").strip().lower()
    if confirm != 'y':
        print("Операция отменена.")
        input("\nНажмите Enter для возврата в меню...")
        return

    # Списание топлива
    tanks = load_json(TANKS_FILE)
    for t in tanks:
        if t["fuel"] == tank["fuel"] and t["number"] == tank["number"]:
            t["current"] -= liters
            break
    save_json(TANKS_FILE, tanks)

    # Обновление статистики
    stats = load_json(STATS_FILE)
    stats["total_income"] += cost
    stats["cars_served"] += 1
    stats["fuel_sold"][fuel] += liters
    stats["fuel_transactions"][fuel] += 1
    save_json(STATS_FILE, stats)

    log_event(f"Продажа: {liters:.1f} л {fuel} на колонке {col}, сумма: {cost:.2f} ₽")
    print("\nОперация выполнена успешно.")
    print("Спасибо за покупку!")
    input("\nНажмите Enter для возврата в меню...")

def show_tanks():
    print("\n--- Состояние цистерн ---\n")
    tanks = load_json(TANKS_FILE)
    for t in tanks:
        status = "ВКЛ" if t["enabled"] else "ВЫКЛ"
        warn = " (ниже порога)" if not t["enabled"] and t["current"] < MIN_TANK_LEVEL else ""
        print(f"{t['fuel']} №{t['number']} | {int(t['current'])} / {t['max_volume']} л | {status}{warn}")
    input("\nНажмите Enter для возврата в меню...")

def refill_tank():
    if is_emergency():
        print("\nАЗС в аварийном режиме. Пополнение невозможно.")
        input("\nНажмите Enter для возврата в меню...")
        return

    print("\n--- Оформить пополнение топлива ---\n")
    tanks = load_json(TANKS_FILE)
    for i, t in enumerate(tanks, 1):
        print(f"{i}) {t['fuel']} №{t['number']} | {int(t['current'])} / {t['max_volume']} л")
    
    try:
        idx = int(input("\nВыберите цистерну:\n> ")) - 1
        if not (0 <= idx < len(tanks)):
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
    save_json(TANKS_FILE, tanks)
    log_event(f"Пополнение: +{liters} л в {tank['fuel']} №{tank['number']}")
    print("Пополнение успешно оформлено.")
    input("\nНажмите Enter для возврата в меню...")

def show_stats():
    print("\n--- Баланс и статистика ---\n")
    stats = load_json(STATS_FILE)
    print(f"Обслужено автомобилей: {stats['cars_served']}")
    print(f"Общий доход: {stats['total_income']:,.2f} ₽\n")
    print("Продано топлива:")
    for fuel in PRICES:
        liters = stats["fuel_sold"][fuel]
        income = liters * PRICES[fuel]
        print(f"{fuel} - {int(liters)} л ({income:,.2f} ₽)")
    input("\nНажмите Enter для возврата в меню...")

def show_history():
    print("\n--- История операций ---\n")
    history = load_json(HISTORY_FILE)
    if not history:
        print("История пуста.")
    else:
        for entry in history[-10:]:
            print(entry)
    input("\nНажмите Enter для возврата в меню...")

def transfer_fuel():
    if is_emergency():
        print("\nАЗС в аварийном режиме. Перекачка невозможна.")
        input("\nНажмите Enter для возврата в меню...")
        return

    print("\n--- Перекачка топлива между цистернами ---\n")
    tanks = load_json(TANKS_FILE)
    from collections import defaultdict
    grouped = defaultdict(list)
    for t in tanks:
        grouped[t["fuel"]].append(t)

    fuels = list(grouped.keys())
    print("Выберите тип топлива:")
    for i, f in enumerate(fuels, 1):
        print(f"{i}) {f}")
    
    try:
        f_idx = int(input("\n> ")) - 1
        fuel = fuels[f_idx]
    except (ValueError, IndexError):
        print("Неверный выбор.")
        input("\nНажмите Enter для возврата в меню...")
        return

    candidates = grouped[fuel]
    if len(candidates) < 2:
        print("Недостаточно цистерн для перекачки.")
        input("\nНажмите Enter для возврата в меню...")
        return

    print("\nИсточник:")
    for i, t in enumerate(candidates, 1):
        print(f"{i}) {fuel} №{t['number']} | {int(t['current'])} л")
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
        print(f"{i}) {fuel} №{t['number']} | {int(t['current'])} / {t['max_volume']} л")
    try:
        dst_idx = int(input("\n> ")) - 1
        dst = others[dst_idx]
    except (ValueError, IndexError):
        print("Неверный выбор приёмника.")
        input("\nНажмите Enter для возврата в меню...")
        return

    try:
        liters = float(input("\nСколько литров перекачать?\n> "))
        if liters <= 0:
            raise ValueError("Количество должно быть положительным")
        if liters > src["current"]:
            raise ValueError("Недостаточно топлива в источнике")
        if dst["current"] + liters > dst["max_volume"]:
            raise ValueError("Превышает объём приёмника")
    except ValueError as e:
        print(f"Ошибка: {e}")
        input("\nНажмите Enter для возврата в меню...")
        return

    src["current"] -= liters
    dst["current"] += liters
    save_json(TANKS_FILE, tanks)
    log_event(f"Перекачка: {liters} л {fuel} из №{src['number']} в №{dst['number']}")
    print("Перекачка успешно выполнена.")
    input("\nНажмите Enter для возврата в меню...")

def manage_tanks():
    if is_emergency():
        print("\nАЗС в аварийном режиме. Управление цистернами невозможно.")
        input("\nНажмите Enter для возврата в меню...")
        return

    print("\n--- Управление цистернами ---\n")
    print("1) Включить цистерну")
    print("2) Отключить цистерну")
    action = input("\n> ").strip()
    tanks = load_json(TANKS_FILE)

    if action == "1":
        disabled = [t for t in tanks if not t["enabled"]]
        if not disabled:
            print("Нет отключённых цистерн.")
            input("\nНажмите Enter для возврата в меню...")
            return
        print("\nЦистерны для включения:")
        for i, t in enumerate(disabled, 1):
            print(f"{i}) {t['fuel']} №{t['number']} | {int(t['current'])} / {t['max_volume']} л")
        try:
            idx = int(input("\n> ")) - 1
            tank = disabled[idx]
            if tank["current"] < MIN_TANK_LEVEL:
                print("Нельзя включить: уровень топлива ниже минимального!")
                input("\nНажмите Enter для возврата в меню...")
                return
            for t in tanks:
                if t["fuel"] == tank["fuel"] and t["number"] == tank["number"]:
                    t["enabled"] = True
                    break
            save_json(TANKS_FILE, tanks)
            log_event(f"Цистерна {tank['fuel']} №{tank['number']} включена вручную")
            print(f"Цистерна {tank['fuel']} №{tank['number']} успешно включена.")
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
            print(f"{i}) {t['fuel']} №{t['number']}")
        try:
            idx = int(input("\n> ")) - 1
            tank = enabled[idx]
            for t in tanks:
                if t["fuel"] == tank["fuel"] and t["number"] == tank["number"]:
                    t["enabled"] = False
                    break
            save_json(TANKS_FILE, tanks)
            log_event(f"Цистерна {tank['fuel']} №{tank['number']} отключена вручную")
            print(f"Цистерна {tank['fuel']} №{tank['number']} отключена.")
        except (ValueError, IndexError):
            print("Неверный выбор.")
    else:
        print("Неверное действие.")
    input("\nНажмите Enter для возврата в меню...")

def show_columns():
    print("\n--- Состояние колонок ---\n")
    for col in range(1, 9):
        print(f"Колонка {col}:")
        for fuel in COLUMNS[col]:
            tank = get_tank_for_column(col, fuel)
            if tank and tank["enabled"]:
                status = "РАБОТАЕТ"
            else:
                status = "НЕ РАБОТАЕТ"
            print(f"  - {fuel}: {status}")
        print()
    input("\nНажмите Enter для возврата в меню...")

def emergency():
    if is_emergency():
        print("\n ! Аварийный режим уже активен!")
        print("Для выхода из аварии используйте соответствующее действие в меню.")
        input("\nНажмите Enter для возврата в меню...")
        return

    print("\n!!! АВАРИЙНАЯ СИТУАЦИЯ !!!")
    confirm = input("Подтвердите активацию аварийного режима (YES):\n> ").strip()
    if confirm != "YES":
        print("Аварийный режим не активирован.")
        input("\nНажмите Enter для возврата в меню...")
        return

    # Отключаем все цистерны
    tanks = load_json(TANKS_FILE)
    for tank in tanks:
        tank["enabled"] = False
    save_json(TANKS_FILE, tanks)

    # Включаем аварийный режим
    set_emergency(True)

    log_event("АВАРИЯ: все цистерны заблокированы. Вызваны аварийные службы.")
    print("\nВсе цистерны заблокированы!")
    print("Имитация вызова МЧС и скорой помощи...")
    print("АЗС остановлена до устранения аварии.")
    input("\nНажмите Enter для возврата в меню...")

def deactivate_emergency():
    if not is_emergency():
        print("\nАварийный режим не активен.")
        input("\nНажмите Enter для возврата в меню...")
        return

    print("\n ВЫХОД ИЗ АВАРИЙНОГО РЕЖИМА")
    print("Внимание: цистерны остаются заблокированными!")
    print("Их необходимо включать вручную через меню управления.")
    confirm = input("Подтвердите выход из аварии (EXIT):\n> ").strip()
    if confirm != "EXIT":
        print("Выход из аварийного режима отменён.")
        input("\nНажмите Enter для возврата в меню...")
        return

    set_emergency(False)
    log_event("Выход из аварийного режима (цистерны остаются заблокированными)")
    print("\nАварийный режим отключён.")
    print("Цистерны НЕ включены автоматически — проверьте их состояние!")
    input("\nНажмите Enter для возврата в меню...")

def main():
    init_data()
    while True:
        check_tanks_auto_disable()
        main_menu()
        choice = input("> ").strip()

        if is_emergency():
            if choice == "9":
                deactivate_emergency()
            elif choice == "0":
                print("Выход из системы. До свидания!")
                break
            else:
                print("<<<<< В аварийном режиме доступны только действия 9 и 0.")
                input("Нажмите Enter для возврата в меню...")
                continue

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

if __name__ == "__main__":
    main()
