import psycopg2


def connect_to_db():
    conn = psycopg2.connect("dbname='tanacs' user='tanacs' host='localhost' password='buggyanás'")
    conn.autocommit = True
    return conn
