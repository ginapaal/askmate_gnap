from flask import Flask, render_template, request, redirect, url_for
import query_manager
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
    rows = query_manager.read_from_db(query_manager.connect_to_db())
    return render_template("list.html", table=rows)


@app.route("/new_question", methods=['GET', 'POST'])
def new_question():

    if request.method == 'POST':
        query_manager.insert_into_questions(query_manager.connect_to_db())
        return redirect("/")
    else:
        return render_template("ask_a_question.html")


@app.route('/question/<question_id>', methods=['GET', 'POST'])
def display_answer_list(question_id):

    rows_answer = query_manager.read_from_answer(query_manager.connect_to_db(), question_id)
    rows_correct = rows_answer[0][4]

    return render_template('answers.html', answer=rows_correct)


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
