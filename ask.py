from flask import Flask, render_template, request
from data_manager import *
import csv

app = Flask(__name__)


@app.route('/', methods=["GET"])
@app.route('/list', methods=["GET"])
def display_list():
    table = read_from_csv("question.csv")
    return render_template("list.html", table=table)


@app.route("/new_question", methods=['GET', 'POST'])
def new_question():
    if request.method == 'POST':
        table = read_from_csv("question.csv")
        question_list = []
        question_list.append(ID_generator(table))
        question_list.append(1)
        question_list.append(request.form['title'])
        question_list.append(request.form['new_question'])
        table.append(question_list)
        write_to_csv("question.csv", question_list)

        return render_template("list.html", table=table)
    else:
        return render_template("ask_a_question.html")


if __name__ == "__main__":
    app.run(debug=True)
