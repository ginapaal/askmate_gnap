from flask import Flask, render_template, request, redirect
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

        return redirect("/")
    else:
        return render_template("ask_a_question.html")

@app.route('/question/<question_id>', methods=['GET','POST'])
def display_answer_list(question_id):
    
    table = read_from_csv('answers.csv')
    reverse_answers_timeline = reversed(list(table))
    return render_template('answers.html', table=reverse_answers_timeline, question_id=question_id)

@app.route("/question/<question_id>/new-answer", methods=["GET", "POST"])
def new_answer(question_id):
    
    if request.method == "POST":
        table = read_from_csv('answers.csv')
        answer_list = []
        timestamp = int(time.time())
        answer_list.append(ID_generator(table))
        answer_list.append(timestamp)
        answer_list.append(question_id)
        answer_list.append(request.form['new_answer'])
        table.append(answer_list)
        write_to_csv('answers.csv', table)
        
        return redirect('/question/<question_id>')
    else:
        return render_template('write_new_answer.html')


if __name__ == "__main__":
    app.run(debug=True)
