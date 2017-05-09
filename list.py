from flask import Flask, render_template
from data_manager import *
import csv

app = Flask(__name__)


@app.route('/', methods=["GET"])
@app.route('/list', methods=["GET"])
def display_list():
    table = read_from_csv("question.csv")
    return render_template("list.html", table=table)


if __name__ == "__main__":
    app.run(debug=True)
