import psycopg2


def connect_to_db():
    conn = psycopg2.connect("dbname='tanacs' user='tanacs' host='localhost' password='buggyanás'")
    conn.autocommit = True
    return conn


def update_db(query, conn):
    cursor = conn.cursor()
    cursor.execute(query)


def print_result(query, conn):
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    return print(rows)


def make_query_readable(rows):
    readable_data = ""
    for item in rows:
        for word in item:
            readable_data += str(word)
            if word != item[-1]:
                readable_data += ", "
        if item != rows[-1]:
            readable_data += " ; "
    return readable_data


def insert_into_questions(conn):
    update_db("""INSERT INTO question VALUES (%s);""", (request.form['new_question']), conn)


def read_from_db(conn):
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM question;""", conn)
    rows = cursor.fetchall()
    print(rows)
    return rows