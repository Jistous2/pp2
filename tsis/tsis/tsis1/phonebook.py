import psycopg2
import csv
import json
import os
from connect import get_connection


def add_new_contact():
    print("\n--- Новый контакт ---")
    fname = input("Имя: ")
    lname = input("Фамилия: ")
    email = input("Email (или Enter): ") or None
    bday = input("День рождения (ГГГГ-ММ-ДД или Enter): ") or None
    group = input("Группа: ")
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO groups (name) VALUES (%s) ON CONFLICT DO NOTHING", (group,))
            cur.execute("SELECT id FROM groups WHERE name = %s", (group,))
            g_id = cur.fetchone()[0]
            cur.execute("INSERT INTO contacts (first_name, last_name, email, birthday, group_id) VALUES (%s,%s,%s,%s,%s) RETURNING id",
                        (fname, lname, email, bday, g_id))
            conn.commit()
    print("Контакт создан.")


def add_phone_to_contact():
    name = input("Имя контакта: ")
    phone = input("Номер: ")
    ptype = input("Тип (home/work/mobile): ")
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, ptype))
            conn.commit()
    print("Телефон добавлен.")


def change_contact_group():
    name = input("Имя контакта: ")
    group = input("Новая группа: ")
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("CALL move_to_group(%s, %s)", (name, group))
            conn.commit()
    print("Группа обновлена.")


def filter_by_group():
    group = input("Название группы: ")
    query = "SELECT c.first_name, c.last_name FROM contacts c JOIN groups g ON c.group_id = g.id WHERE g.name = %s"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (group,))
            for row in cur.fetchall():
                print(f"- {row[0]} {row[1]}")


def search_by_email():
    part = input("Введите часть email: ")
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT first_name, email FROM contacts WHERE email ILIKE %s", (f"%{part}%",))
            for row in cur.fetchall():
                print(f"{row[0]}: {row[1]}")


def sort_contacts():
    print("Сортировать по: 1. Имени, 2. Дню рождения, 3. Дате добавления")
    mode = input("> ")
    cols = {"1": "first_name", "2": "birthday", "3": "created_at"}
    col = cols.get(mode, "first_name")
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(f"SELECT first_name, last_name, birthday FROM contacts ORDER BY {col}")
            for row in cur.fetchall():
                print(row)


def paginated_view():
    offset = 0
    limit = 3
    while True:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT first_name, last_name FROM contacts LIMIT %s OFFSET %s", (limit, offset))
                rows = cur.fetchall()
                print("\n--- Список ---")
                for r in rows:
                    print(f"{r[0]} {r[1]}")
                cmd = input("\n[n] След., [p] Пред., [q] Выход: ").lower()
                if cmd == 'n':
                    offset += limit
                elif cmd == 'p':
                    offset = max(0, offset - limit)
                elif cmd == 'q':
                    break


def export_json():
    query = """
        SELECT c.first_name, c.last_name, c.email, c.birthday, g.name,
               ARRAY_AGG(p.phone || '(' || p.type || ')')
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        GROUP BY c.id, g.name
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            data = [{"name": r[0], "last": r[1], "email": r[2], "bday": str(r[3]), "group": r[4], "phones": r[5]} for r in cur.fetchall()]
            with open("contacts.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
    print("Данные сохранены в contacts.json")


def import_json():
    file = input("Имя JSON файла: ")
    if not os.path.exists(file):
        return
    with open(file, "r") as f:
        data = json.load(f)
    with get_connection() as conn:
        with conn.cursor() as cur:
            for item in data:
                cur.execute("SELECT id FROM contacts WHERE first_name = %s", (item['name'],))
                exists = cur.fetchone()
                action = 'i'
                if exists:
                    action = input(f"Контакт {item['name']} существует. (s)кип / (o)веррайт? ")
                if action == 's':
                    continue
                if action == 'o':
                    cur.execute("DELETE FROM contacts WHERE id = %s", (exists[0],))
                cur.execute("INSERT INTO contacts (first_name, last_name, email, birthday) VALUES (%s,%s,%s,%s)",
                            (item['name'], item['last'], item['email'], item['bday'] if item['bday'] != 'None' else None))
            conn.commit()
    print("Импорт завершен.")


def import_csv():
    file = input("Имя CSV файла: ")
    with open(file, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        with get_connection() as conn:
            with conn.cursor() as cur:
                for r in reader:
                    cur.execute("INSERT INTO groups (name) VALUES (%s) ON CONFLICT DO NOTHING", (r['group'],))
                    cur.execute("SELECT id FROM groups WHERE name = %s", (r['group'],))
                    g_id = cur.fetchone()[0]
                    cur.execute("INSERT INTO contacts (first_name, last_name, email, birthday, group_id) VALUES (%s,%s,%s,%s,%s)",
                                (r['first_name'], r['last_name'], r['email'], r['birthday'], g_id))
            conn.commit()


def main():
    menu = {
        "1": add_new_contact,
        "2": add_phone_to_contact,
        "3": change_contact_group,
        "4": filter_by_group,
        "5": search_by_email,
        "6": sort_contacts,
        "7": paginated_view,
        "8": export_json,
        "9": import_json,
        "10": import_csv
    }
    while True:
        print("\n--- PhoneBook Меню ---")
        print("1. Добавить контакт      2. Добавить телефон     3. Сменить группу")
        print("4. Фильтр по группе      5. Поиск по Email       6. Сортировка")
        print("7. Постраничный просмотр 8. Экспорт JSON         9. Импорт JSON")
        print("10. Импорт CSV           0. Выход")
        choice = input("\nВыберите действие: ")
        if choice == "0":
            break
        if choice in menu:
            menu[choice]()


if __name__ == "__main__":
    main()
