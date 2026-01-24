#Задание 2.1: Типы топлива 
PRICES = {
    "АИ-92": 52.0,
    "АИ-95": 58.3,
    "АИ-98": 64.7,
    "ДТ": 56.0
}

MIN_TANK_LEVEL = 2000  
#  ТЗ 2.2: Автоматическое отключение при низком уровне
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
# ТЗ 2.2: Предупреждения о выключенных цистернах 
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