from flask import Flask, render_template, request
from jinja2 import Template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.sqlite"


db = SQLAlchemy(app)
@app.route('/')
def hello_world():  # put application's code here
    return render_template("base.html")




@app.route('/experiment/', methods=['POST'])
def experiment():
    data = request.get_json()


if __name__ == '__main__':
    app.run()

