import json
import os

SETTINGS_FILE = 'settings.json'

DEFAULT_SETTINGS = {
    'snake_color': [0, 255, 0], # Green (RGB)
    'grid_overlay': True,
    'sound': True
}

def load_settings():
    """Загружает настройки из файла JSON или создает стандартные"""
    if not os.path.exists(SETTINGS_FILE):
        return DEFAULT_SETTINGS.copy()
    try:
        with open(SETTINGS_FILE, 'r') as f:
            data = json.load(f)
            # Проверяем, что все ключи есть
            for k, v in DEFAULT_SETTINGS.items():
                if k not in data:
                    data[k] = v
            return data
    except Exception as e:
        print("Ошибка загрузки настроек:", e)
        return DEFAULT_SETTINGS.copy()

def save_settings(settings):
    """Сохраняет настройки в файл JSON"""
    try:
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(settings, f, indent=4)
    except Exception as e:
        print("Ошибка сохранения настроек:", e)
