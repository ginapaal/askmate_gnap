import psycopg2


def connect_to_db():
    conn = psycopg2.connect("dbname='gina' user='gina' host='localhost' password='thebest'")
    conn.autocommit = True
    return conn
