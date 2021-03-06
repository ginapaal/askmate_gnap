from datetime import datetime
from flask import request
import psycopg2
import config
import sys


def connect_to_db():
    try:
        conn = psycopg2.connect("dbname='{}' user='{}' host='localhost' password='{}'".format(
            config.db_name, config.user, config.password))
        conn.autocommit = True
    except psycopg2.Error:
        print("""Connection with database failed. You made a typo in your database name, username or password.
            You should check your config.py""")
        sys.exit(0)
    return conn


def insert_into_question(conn):
    cursor = conn.cursor()
    dt = datetime.now()
    message = request.form["new_question"]
    title = request.form["title"]
    name = request.form["username"]
    cursor.execute("""SELECT id FROM users WHERE username = %s;""", (name,))
    user_id = cursor.fetchall()[0][0]
    cursor.execute("""INSERT INTO question (submission_time, title, message, user_id)
     VALUES (%s,%s,%s,%s);""", (dt, title, message, user_id))


def read_from_db(conn):
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM question ORDER BY submission_time;""", conn)
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
    name = request.form["username"]
    cursor.execute("""SELECT id FROM users WHERE username = %s;""", (name,))
    user_id = cursor.fetchall()[0][0]
    cursor.execute("""INSERT INTO answer (submission_time, question_id, message, user_id)
     VALUES (%s,%s,%s,%s);""", (dt, question_id, message, user_id))


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
    name = request.form["username"]
    cursor.execute("""SELECT id FROM users WHERE username = %s;""", (name,))
    user_id = cursor.fetchall()[0][0]
    cursor.execute("""INSERT INTO comment (question_id, message, submission_time, user_id) VALUES(%s,%s,%s,%s);""",
                   (question_id, message, dt, user_id))


def add_a_comment(conn, answer_id):
    cursor = conn.cursor()
    dt = datetime.now()
    message = request.form["new_comment"]
    name = request.form["username"]
    cursor.execute("""SELECT id FROM users WHERE username = %s;""", (name,))
    user_id = cursor.fetchall()[0][0]
    cursor.execute("""INSERT INTO comment (answer_id, message, submission_time, user_id) VALUES(%s,%s,%s,%s);""",
                   (answer_id, message, dt, user_id))


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
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
  ID serial,
  UserName varchar(255) NOT NULL,
  registration_date TIMESTAMP,
  user_reputation int DEFAULT 0,
  PRIMARY KEY (ID));""")


def add_a_user(conn):
    cursor = conn.cursor()
    dt = datetime.now()
    username = request.form["username"]
    cursor.execute("""INSERT INTO users (username, registration_date) VALUES(%s,%s);""",
                   (username, dt))


def give_answer_datas_from_answer_table(question_id):
    rows_answer = reader_by_id(
        connect_to_db(), """SELECT * FROM answer WHERE question_id=%s ORDER BY id;""", question_id)
    return rows_answer


def give_question_title(question_id):
    question = show_db_item(connect_to_db(), """SELECT title FROM question WHERE id=%s;""", question_id)
    return question


def give_question_body(question_id):
    question_body = show_db_item(connect_to_db(), """SELECT message FROM question WHERE id=%s;""", question_id)
    return question_body


def give_answer_comment_list(answer_id):
    answer = show_db_item(connect_to_db(), """SELECT message FROM answer WHERE id=%s;""", answer_id)
    return answer


def question_vote_like(conn, question_id, user_id):
    cursor = conn.cursor()
    cursor.execute("""UPDATE question SET vote_number=vote_number+1 WHERE id=%s;""", (question_id,))
    cursor.execute("""UPDATE users SET user_reputation=user_reputation+5 WHERE id=%s;""", (user_id,))


def question_vote_dislike(conn, question_id, user_id):
    cursor = conn.cursor()
    cursor.execute("""UPDATE question SET vote_number=vote_number-1 WHERE id=%s;""", (question_id,))
    cursor.execute("""UPDATE users SET user_reputation=user_reputation-2 WHERE id=%s;""", (user_id,))


def answer_vote_like(conn, question_id, answer_id, user_id):
    cursor = conn.cursor()
    cursor.execute("""UPDATE answer SET vote_number=vote_number+1 WHERE (question_id, id)=(%s,%s);""",
                   (question_id, answer_id))
    cursor.execute("""UPDATE users SET user_reputation=user_reputation+10 WHERE id=%s;""", (user_id,))


def answer_vote_dislike(conn, question_id, answer_id, user_id):
    cursor = conn.cursor()
    cursor.execute("""UPDATE answer SET vote_number=vote_number-1 WHERE (question_id, id)=(%s,%s);""",
                   (question_id, answer_id))
    cursor.execute("""UPDATE users SET user_reputation=user_reputation-2 WHERE id=%s;""", (user_id,))


def list_users(conn):
    cursor = conn.cursor()
    cursor.execute("""SELECT username, registration_date, id FROM users;""")
    rows_users = cursor.fetchall()
    return rows_users


def accepted_answer(conn, answer_id, question_id, user_id):
    cursor = conn.cursor()
    cursor.execute("""UPDATE answer SET accept=True WHERE id=%s;""", (answer_id,))
    cursor.execute("""UPDATE users SET user_reputation=user_reputation+15 WHERE id=%s;""", (user_id,))


def delete_question_comment(conn, comment_id):
    cursor = conn.cursor()
    cursor.execute("""DELETE FROM comment WHERE id=%s;""", (comment_id,))


def delete_question(conn, question_id):
    cursor = conn.cursor()
    try:
        cursor.execute("""DELETE FROM question WHERE id=%s;""", (question_id,))
    except psycopg2.Error:
        cursor.execute("""DELETE FROM comment WHERE question_id=%s;""", (question_id,))
        cursor.execute("""DELETE FROM answer WHERE question_id=%s;""", (question_id,))
        cursor.execute("""DELETE FROM question_tag WHERE question_id=%s;""", (question_id,))
        cursor.execute("""DELETE FROM question WHERE id=%s;""", (question_id,))


def delete_answer_row(conn, answer_id):
    cursor = conn.cursor()
    cursor.execute("""SELECT question_id from answer WHERE id=%s;""", (answer_id,))
    question_id = cursor.fetchone()[0]
    cursor.execute("""DELETE FROM answer WHERE id=%s;""", (answer_id,))
    return question_id


def delete_answer_comment(conn, comment_id):
    cursor = conn.cursor()
    print(comment_id)
    cursor.execute("""DELETE FROM comment WHERE id=%s;""", (comment_id,))


def display_userpage_username_reputation(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("""SELECT username, user_reputation
                        FROM users WHERE id=%s ;""", (user_id,))
    username_userreput = cursor.fetchall()
    return username_userreput


def display_userpage_questions(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("""SELECT message
                        FROM question WHERE user_id=%s ;""", (user_id,))
    username_question = cursor.fetchall()
    return username_question


def display_userpage_answer(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("""SELECT message
                        FROM answer WHERE user_id=%s ;""", (user_id,))
    username_answer = cursor.fetchall()
    return username_answer


def display_userpage_comment(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("""SELECT message
                        FROM comment WHERE user_id=%s ;""", (user_id,))
    username_answer = cursor.fetchall()
    return username_answer
