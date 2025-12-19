#Задание 1
objects = [
    ("Containment Cell A", 4),
    ("Archive Vault", 1),
    ("Bio Lab Sector", 3),
    ("Observation Wing", 2)
]

sorted_objects = sorted(objects, key=lambda x: x[1])
print("Сортировка по уровню угрозы:", sorted_objects)

#Задание 2
staff_shifts = [
    {"name": "Dr. Shaw", "shift_cost": 120, "shifts": 15},
    {"name": "Agent Torres", "shift_cost": 90, "shifts": 22},
    {"name": "Researcher Hall", "shift_cost": 150, "shifts": 10}
]

total_costs = list(map(lambda emp: emp["shift_cost"] * emp["shifts"], staff_shifts))
print("Общая стоимость работы:", total_costs)

max_cost = max(total_costs)
print("Максимальная стоимость:", max_cost)

#Задание 3
personnel = [
    {"name": "Dr. Klein", "clearance": 2},
    {"name": "Agent Brooks", "clearance": 4},
    {"name": "Technician Reed", "clearance": 1}
]

def add_clearance_category(person):
    clearance = person["clearance"]
    if clearance == 1:
        category = "Restricted"
    elif 2 <= clearance <= 3:
        category = "Confidential"
    else:
        category = "Top Secret"
    return {**person, "category": category}

personnel_with_category = list(map(add_clearance_category, personnel))
print("Персонал с категориями допуска:", personnel_with_category)

# Задание 4
zones = [
    {"zone": "Sector-12", "active_from": 8, "active_to": 18},
    {"zone": "Deep Storage", "active_from": 0, "active_to": 24},
    {"zone": "Research Wing", "active_from": 9, "active_to": 17}
]

day_zones = list(filter(lambda z: z["active_from"] >= 8 and z["active_to"] <= 18, zones))
print("Дневные зоны:", day_zones)

#Задание 5
reports = [
    {"author": "Dr. Moss", "text": "Analysis completed. Reference: http://external-archive.net"},
    # ... остальные отчеты
]

import re

# 1. Отбор отчетов со ссылками
reports_with_links = list(filter(lambda r: 'http' in r["text"], reports))
print("Отчеты со ссылками:", reports_with_links)

# 2. Замена ссылок
def remove_links(report):
    new_text = re.sub(r'https?://[^\s]+', '[ДАННЫЕ УДАЛЕНЫ]', report["text"])
    return {**report, "text": new_text}

cleaned_reports = list(map(remove_links, reports_with_links))
print("Очищенные отчеты:", cleaned_reports)
#Задание 6
scp_objects = [
    {"scp": "SCP-096", "class": "Euclid"},
    {"scp": "SCP-173", "class": "Euclid"},
    {"scp": "SCP-055", "class": "Keter"},
    {"scp": "SCP-999", "class": "Safe"},
    {"scp": "SCP-3001", "class": "Keter"}
]

enhanced_containment = list(filter(lambda obj: obj["class"] != "Safe", scp_objects))
print("Объекты с усиленными мерами:", enhanced_containment)
#Задание 7
incidents = [
    {"id": 101, "staff": 4},
    {"id": 102, "staff": 12},
    {"id": 103, "staff": 7},
    {"id": 104, "staff": 20}
]

sorted_incidents = sorted(incidents, key=lambda x: x["staff"], reverse=True)
top_three = sorted_incidents[:3]
print("Три наиболее ресурсоемких инцидента:", top_three)
#Задание 8
protocols = [
    ("Lockdown", 5),
    ("Evacuation", 4),
    ("Data Wipe", 3),
    ("Routine Scan", 1)
]

protocol_strings = list(map(lambda p: f"Protocol {p[0]} - Criticality {p[1]}", protocols))
print("Строки протоколов:", protocol_strings)
#Задание 9
shifts = [6, 12, 8, 24, 10, 4]

filtered_shifts = list(filter(lambda h: 8 <= h <= 12, shifts))
print("Смены от 8 до 12 часов:", filtered_shifts)
#Задание 10
evaluations = [
    {"name": "Agent Cole", "score": 78},
    {"name": "Dr. Weiss", "score": 92},
    {"name": "Technician Moore", "score": 61},
    {"name": "Researcher Lin", "score": 88}
]

best_employee = max(evaluations, key=lambda x: x["score"])
print("Лучший сотрудник:", best_employee["name"], "с баллом", best_employee["score"])
