from pathlib import Path

from connect import get_connection


BASE_DIR = Path(__file__).resolve().parent


def _execute_sql_file(filename: str) -> None:
    sql = (BASE_DIR / filename).read_text(encoding="utf-8")
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
        conn.commit()


def create_table_if_missing() -> None:
    ddl = """
    CREATE TABLE IF NOT EXISTS phonebook (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        surname VARCHAR(100),
        phone VARCHAR(20) NOT NULL UNIQUE
    );
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(ddl)
        conn.commit()


def create_db_objects() -> None:
    create_table_if_missing()
    _execute_sql_file("functions.sql")
    _execute_sql_file("procedures.sql")


def search_records(pattern: str):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM search_phonebook(%s);", (pattern,))
            return cur.fetchall()


def upsert_single_user(name: str, phone: str) -> None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("CALL upsert_user(%s, %s);", (name, phone))
        conn.commit()


def upsert_many_users(users):
    names = [name for name, _ in users]
    phones = [phone for _, phone in users]

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "CALL upsert_many_users(%s, %s, %s);",
                (names, phones, []),
            )
            row = cur.fetchone()
        conn.commit()

    if not row:
        return []
    return row[0]


def get_paginated(limit: int, offset: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM get_phonebook_page(%s, %s);", (limit, offset))
            return cur.fetchall()


def delete_user(username: str | None = None, phone: str | None = None) -> None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("CALL delete_from_phonebook(%s, %s);", (username, phone))
        conn.commit()


if __name__ == "__main__":
    create_db_objects()

    upsert_single_user("Alice", "+77001234567")
    upsert_single_user("Bob", "+77004567890")
    upsert_single_user("Alice", "+77009998877")

    invalid = upsert_many_users(
        [
            ("Charlie", "+77001112233"),
            ("Diana", "INVALID_PHONE"),
            ("Eve", "+77002223344"),
        ]
    )

    print("Search for 'Ali':", search_records("Ali"))
    print("Page limit=2 offset=0:", get_paginated(2, 0))
    print("Incorrect data from batch insert:", invalid)

    delete_user(username="Bob")
    delete_user(phone="+77002223344")

    print("All records after delete:", get_paginated(100, 0))
