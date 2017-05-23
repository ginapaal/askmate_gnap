import psycopg2
from datetime import datetime
from flask import request


def connect_to_db():
    conn = psycopg2.connect("dbname='galdonyi' user='galdonyi' host='localhost' password='orrpolip1'")
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
    cursor = conn.cursor()
    dt = datetime.now()
    message = request.form["new_question"]
    title = request.form["title"]
    cursor.execute("""INSERT INTO question (submission_time, title, message)
     VALUES (%s,%s,%s);""", (dt, title, message))


def read_from_db(conn):
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM question;""", conn)
    rows = cursor.fetchall()
    return rows


def read_from_answer(conn, question_id):
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM answer WHERE id=%s;""", (question_id))
    rows = cursor.fetchall()
    print(rows)
    return rows
