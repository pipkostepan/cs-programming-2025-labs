"""
Система управления автозаправочной станцией
Пипко Степан
"""

import json
import os
from datetime import datetime

# ЗАДАНИЕ 1: Конфигурация системы

# Цены на топливо (руб/литр)
PRICES = {
    'АИ-92': 48.50,
    'АИ-95': 52.30, 
    'АИ-98': 56.80,
    'ДТ': 54.10
}

# Схема подключения колонок (из ТЗ)
COLUMNS = {
    1: {'АИ-92': 'АИ-92 №1', 'АИ-95': 'АИ-95 №1'},
    2: {'АИ-92': 'АИ-92 №1', 'АИ-95': 'АИ-95 №1'},
    3: {'АИ-92': 'АИ-92 №1', 'АИ-95': 'АИ-95 №1', 'АИ-98': 'АИ-98 №1', 'ДТ': 'ДТ №1'},
    4: {'АИ-92': 'АИ-92 №1', 'АИ-95': 'АИ-95 №1', 'АИ-98': 'АИ-98 №1', 'ДТ': 'ДТ №1'},
    5: {'АИ-92': 'АИ-92 №1', 'АИ-95': 'АИ-95 №2', 'АИ-98': 'АИ-98 №1', 'ДТ': 'ДТ №1'},
    6: {'АИ-92': 'АИ-92 №1', 'АИ-95': 'АИ-95 №2', 'АИ-98': 'АИ-98 №1', 'ДТ': 'ДТ №1'},
    7: {'АИ-95': 'АИ-95 №2', 'ДТ': 'ДТ №1'},
    8: {'АИ-95': 'АИ-95 №2', 'ДТ': 'ДТ №1'}
}

