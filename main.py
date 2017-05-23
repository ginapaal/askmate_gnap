from flask import Flask, render_template, request, redirect, url_for
import query_manager
import csv
import time

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
@app.route('/list', methods=["GET", "POST"])
def display_list():
    rows = query_manager.read_from_db(query_manager.connect_to_db())
    return render_template("list.html", table=rows)


@app.route("/new_question", methods=['GET', 'POST'])
def new_question():
    if request.method == 'POST':
        query_manager.insert_into_question(query_manager.connect_to_db())
        return redirect("/")
    else:
        return render_template("ask_a_question.html")


@app.route('/question/<question_id>', methods=['GET', 'POST'])
def display_answer_list(question_id):

    rows_answer = query_manager.read_from_answer(query_manager.connect_to_db(), question_id)
    rows_question = query_manager.read_from_question(query_manager.connect_to_db(), question_id)
    if rows_answer == []:
        rows_answer = ""

    return render_template('answers.html', answer=rows_answer, question_id=question_id, question=rows_question[0][4])


@app.route("/question/<question_id>/new-answer", methods=["GET", "POST"])
def new_answer(question_id):

    if request.method == "POST":

        query_manager.insert_into_answer(query_manager.connect_to_db(), question_id)
        return redirect("/")
    else:
        print(question_id)
        return render_template('write_new_answer.html', question_id=question_id)


if __name__ == "__main__":
    app.run(debug=True)
