from flask import *
from data_manager import *

app = Flask(__name__)

@app.route('/', method= 'GET')
@app.route('/list', method= 'GET')
def direct_to_question():

    with read_from_csv('list')

@app.route('/', method= 'GET', 'POST')
@app.route('/list', method='GET','POST')
def display_answer_list()

    table = read_from_csv('answers.csv')
    reverse_answers_timeline = reversed(table)
    return render_table('answers.html', table = reverse_answers_timeline )



@app.route("/new_asnwer", method=["GET", "POST"])
def new_answer():
    if request.method == "POST":
        table = read_from_csv('answers.csv')
        answer_list = []
        answer_list.append(ID_generator(table))
        answer_list.append(request.form['new_answer'])
        table.append(answer_list)
        write_to_csv('answers.csv')
        return render_template("answers.html")
    else:
        return render_template("answers.html")

if __name__ == '__main__':
    app.run(debug=True)
