from flask import Flask, render_template, request
from data_manager import *
import csv
import time

app = Flask(__name__)


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

        return render_template("list.html", table=table)
    else:
        return render_template("ask_a_question.html")


if __name__ == "__main__":
    app.run(debug=True)