# ЗАДАНИЕ 2: Функции для работы с файлами
def load_file(filename):
    """Загружает данные из JSON файла"""
    if os.path.exists(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data
        except:
            return None
    return None

def save_file(filename, data):
    """Сохраняет данные в JSON файл"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except:
        return False

def get_current_time():
    """Возвращает текущее время в формате строки"""
    return datetime.now().strftime("%H:%M %d.%m")

# ЗАДАНИЕ 3: Класс Цистерна

class Tank:
    """Класс для представления цистерны с топливом"""
    
    def __init__(self, name, fuel_type, max_liters):
        self.name = name
        self.fuel_type = fuel_type
        self.max = max_liters
        self.current = max_liters * 0.7  # Начинаем с 70% заполнения
        self.min = max_liters * 0.1      # Минимум 10%
        self.on = True                    # Включена ли цистерна
        self.low_auto_off = False         # Автоотключение из-за низкого уровня
    
    def check_level(self):
        """Проверяет уровень топлива и отключает если нужно"""
        if self.current < self.min and self.on:
            self.on = False
            self.low_auto_off = True
            return False
        return True
    
    def can_sell(self, liters):
        """Проверяет, можно ли продать указанное количество"""
        if not self.on:
            return False, "Цистерна выключена"
        if self.current < liters:
            return False, f"Не хватает, есть только {self.current:.0f} л"
        return True, "OK"
    
    def sell(self, liters):
        """Продает топливо из цистерны"""
        ok, msg = self.can_sell(liters)
        if not ok:
            return False, msg
        self.current -= liters
        self.check_level()
        return True, f"Продано {liters:.1f} л"
    
    def add(self, liters):
        """Добавляет топливо в цистерну"""
        if self.current + liters > self.max:
            free = self.max - self.current
            return False, f"Переполнение, можно добавить {free:.0f} л"
        self.current += liters
        # После пополнения НЕ включаем автоматически
        self.low_auto_off = False
        return True, f"Добавлено {liters:.1f} л"
    
    def turn_on(self):
        """Включает цистерну"""
        if self.current >= self.min:
            self.on = True
            self.low_auto_off = False
            return True, "Включена"
        return False, "Нельзя включить: мало топлива"
    
    def turn_off(self):
        """Выключает цистерну"""
        self.on = False
        self.low_auto_off = False
        return True, "Выключена"
    
    def get_info(self):
        """Возвращает информацию о цистерне"""
        return {
            'name': self.name,
            'fuel': self.fuel_type,
            'current': self.current,
            'max': self.max,
            'percent': (self.current / self.max) * 100,
            'on': self.on,
            'low': self.low_auto_off
        }

# ЗАДАНИЕ 4: Главный класс системы

class AZSSystem:
    """Главный класс системы управления АЗС"""
    
    def __init__(self):
        # Инициализация всех данных
        self.tanks = {}      # Словарь цистерн
        self.stats = {}      # Статистика продаж
        self.history = []    # История операций
        self.emergency = False  # Аварийный режим
        
        # Загружаем или создаем систему
        self.load_system()
    
    def load_system(self):
        """Загружает или создает систему"""
        # Пробуем загрузить сохраненные данные
        tanks_data = load_file('tanks.json')
        stats_data = load_file('stats.json')
        history_data = load_file('history.json')
        emergency_data = load_file('emergency.json')
        
        if tanks_data:
            # Загружаем сохраненные цистерны
            for name, data in tanks_data.items():
                tank = Tank(name, data['fuel'], data['max'])
                tank.current = data['current']
                tank.on = data['on']
                tank.low_auto_off = data.get('low', False)
                self.tanks[name] = tank
        else:
            # Создаем новые цистерны
            self.create_tanks()
        
        if stats_data:
            self.stats = stats_data
        else:
            self.create_stats()
        
        if history_data:
            self.history = history_data
        
        if emergency_data:
            self.emergency = emergency_data.get('active', False)
    
    def save_system(self):
        """Сохраняет все данные системы"""
        # Сохраняем цистерны
        tanks_data = {}
        for name, tank in self.tanks.items():
            tanks_data[name] = {
                'fuel': tank.fuel_type,
                'max': tank.max,
                'current': tank.current,
                'on': tank.on,
                'low': tank.low_auto_off
            }
        save_file('tanks.json', tanks_data)
        
        # Сохраняем остальное
        save_file('stats.json', self.stats)
        save_file('history.json', self.history)
        save_file('emergency.json', {'active': self.emergency})
    
    def create_tanks(self):
        """Создает цистерны по заданию ТЗ"""
        # 5 цистерн как в ТЗ
        self.tanks['АИ-92 №1'] = Tank('АИ-92 №1', 'АИ-92', 20000)
        self.tanks['АИ-95 №1'] = Tank('АИ-95 №1', 'АИ-95', 20000)
        self.tanks['АИ-95 №2'] = Tank('АИ-95 №2', 'АИ-95', 20000)
        self.tanks['АИ-98 №1'] = Tank('АИ-98 №1', 'АИ-98', 15000)
        self.tanks['ДТ №1'] = Tank('ДТ №1', 'ДТ', 25000)
        
        # Начальные значения (как в примере из ТЗ)
        self.tanks['АИ-92 №1'].current = 12400
        self.tanks['АИ-95 №1'].current = 9800
        self.tanks['АИ-95 №2'].current = 1200
        self.tanks['АИ-98 №1'].current = 10000
        self.tanks['ДТ №1'].current = 15600
        
        # Отключаем те, что в примере
        self.tanks['АИ-95 №2'].turn_off()
        self.tanks['АИ-95 №2'].low_auto_off = True
        self.tanks['АИ-98 №1'].turn_off()
    
    def create_stats(self):
        """Создает начальную статистику"""
        self.stats = {
            'cars': 0,
            'money': 0.0,
            'fuel_data': {}
        }
        for fuel in PRICES:
            self.stats['fuel_data'][fuel] = {
                'liters': 0.0,
                'money': 0.0,
                'sales': 0
            }
    
    def add_history(self, action, details):
        """Добавляет запись в историю операций"""
        record = {
            'time': get_current_time(),
            'action': action,
            'details': details
        }
        self.history.append(record)
        # Ограничиваем историю 20 записями
        if len(self.history) > 20:
            self.history = self.history[-20:]
    
    def show_warnings(self):
        """Возвращает список предупреждений"""
        warnings = []
        if self.emergency:
            warnings.append("АВАРИЙНЫЙ РЕЖИМ!")
        for tank in self.tanks.values():
            if not tank.on:
                if tank.low_auto_off:
                    warnings.append(f"{tank.name}: мало топлива")
                else:
                    warnings.append(f"{tank.name}: выключена")
        return warnings

# ЗАДАНИЕ 5: Основные функции системы (меню)


    def menu_1_sell(self):
        """Обслуживает клиента (меню 1)"""
        if self.emergency:
            print("\nАварийный режим! Продажи остановлены.")
            return
        
        print("\n=== ОБСЛУЖИВАНИЕ КЛИЕНТА ===")
        
        # 1. Выбор колонки
        print("\nВыберите колонку (1-8):")
        col = input("> ")
        if not col.isdigit() or int(col) < 1 or int(col) > 8:
            print("Нет такой колонки")
            return
        col = int(col)
        
        # 2. Какое топливо на этой колонке
        fuels = COLUMNS[col]
        print(f"\nНа колонке {col} есть:")
        options = []
        i = 1
        for fuel_type, tank_name in fuels.items():
            tank = self.tanks[tank_name]
            status = "+" if tank.on else "-"
            print(f"{i}) {fuel_type} ({tank_name}) [{status}]")
            options.append((fuel_type, tank_name))
            i += 1
        
        # 3. Выбор топлива
        choice = input("\nВыберите топливо: ")
        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(options):
            print("Неверный выбор")
            return
        fuel_type, tank_name = options[int(choice)-1]
        tank = self.tanks[tank_name]
        
        # 4. Проверка цистерны
        if not tank.on:
            print(f"\nЦистерна {tank_name} отключена!")
            if tank.low_auto_off:
                print("Причина: низкий уровень топлива")
            return
        
        # 5. Сколько литров
        print(f"\nВ цистерне: {tank.current:.0f} л")
        liters = input("Сколько литров? ")
        try:
            liters = float(liters)
            if liters <= 0:
                print("Должно быть больше 0")
                return
            if liters > tank.current:
                print(f"Слишком много. Максимум: {tank.current:.0f} л")
                return
        except:
            print("Нужно число")
            return
        
        # 6. Расчет цены
        price = PRICES[fuel_type]
        cost = liters * price
        print(f"\n{liters:.1f} л × {price:.2f} руб = {cost:.2f} руб")
        
        # 7. Подтверждение
        confirm = input("\nОплатить? (д/н): ").lower()
        if confirm != 'д':
            print("Отмена")
            return
        
        # 8. Продажа
        ok, msg = tank.sell(liters)
        if not ok:
            print(f"Ошибка: {msg}")
            return
        
        # 9. Обновляем статистику
        self.stats['cars'] += 1
        self.stats['money'] += cost
        if fuel_type in self.stats['fuel_data']:
            self.stats['fuel_data'][fuel_type]['liters'] += liters
            self.stats['fuel_data'][fuel_type]['money'] += cost
            self.stats['fuel_data'][fuel_type]['sales'] += 1
        
        # 10. Запись в историю
        self.add_history('Продажа', 
            f"{liters:.1f} л {fuel_type} на колонке {col}, {cost:.2f} руб")
        
        # 11. Сохраняем
        self.save_system()
        
        print(f"\nУспешно! Продано {liters:.1f} л")
        print(f"Осталось: {tank.current:.0f} л")
    
    def menu_2_tanks(self):
        """Показывает состояние цистерн (меню 2)"""
        print("\n=== СОСТОЯНИЕ ЦИСТЕРН ===")
        
        for fuel_type in ['АИ-92', 'АИ-95', 'АИ-98', 'ДТ']:
            print(f"\n{fuel_type}:")
            for tank in self.tanks.values():
                if tank.fuel_type == fuel_type:
                    info = tank.get_info()
                    status = "ВКЛ" if info['on'] else "ВЫКЛ"
                    if info['low']:
                        status += " (авто)"
                    warning = ""
                    if info['percent'] < 20:
                        warning = " ⚠ мало"
                    
                    print(f"  {info['name']}:")
                    print(f"    {info['current']:.0f}/{info['max']:.0f} л ({info['percent']:.1f}%)")
                    print(f"    Статус: {status}{warning}")
    
    def menu_3_refill(self):
        """Пополняет цистерну (меню 3)"""
        if self.emergency:
            print("\nАварийный режим!")
            return
        
        print("\n=== ПОПОЛНЕНИЕ ЦИСТЕРНЫ ===")
        
        # Список цистерн
        print("\nВыберите цистерну:")
        tanks_list = list(self.tanks.values())
        for i, tank in enumerate(tanks_list, 1):
            free = tank.max - tank.current
            print(f"{i}) {tank.name} - можно добавить {free:.0f} л")
        
        # Выбор
        choice = input("\n> ")
        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(tanks_list):
            print("Неверный выбор")
            return
        tank = tanks_list[int(choice)-1]
        free = tank.max - tank.current
        
        # Сколько добавить
        liters = input(f"\nСколько литров добавить? (до {free:.0f}): ")
        try:
            liters = float(liters)
            if liters <= 0:
                print("Должно быть > 0")
                return
            if liters > free:
                print(f"Слишком много. Максимум: {free:.0f} л")
                return
        except:
            print("Нужно число")
            return
        
        # Подтверждение
        confirm = input(f"\nДобавить {liters:.0f} л в {tank.name}? (д/н): ")
        if confirm.lower() != 'д':
            print("Отмена")
            return
        
        # Добавляем
        ok, msg = tank.add(liters)
        if not ok:
            print(f"Ошибка: {msg}")
            return
        
        # Запись в историю
        self.add_history('Пополнение', 
            f"{tank.name}: +{liters:.0f} л, теперь {tank.current:.0f} л")
        
        # Сохраняем
        self.save_system()
        
        print(f"\nУспешно! Теперь: {tank.current:.0f} л")
        print("Цистерна осталась в текущем состоянии")
    
    def menu_4_stats(self):
        """Показывает статистику (меню 4)"""
        print("\n=== СТАТИСТИКА ===")
        
        print(f"\nВсего машин: {self.stats['cars']}")
        print(f"Всего денег: {self.stats['money']:.2f} руб")
        
        print("\nПо топливу:")
        for fuel, data in self.stats['fuel_data'].items():
            if data['sales'] > 0:
                print(f"\n{fuel}:")
                print(f"  Продано: {data['liters']:.0f} л")
                print(f"  Деньги: {data['money']:.0f} руб")
                print(f"  Раз: {data['sales']}")
    
    def menu_5_history(self):
        """Показывает историю операций (меню 5)"""
        print("\n=== ИСТОРИЯ ОПЕРАЦИЙ ===")
        
        if not self.history:
            print("\nИстория пуста")
            return
        
        print(f"\nПоследние {len(self.history)} записей:")
        for record in reversed(self.history[-10:]):
            print(f"\n[{record['time']}] {record['action']}")
            print(f"  {record['details']}")
    
    def menu_6_transfer(self):
        """Перекачивает топливо (меню 6)"""
        if self.emergency:
            print("\nАварийный режим!")
            return
        
        print("\n=== ПЕРЕКАЧКА ТОПЛИВА ===")
        print("Только между цистернами одного типа")
        
        # Группируем по типу
        groups = {}
        for tank in self.tanks.values():
            fuel = tank.fuel_type
            if fuel not in groups:
                groups[fuel] = []
            groups[fuel].append(tank)
        
        # Выбираем тип
        print("\nВыберите тип топлива:")
        fuels = list(groups.keys())
        for i, fuel in enumerate(fuels, 1):
            print(f"{i}) {fuel} ({len(groups[fuel])} цистерн)")
        
        choice = input("\n> ")
        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(fuels):
            print("Неверный выбор")
            return
        fuel_type = fuels[int(choice)-1]
        tanks = groups[fuel_type]
        
        if len(tanks) < 2:
            print(f"Для {fuel_type} только 1 цистерна")
            return
        
        # Выбираем откуда
        print(f"\nЦистерны с {fuel_type}:")
        for i, tank in enumerate(tanks, 1):
            print(f"{i}) {tank.name}: {tank.current:.0f} л")
        
        from_choice = input("\nОткуда? ")
        if not from_choice.isdigit() or int(from_choice) < 1 or int(from_choice) > len(tanks):
            print("Неверный выбор")
            return
        from_tank = tanks[int(from_choice)-1]
        
        if not from_tank.on:
            print("Цистерна отключена")
            return
        
        # Выбираем куда
        print(f"\nКуда (кроме {from_tank.name})?")
        to_options = []
        for i, tank in enumerate(tanks, 1):
            if tank.name != from_tank.name:
                free = tank.max - tank.current
                print(f"{i}) {tank.name}: {tank.current:.0f} л (свободно {free:.0f} л)")
                to_options.append(tank)
        
        to_choice = input("\nКуда? ")
        if not to_choice.isdigit() or int(to_choice) < 1 or int(to_choice) > len(to_options):
            print("Неверный выбор")
            return
        to_tank = to_options[int(to_choice)-1]
        
        # Сколько перекачать
        can = min(from_tank.current, to_tank.max - to_tank.current)
        print(f"\nМожно перекачать до {can:.0f} л")
        
        liters = input("Сколько литров? ")
        try:
            liters = float(liters)
            if liters <= 0:
                print("Должно быть > 0")
                return
            if liters > can:
                print(f"Слишком много. Максимум: {can:.0f} л")
                return
        except:
            print("Нужно число")
            return
        
        # Подтверждение
        confirm = input(f"\nПерекачать {liters:.0f} л? (д/н): ")
        if confirm.lower() != 'д':
            print("Отмена")
            return
        
        # Перекачиваем
        ok1, msg1 = from_tank.sell(liters)
        if not ok1:
            print(f"Ошибка: {msg1}")
            return
        
        ok2, msg2 = to_tank.add(liters)
        if not ok2:
            # Возвращаем если ошибка
            from_tank.add(liters)
            print(f"Ошибка: {msg2}")
            return
        
        # Запись в историю
        self.add_history('Перекачка',
            f"{liters:.0f} л {fuel_type} из {from_tank.name} в {to_tank.name}")
        
        # Сохраняем
        self.save_system()
        
        print(f"\nУспешно!")
        print(f"{from_tank.name}: {from_tank.current:.0f} л")
        print(f"{to_tank.name}: {to_tank.current:.0f} л")
    
    def menu_7_manage(self):
        """Управляет цистернами (меню 7)"""
        print("\n=== УПРАВЛЕНИЕ ЦИСТЕРНАМИ ===")
        
        print("\n1) Включить цистерну")
        print("2) Выключить цистерну")
        
        action = input("\nЧто сделать? ")
        if action not in ['1', '2']:
            print("Неверный выбор")
            return
        
        if action == '1':
            # Включение
            off_tanks = [t for t in self.tanks.values() if not t.on and not t.low_auto_off]
            if not off_tanks:
                print("\nНет цистерн для включения")
                return
            
            print("\nМожно включить:")
            for i, tank in enumerate(off_tanks, 1):
                print(f"{i}) {tank.name}: {tank.current:.0f} л")
            
            choice = input("\nКакую? ")
            if not choice.isdigit() or int(choice) < 1 or int(choice) > len(off_tanks):
                print("Неверный выбор")
                return
            
            tank = off_tanks[int(choice)-1]
            ok, msg = tank.turn_on()
            if ok:
                print(f"\nУспешно! {msg}")
                self.add_history('Включение', f"Цистерна {tank.name}")
                self.save_system()
            else:
                print(f"\nОшибка: {msg}")
        
        else:
            # Выключение
            on_tanks = [t for t in self.tanks.values() if t.on]
            if not on_tanks:
                print("\nНет цистерн для выключения")
                return
            
            print("\nМожно выключить:")
            for i, tank in enumerate(on_tanks, 1):
                print(f"{i}) {tank.name}: {tank.current:.0f} л")
            
            choice = input("\nКакую? ")
            if not choice.isdigit() or int(choice) < 1 or int(choice) > len(on_tanks):
                print("Неверный выбор")
                return
            
            tank = on_tanks[int(choice)-1]
            ok, msg = tank.turn_off()
            if ok:
                print(f"\nУспешно! {msg}")
                self.add_history('Выключение', f"Цистерна {tank.name}")
                self.save_system()
            else:
                print(f"\nОшибка: {msg}")
    
    def menu_8_columns(self):
        """Показывает состояние колонок (меню 8)"""
        print("\n=== СОСТОЯНИЕ КОЛОНОК ===")
        
        for col in range(1, 9):
            print(f"\nКолонка {col}:")
            for fuel, tank_name in COLUMNS[col].items():
                tank = self.tanks[tank_name]
                if tank.on:
                    status = "+ работает"
                else:
                    if tank.low_auto_off:
                        status = "- не работает (мало топлива)"
                    else:
                        status = "- не работает"
                print(f"  {fuel} -> {tank_name} [{status}]")
    
    def menu_9_emergency(self):
        """Аварийный режим (меню 9)"""
        print("\n=== АВАРИЙНЫЙ РЕЖИМ ===")
        
        if self.emergency:
            print(f"\nАварийный режим активен!")
            print("\n1) Выключить аварийный режим")
            print("2) Назад")
            
            choice = input("\n> ")
            if choice == '1':
                confirm = input("\nВы уверены? (д/н): ")
                if confirm.lower() == 'д':
                    self.emergency = False
                    self.add_history('Авария', "Режим выключен")
                    self.save_system()
                    print("\nАварийный режим выключен")
                    print("Цистерны остались выключенными")
                else:
                    print("Отмена")
        
        else:
            print("\nВНИМАНИЕ! Активация аварийного режима!")
            print("\nЧто будет:")
            print("1. Все цистерны отключатся")
            print("2. Продажи остановятся")
            print("3. Вызовут службы")
            
            confirm = input("\nАктивировать? (д/н): ")
            if confirm.lower() != 'д':
                print("Отмена")
                return
            
            # Включаем аварийный режим
            for tank in self.tanks.values():
                tank.on = False
                tank.low_auto_off = False
            
            self.emergency = True
            self.add_history('Авария', "Режим включен! Вызов 112, 104")
            self.save_system()
            
            print("\nАВАРИЙНЫЙ РЕЖИМ АКТИВИРОВАН!")
            print("Все цистерны отключены")
            print("Вызов: 112, 104")

# ЗАДАНИЕ 6: Главный цикл программы

    def run(self):
        """Запускает программу"""
        print("Система АЗС - загрузка...")
        
        while True:
            # Очистка экрана
            if os.name == 'nt':
                os.system('cls')
            else:
                os.system('clear')
            
            # Заголовок
            print("="*50)
            print("АЗС <<СеверНефть>>")
            print("="*50)
            
            # Предупреждения
            warnings = self.show_warnings()
            if warnings:
                print("\nВНИМАНИЕ:")
                for w in warnings:
                    print(f"  - {w}")
            
            # Меню
            print("\nМЕНЮ:")
            print("1) Обслужить клиента")
            print("2) Цистерны")
            print("3) Пополнить")
            print("4) Статистика")
            print("5) История")
            print("6) Перекачка")
            print("7) Управление цистернами")
            print("8) Колонки")
            print("9) АВАРИЙНЫЙ РЕЖИМ")
            print("0) Выход")
            
            choice = input("\nВыберите: ")
            
            if choice == '0':
                print("\nСохранение...")
                self.save_system()
                print("Выход")
                break
            
            elif choice == '1':
                self.menu_1_sell()
            elif choice == '2':
                self.menu_2_tanks()
            elif choice == '3':
                self.menu_3_refill()
            elif choice == '4':
                self.menu_4_stats()
            elif choice == '5':
                self.menu_5_history()
            elif choice == '6':
                self.menu_6_transfer()
            elif choice == '7':
                self.menu_7_manage()
            elif choice == '8':
                self.menu_8_columns()
            elif choice == '9':
                self.menu_9_emergency()
            else:
                print("Неверный выбор")
            
            input("\nНажмите Enter...")

# ЗАДАНИЕ 7: Запуск программы

if __name__ == "__main__":
    system = AZSSystem()
    system.run()