from flask import Flask, render_template, request, redirect, url_for
import query_manager
from connect_manager import connect_to_db

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
@app.route('/list', methods=["GET", "POST"])
def display_list():
    rows = query_manager.read_from_db(connect_to_db())
    return render_template("list.html", table=rows)


@app.route("/new_question", methods=['GET', 'POST'])
def new_question():
    if request.method == 'POST':
        query_manager.insert_into_question(connect_to_db())
        return redirect("/")
    else:
        return render_template("ask_a_question.html")


@app.route('/question/<question_id>', methods=['GET', 'POST'])
def display_answer_list(question_id):

    rows_answer = query_manager.reader_by_id(
        connect_to_db(), """SELECT * FROM answer WHERE question_id=%s;""", question_id)
    question = query_manager.show_db_item(connect_to_db(), """SELECT title FROM question WHERE id=%s;""", question_id)
    question_body = query_manager.show_db_item(
        connect_to_db(), """SELECT message FROM question WHERE id=%s;""", question_id)
    return render_template('answers.html', answer=rows_answer, question_id=question_id, question=question,
                           question_body=question_body)


@app.route("/question/<question_id>/new-answer", methods=["GET", "POST"])
def new_answer(question_id):

    question = query_manager.show_db_item(connect_to_db(), """SELECT title FROM question WHERE id=%s;""", question_id)
    question_body = query_manager.show_db_item(
        connect_to_db(), """SELECT message FROM question WHERE id=%s;""", question_id)
    if request.method == "POST":

        query_manager.insert_into_answer(connect_to_db(), question_id)
        return redirect("/question/" + question_id + "")
    else:
        return render_template('write_new_answer.html', question_id=question_id, question=question,
                               question_body=question_body)


@app.route("/question/<question_id>/comments", methods=['POST', 'GET'])
def display_comment_list(question_id):
    rows_comments = query_manager.read_from_q_comments(connect_to_db(), question_id)
    question = query_manager.show_db_item(connect_to_db(), """SELECT title FROM question WHERE id=%s;""", question_id)
    question_body = query_manager.show_db_item(
        connect_to_db(), """SELECT message FROM question WHERE id=%s;""", question_id)
    return render_template("question_comment.html", comment=rows_comments, question_id=question_id,
                           question=question, question_body=question_body)


@app.route("/question/<question_id>/new-comment", methods=['POST', 'GET'])
def add_new_q_comment(question_id):
    question = query_manager.show_db_item(connect_to_db(), """SELECT title FROM question WHERE id=%s;""", question_id)
    question_body = query_manager.show_db_item(
        connect_to_db(), """SELECT message FROM question WHERE id=%s;""", question_id)
    if request.method == "POST":
        query_manager.add_q_comment(connect_to_db(), question_id)
        return redirect("/question/" + question_id + "/comments")
    else:
        return render_template("give_question_comment.html", question_id=question_id, question=question, question_body=question_body)


@app.route("/answer/<answer_id>/comments", methods=['POST', 'GET'])
def display_a_comment_list(answer_id):
    rows_comments = query_manager.read_from_a_comments(connect_to_db(), answer_id)
    answer = query_manager.show_db_item(connect_to_db(), """SELECT message FROM answer WHERE id=%s;""", answer_id)
    return render_template("answer_comment.html", comment=rows_comments, answer_id=answer_id,
                           answer=answer)


@app.route('/answer/<answer_id>/new-comment', methods=["POST", "GET"])
def add_new_a_comment(answer_id):
    answer = query_manager.show_db_item(
        connect_to_db(), """SELECT message FROM answer WHERE id=%s;""", answer_id)

    if request.method == "POST":
        query_manager.add_a_comment(connect_to_db(), answer_id)
        return redirect("/answer/" + answer_id + "/comments")
    else:
        return render_template("give_answer_comment.html", answer_id=answer_id, answer=answer)


if __name__ == "__main__":
    app.run(debug=True)
