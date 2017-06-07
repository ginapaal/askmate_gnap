from datetime import datetime
from flask import request
import psycopg2
import config


def connect_to_db():
    conn = psycopg2.connect("dbname='{}' user='{}' host='localhost' password='{}'".format(
        config.db_name, config.user, config.password))
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


def reader_by_id(conn, query, question_id):
    cursor = conn.cursor()
    cursor.execute(query, (question_id,))
    rows = cursor.fetchall()
    return rows


def insert_into_answer(conn, question_id):
    cursor = conn.cursor()
    dt = datetime.now()
    message = request.form["new_answer"]
    cursor.execute("""INSERT INTO answer (submission_time, question_id, message)
     VALUES (%s,%s,%s);""", (dt, question_id, message))


def read_from_q_comments(conn, question_id):
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM comment WHERE question_id=%s;""", (question_id,))
    rows = cursor.fetchall()
    return rows


def read_from_a_comments(conn, answer_id):
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM comment WHERE answer_id=%s;""", (answer_id,))
    rows = cursor.fetchall()
    return rows


def add_q_comment(conn, question_id):
    cursor = conn.cursor()
    dt = datetime.now()
    message = request.form["new_comment"]
    cursor.execute("""INSERT INTO comment (question_id, message, submission_time) VALUES(%s,%s,%s);""",
                   (question_id, message, dt))


def add_a_comment(conn, answer_id):
    cursor = conn.cursor()
    dt = datetime.now()
    message = request.form["new_comment"]
    cursor.execute("""INSERT INTO comment (answer_id, message, submission_time) VALUES(%s,%s,%s);""",
                   (answer_id, message, dt))


def readable_query(query):
    readable = ""
    for item in query:
        for word in item:
            readable += word
    return readable


def show_db_item(conn, query, question_id):
    """
    Makes a query then returns it in readable form.
    """
    query = reader_by_id(conn, query, question_id)
    data = readable_query(query)
    return data


def create_registration_table(conn):
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS Registration (
   ID serial,
   UserName varchar(255) NOT NULL,
   registration_date TIMESTAMP,
   PRIMARY KEY (ID));""")
    try:
        cursor.execute("""ALTER TABLE question
       ADD  user_id  int ;""")
        cursor.execute("""ALTER TABLE answer
       ADD  user_id  int ;""")
        cursor.execute("""ALTER TABLE comment
       ADD  user_id  int ;""")
    except:
        pass


def add_a_user(conn):
    cursor = conn.cursor()
    dt = datetime.now()
    username = request.form["username"]
    cursor.execute("""INSERT INTO registration (username, registration_date) VALUES(%s,%s);""",
                   (username, dt))


def question_vote_like(conn, question_id):
    cursor = conn.cursor()
    cursor.execute("""UPDATE question SET vote_number=vote_number+1 WHERE id=%s;""", (question_id))
    return


def question_vote_dislike(conn, question_id):
    cursor = conn.cursor()
    cursor.execute("""UPDATE question SET vote_number=vote_number-1 WHERE id=%s;""", (question_id))


def answer_vote_like(conn, question_id, answer_id):
    cursor = conn.cursor()
    cursor.execute("""UPDATE answer SET vote_number=vote_number+1 WHERE (question_id, id)=(%s,%s);""",
                   (question_id, answer_id))


def answer_vote_dislike(conn, question_id, answer_id):
    cursor = conn.cursor()
    cursor.execute("""UPDATE answer SET vote_number=vote_number-1 WHERE (question_id, id)=(%s,%s);""",
                   (question_id, answer_id))
