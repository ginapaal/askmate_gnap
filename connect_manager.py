import psycopg2


def connect_to_db():
    conn = psycopg2.connect("dbname='matraiv' user='matraiv' host='localhost' password='1989matraiv17'")
    conn.autocommit = True
    return conn
