import psycopg2


def connect_to_db():
    conn = psycopg2.connect("dbname='galdonyi' user='galdonyi' host='localhost' password='orrpolip1'")
    conn.autocommit = True
    return conn
