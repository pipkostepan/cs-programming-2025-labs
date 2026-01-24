# Система управления автозаправочной станцией (АЗС)

import json
import os
from datetime import datetime

# Файлы данных
TANKS_FILE = "tanks.json"
STATS_FILE = "stats.json"
HISTORY_FILE = "history.json"
SYSTEM_FILE = "system.json"  # ← НОВОЕ: для хранения состояния аварии

# Цены на топливо (руб/л)
PRICES = {
    "АИ-92": 72.2,
    "АИ-95": 73.3,
    "АИ-98": 78.7,
    "ДТ": 84.0
}
