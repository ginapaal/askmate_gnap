from flask import *
from data_manager import *

app = Flask(__name__)


@app.route("/new_asnwer", methods=["GET", "POST"])
def new_answer():
    if request.method == "POST":
        table = read_from_csv('answers.csv')
        answer_list = []
        answer_list.append(ID_generator(table)(request.form('new_answer'))
        table.append(answer_list)
        write_to_csv('answers.csv')
        return render_template("answers.html")
    else return render_template("answes.html")

if __name__ == '__main__':
    app.run(debug=True)
