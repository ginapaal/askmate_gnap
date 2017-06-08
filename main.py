from flask import Flask, render_template, request, redirect, url_for
import query_manager

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
@app.route('/list/<question_id>', methods=["GET", "POST"])
def display_list():
    rows = query_manager.read_from_db(query_manager.connect_to_db())
    return render_template("list.html", table=rows)


@app.route("/new_question", methods=['GET', 'POST'])
def new_question():
    if request.method == 'POST':
        try:
            query_manager.insert_into_question(query_manager.connect_to_db())
            return redirect("/")
        except IndexError:
            return render_template("need_registrate.html")
    else:
        return render_template("ask_a_question.html")


@app.route('/question/<question_id>', methods=['GET', 'POST'])
def display_answer_list(question_id):
    rows_answer = query_manager.give_answer_datas_from_answer_table(question_id)
    question = query_manager.give_question_title(question_id)
    question_body = query_manager.give_question_body(question_id)
    return render_template('answers.html', answer=rows_answer, question_id=question_id, question=question,
                           question_body=question_body)


@app.route("/question/<question_id>/new-answer", methods=["GET", "POST"])
def new_answer(question_id):
    question = query_manager.give_question_title(question_id)
    question_body = query_manager.give_question_body(question_id)
    if request.method == "POST":
        try:
            query_manager.insert_into_answer(query_manager.connect_to_db(), question_id)
            return redirect("/question/" + question_id + "")
        except IndexError:
            return render_template("need_registrate.html")
    else:
        return render_template('write_new_answer.html', question_id=question_id, question=question,
                               question_body=question_body)


@app.route("/question/<question_id>/comments", methods=['POST', 'GET'])
def display_q_comment_list(question_id):
    rows_comments = query_manager.read_from_q_comments(query_manager.connect_to_db(), question_id)
    question = query_manager.give_question_title(question_id)
    question_body = query_manager.give_question_body(question_id)
    return render_template("question_comment.html", comment=rows_comments, question_id=question_id,
                           question=question, question_body=question_body)


@app.route("/question/<question_id>/new-comment", methods=['POST', 'GET'])
def add_new_q_comment(question_id):
    question = query_manager.give_question_title(question_id)
    question_body = query_manager.give_question_body(question_id)

    if request.method == "POST":
        try:
            query_manager.add_q_comment(query_manager.connect_to_db(), question_id)
            return redirect("/question/" + question_id + "/comments")
        except IndexError:
            return render_template("need_registrate.html")
    else:
        return render_template("give_question_comment.html", question_id=question_id, question=question, question_body=question_body)


@app.route("/answer/<answer_id>/comments", methods=['POST', 'GET'])
def display_a_comment_list(answer_id):
    rows_comments = query_manager.read_from_a_comments(query_manager.connect_to_db(), answer_id)
    answer = query_manager.give_answer_comment_list(answer_id)
    return render_template("answer_comment.html", comment=rows_comments, answer_id=answer_id,
                           answer=answer)


@app.route('/answer/<answer_id>/new-comment', methods=["POST", "GET"])
def add_new_a_comment(answer_id):
    answer = query_manager.give_answer_comment_list(answer_id)

    if request.method == "POST":
        try:
            query_manager.add_a_comment(query_manager.connect_to_db(), answer_id)
            return redirect("/answer/" + answer_id + "/comments")
        except IndexError:
            return render_template("need_registrate.html")
    else:
        return render_template("give_answer_comment.html", answer_id=answer_id, answer=answer)


@app.route('/registration', methods=["POST", "GET"])
def create_new_reg_table():
    query_manager.create_registration_table(query_manager.connect_to_db())
    if request.method == 'POST':
        query_manager.add_a_user(query_manager.connect_to_db())
        return redirect("/")
    else:
        return render_template("registration_display.html")


@app.route('/question/<question_id>/<user_id>/vote/vote-up')
def question_voteup(question_id, user_id):
    query_manager.question_vote_like(query_manager.connect_to_db(), question_id, user_id)
    return redirect("/")


@app.route('/question/<question_id>/<user_id>/vote/vote-down')
def question_votedown(question_id, user_id):
    query_manager.question_vote_dislike(query_manager.connect_to_db(), question_id, user_id)
    return redirect("/")


@app.route('/question/<question_id>/<answer_id>/<user_id>/vote/vote-up')
def answer_voteup(question_id, answer_id, user_id):
    query_manager.answer_vote_like(query_manager.connect_to_db(), question_id, answer_id, user_id)
    return redirect(url_for("display_answer_list", question_id=question_id, answer_id=answer_id))


@app.route('/question/<question_id>/<answer_id>/<user_id>/vote/vote-down')
def answer_votedown(question_id, answer_id, user_id):
    query_manager.answer_vote_dislike(query_manager.connect_to_db(), question_id, answer_id, user_id)
    return redirect(url_for("display_answer_list", question_id=question_id, answer_id=answer_id))


@app.route('/users-list', methods=['GET', 'POST'])
def users():
    rows_users = query_manager.list_users(query_manager.connect_to_db())
    return render_template("users_list.html", table=rows_users)


@app.route('/user/<user_id>', methods=['GET', 'POST'])
def user_page(user_id):
    rows_username = query_manager.display_userpage_username_reputation(query_manager.connect_to_db(), user_id)
    rows_user_question = query_manager.display_userpage_questions(query_manager.connect_to_db(), user_id)
    rows_user_answer = query_manager.display_userpage_answer(query_manager.connect_to_db(), user_id)
    rows_user_comment = query_manager.display_userpage_comment(query_manager.connect_to_db(), user_id)
    return render_template("user_page.html", table_username=rows_username, table_user_question=rows_user_question,
                           table_user_answer=rows_user_answer, table_user_comment=rows_user_comment)


@app.route('/question/<question_id>/<answer_id>/<user_id>')
def accept_answer(question_id, answer_id, user_id):
    query_manager.accepted_answer(query_manager.connect_to_db(), answer_id, question_id, user_id)
    return redirect("/question/" + question_id)


@app.route('/question/<question_id>/comments/<comment_id>/delete')
def delete_question_comment(comment_id, question_id):
    query_manager.delete_question_comment(query_manager.connect_to_db(), comment_id)
    return redirect(url_for("display_q_comment_list", question_id=question_id))


@app.route('/question/<question_id>/delete')
def delete_question(question_id):
    query_manager.delete_question(query_manager.connect_to_db(), question_id)
    return redirect(url_for("display_list"))


@app.route('/answer/<answer_id>/delete')
def delete_answer(answer_id):
    question_id = query_manager.delete_answer_row(query_manager.connect_to_db(), answer_id)
    return redirect(url_for("display_answer_list", question_id=question_id))


@app.route('/answer/<answer_id>/comments/<comment_id>/delete')
def delete_answer_comment(comment_id, answer_id):
    query_manager.delete_answer_comment(query_manager.connect_to_db(), comment_id)
    return redirect(url_for("display_a_comment_list", answer_id=answer_id, comment_id=comment_id))


if __name__ == "__main__":
    app.run(debug=True)
