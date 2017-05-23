from flask import Flask, render_template, request, redirect, url_for
from data_manager import *
import csv
import time

app = Flask(__name__)


def linefinder(table, question_id, id_num):

    line = 0

    while line < len(table) - 1 and table[line][id_num] != str(question_id):
        line += 1
    return table[line]


@app.route('/', methods=["GET", "POST"])
@app.route('/list', methods=["GET", "POST"])
def display_list():

    table = read_from_csv("question.csv")
    rev_table = reversed(list(table))
    return render_template("list.html", table=rev_table)


@app.route("/new_question", methods=['GET', 'POST'])
def new_question():

    if request.method == 'POST':
        table = read_from_csv("question.csv")
        timestamp = int(time.time())
        question_list = []
        question_list.append(ID_generator(table))
        question_list.append(timestamp)
        question_list.append(request.form['title'])
        question_list.append(request.form['new_question'])
        table.append(question_list)
        write_to_csv("question.csv", question_list)

        return redirect("/")
    else:
        return render_template("ask_a_question.html")


@app.route('/question/<question_id>', methods=['GET', 'POST'])
def display_answer_list(question_id):

    table = read_from_csv('question.csv')
    answer_table = read_from_csv('answers.csv')
    reverse_answers_timeline = reversed(list(answer_table))
    question_line = linefinder(table, question_id, 0)
    question_title = question_line[2]
    question_msg = question_line[3]

    answer_line = linefinder(answer_table, question_id, 2)
    answer = answer_line[3]

    return render_template('answers.html', answer_table=reverse_answers_timeline, answer=answer, line=answer_line, table=table, question_id=question_id, title=question_title, question_msg=question_msg)


@app.route("/question/<question_id>/new-answer", methods=["GET", "POST"])
def new_answer(question_id):

    if request.method == "POST":
        answer_table = read_from_csv('answers.csv')
        timestamp = int(time.time())
        answer_list = []
        answer_list.append(ID_generator(answer_table))
        answer_list.append(timestamp)
        answer_list.append(question_id)
        answer_list.append(request.form['new_answer'])
        answer_table.append(answer_list)

        write_to_csv('answers.csv', answer_list)

        return redirect("/")
    else:
        return render_template('write_new_answer.html', question_id=question_id)


if __name__ == "__main__":
    app.run(debug=True)
