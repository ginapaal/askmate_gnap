import psycopg2
from datetime import datetime
from flask import request


def connect_to_db():
    conn = psycopg2.connect("dbname='matraiv' user='matraiv' host='localhost' password='1989matraiv17'")
    conn.autocommit = True
    return conn


def insert_into_question(conn):
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


def read_from_question(conn, question_id):
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM question WHERE id=%s;""", (question_id))
    rows = cursor.fetchall()
    return rows


def read_from_answer(conn, question_id):
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM answer WHERE question_id=%s;""", (question_id))
    rows = cursor.fetchall()
    return rows


def insert_into_answer(conn, question_id):
    cursor = conn.cursor()
    dt = datetime.now()
    message = request.form["new_answer"]
    cursor.execute("""INSERT INTO answer (submission_time, question_id, message)
     VALUES (%s,%s,%s);""", (dt, question_id, message))
