#Задание 1
def z1():
    objects = [
        ("Containment Cell A", 4),
        ("Archive Vault", 1),
        ("Bio Lab Sector", 3),
        ("Observation Wing", 2)
    ]
    
    sorted_objects = sorted(objects, key=lambda item: item[1])
    return sorted_objects
#Задание 2
def z2():
    staff_shifts = [
        {"name": "Dr. Shaw", "shift_cost": 120, "shifts": 15},
        {"name": "Agent Torres", "shift_cost": 90, "shifts": 22},
        {"name": "Researcher Hall", "shift_cost": 150, "shifts": 10}
    ]
    
    total_salaries = []
    for worker in staff_shifts:
        total = worker["shift_cost"] * worker["shifts"]
        total_salaries.append(total)
    
    max_salary = max(total_salaries)
    return max_salary
#Задание 3
def z3():
    personnel = [
        {"name": "Dr. Klein", "clearance": 2},
        {"name": "Agent Brooks", "clearance": 4},
        {"name": "Technician Reed", "clearance": 1}
    ]
    
    result = []
    for person in personnel:
        level = person["clearance"]
        
        if level == 1:
            category = "Restricted"
        elif 2 <= level <= 3:
            category = "Confidential"
        else:
            category = "Top Secret"
        
        result.append({
            "name": person["name"],
            "clearance": level,
            "category": category
        })
    
    return result
#Задание 4
def z4():
    zones = [
        {"zone": "Sector-12", "active_from": 8, "active_to": 18},
        {"zone": "Deep Storage", "active_from": 0, "active_to": 24},
        {"zone": "Research Wing", "active_from": 9, "active_to": 17}
    ]
    
    day_zones = []
    for zone in zones:
        start = zone["active_from"]
        end = zone["active_to"]
        
        if start >= 8 and end <= 18:
            day_zones.append(zone)
    
    return day_zones
#Задание 5
def z5():
    reports = [
        {"id": 1, "text": "Объект SCP-173 замечен в коридоре http://scp-wiki.net/scp-173"},
        {"id": 2, "text": "Рутинная проверка оборудования"},
        # ... другие отчеты
    ]
    
    reports_with_links = []
    for report in reports:
        if "http://" in report["text"] or "https://" in report["text"]:
            reports_with_links.append(report.copy())
    
    for report in reports_with_links:
        text = report["text"]
        text = text.replace("http://", "[ДАННЫЕ УДАЛЕНЫ] ")
        text = text.replace("https://", "[ДАННЫЕ УДАЛЕНЫ] ")
        report["text"] = text
    
    return reports_with_links
#Задание 6
def z6():
    scp_objects = [
        {"scp": "SCP-096", "class": "Euclid"},
        {"scp": "SCP-173", "class": "Euclid"},
        {"scp": "SCP-055", "class": "Keter"},
        {"scp": "SCP-999", "class": "Safe"},
        {"scp": "SCP-3001", "class": "Keter"}
    ]
    
    dangerous_scps = []
    for scp in scp_objects:
        if scp["class"] != "Safe":
            dangerous_scps.append(scp)
    
    return dangerous_scps
#Задание 7
def z7():
    incidents = [
        {"id": 101, "staff": 4},
        {"id": 102, "staff": 12},
        {"id": 103, "staff": 7},
        {"id": 104, "staff": 20}
    ]
    
    sorted_incidents = sorted(incidents, key=lambda x: x["staff"], reverse=True)
    biggest_incidents = sorted_incidents[:3]
    
    return biggest_incidents
#Задание 8
def z8():
    protocols = [
        ("Lockdown", 5),
        ("Evacuation", 4),
        ("Data Wipe", 3),
        ("Routine Scan", 1)
    ]
    
    result = []
    for protocol in protocols:
        name, level = protocol
        result.append(f"Protocol {name} - Criticality {level}")
    
    return result
#Задание 9
def z9():
    shifts = [6, 12, 8, 24, 10, 4]
    
    normal_shifts = []
    for hours in shifts:
        if 8 <= hours <= 12:
            normal_shifts.append(hours)
    
    return normal_shifts
#Задание 10
def z10():
    evaluations = [
        {"name": "Agent Cole", "score": 78},
        {"name": "Dr. Weiss", "score": 92},
        {"name": "Technician Moore", "score": 61},
        {"name": "Researcher Lin", "score": 88}
    ]
    
    best_score = 0
    best_employee = ""
    
    for employee in evaluations:
        if employee["score"] > best_score:
            best_score = employee["score"]
            best_employee = employee["name"]
    
    return {"name": best_employee, "score": best_score}