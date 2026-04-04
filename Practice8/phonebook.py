from pathlib import Path

from connect import get_connection


BASE_DIR = Path(__file__).resolve().parent


def _exec(sql: str, params=(), fetch: bool = False):
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(sql, params)
        return cur.fetchall() if fetch else None


def _load_sql(filename: str) -> None:
    _exec((BASE_DIR / filename).read_text(encoding="utf-8"))


def init_db() -> None:
    _exec(
        """
    CREATE TABLE IF NOT EXISTS phonebook (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        surname VARCHAR(100),
        phone VARCHAR(20) NOT NULL UNIQUE
    );
    """
    )
    _load_sql("functions.sql")
    _load_sql("procedures.sql")


def search_records(pattern: str):
    return _exec("SELECT * FROM search_phonebook(%s);", (pattern,), fetch=True)


def upsert_user(name: str, phone: str) -> None:
    _exec("CALL upsert_user(%s, %s);", (name, phone))


def upsert_many_users(users):
    if not users:
        return []

    names = [name for name, _ in users]
    phones = [phone for _, phone in users]
    rows = _exec("CALL upsert_many_users(%s, %s, %s);", (names, phones, []), fetch=True)
    return rows[0][0] if rows else []


def get_paginated(limit: int, offset: int):
    return _exec("SELECT * FROM get_phonebook_page(%s, %s);", (limit, offset), fetch=True)


def delete_user(username: str | None = None, phone: str | None = None) -> None:
    _exec("CALL delete_from_phonebook(%s, %s);", (username, phone))


if __name__ == "__main__":
    init_db()

    upsert_user("Alice", "+77001234567")
    upsert_user("Bob", "+77004567890")
    upsert_user("Alice", "+77009998877")

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
