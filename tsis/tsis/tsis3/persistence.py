import json
import os

SETTINGS_FILE = 'settings.json'
LEADERBOARD_FILE = 'leaderboard.json'

DEFAULT_SETTINGS = {
    'sound': True,
    'car_color': 'red',
    'difficulty': 'normal' 
}

def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        return DEFAULT_SETTINGS.copy()
    try:
        with open(SETTINGS_FILE, 'r') as f:
            data = json.load(f)
            for k, v in DEFAULT_SETTINGS.items():
                if k not in data:
                    data[k] = v
            return data
    except:
        return DEFAULT_SETTINGS.copy()

def save_settings(settings):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f, indent=4)

def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    try:
        with open(LEADERBOARD_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

def save_leaderboard(score_entry):
    board = load_leaderboard()
    board.append(score_entry)
    board.sort(key=lambda x: x['score'], reverse=True)
    board = board[:10]
    
    with open(LEADERBOARD_FILE, 'w') as f:
        json.dump(board, f, indent=4)
