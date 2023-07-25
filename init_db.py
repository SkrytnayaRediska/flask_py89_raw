import psycopg2


def get_connection(db_name):
    connection = psycopg2.connect(
        dbname=db_name,
        host='127.0.0.1',
        port='5432',
        user='postgres',
        password='12345'
    )
    return connection


with get_connection('py89_blog_raw') as conn:
    with conn.cursor() as cursor:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS posts(
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP)
            """
        )
        conn.commit()
        cursor.execute("""
                INSERT INTO posts (title, content) 
                VALUES ('title1', 'content1'),
                       ('title2', 'content2')
                """)
        conn.commit()
