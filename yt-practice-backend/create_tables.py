from app.db import get_connection


def create_tables():
    with open("app/schema.sql", "r") as file:
        sql = file.read()

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
        conn.commit()

    print("Tables created successfully.")


if __name__ == "__main__":
    create_tables()