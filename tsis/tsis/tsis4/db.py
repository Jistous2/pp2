import psycopg2
from config import db_config

def get_connection():
    """Подключение к базе данных"""
    try:
        conn = psycopg2.connect(**db_config)
        return conn
    except Exception as e:
        print("Ошибка подключения к БД:", e)
        return None

def init_db():
    """Создает таблицы, если они еще не существуют"""
    conn = get_connection()
    if not conn: return
    
    try:
        with conn.cursor() as cur:
            cur.execute('''
                CREATE TABLE IF NOT EXISTS players (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL
                );
            ''')
            cur.execute('''
                CREATE TABLE IF NOT EXISTS game_sessions (
                    id SERIAL PRIMARY KEY,
                    player_id INTEGER REFERENCES players(id),
                    score INTEGER NOT NULL,
                    level_reached INTEGER NOT NULL,
                    played_at TIMESTAMP DEFAULT NOW()
                );
            ''')
            conn.commit()
            print("Таблицы базы данных успешно проверены/созданы.")
    except Exception as e:
        print("Ошибка при создании таблиц:", e)
    finally:
        conn.close()

def save_score(username, score, level):
    """Сохраняет результат игры для конкретного пользователя"""
    conn = get_connection()
    if not conn: return

    try:
        with conn.cursor() as cur:
            # 1. Проверяем, есть ли такой игрок, если нет - добавляем
            cur.execute("SELECT id FROM players WHERE username = %s;", (username,))
            result = cur.fetchone()
            
            if result:
                player_id = result[0]
            else:
                cur.execute("INSERT INTO players (username) VALUES (%s) RETURNING id;", (username,))
                player_id = cur.fetchone()[0]

            # 2. Сохраняем результат (игровую сессию)
            cur.execute('''
                INSERT INTO game_sessions (player_id, score, level_reached)
                VALUES (%s, %s, %s);
            ''', (player_id, score, level))
            
            conn.commit()
    except Exception as e:
        print("Ошибка при сохранении результата:", e)
    finally:
        conn.close()

def get_top_10():
    """Получает Топ-10 результатов за все время"""
    conn = get_connection()
    if not conn: return []

    try:
        with conn.cursor() as cur:
            cur.execute('''
                SELECT p.username, s.score, s.level_reached, s.played_at
                FROM game_sessions s
                JOIN players p ON s.player_id = p.id
                ORDER BY s.score DESC
                LIMIT 10;
            ''')
            return cur.fetchall()
    except Exception as e:
        print("Ошибка при получении Топ-10:", e)
        return []
    finally:
        conn.close()

def get_personal_best(username):
    """Получает лучший результат конкретного игрока"""
    conn = get_connection()
    if not conn: return 0

    try:
        with conn.cursor() as cur:
            cur.execute('''
                SELECT MAX(s.score)
                FROM game_sessions s
                JOIN players p ON s.player_id = p.id
                WHERE p.username = %s;
            ''', (username,))
            result = cur.fetchone()
            return result[0] if result and result[0] is not None else 0
    except Exception as e:
        print("Ошибка при получении лучшего результата:", e)
        return 0
    finally:
        conn.close()

if __name__ == "__main__":
    # Проверка работы базы при запуске файла напрямую
    init_db()
