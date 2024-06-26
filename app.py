from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from urllib.parse import quote
from dotenv import load_dotenv
from sqlalchemy import text
# 'pip install pymysql cryptography' may be a required package for this program to run




# MySQL Creds
load_dotenv(r'./password.env')
host = "localhost"
username = "root"
password = os.getenv('MY_PASSWORD')
database_name = "imdb_dummy"



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{quote(username)}:{quote(password)}@{quote(host)}/{quote(database_name)}?charset=utf8mb4"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


@app.route('/')
def index():
    return render_template("index.html")

# print full title_akas
@app.route('/title_akas')
def show_title_akas():
    result = db.session.execute(text('SELECT * FROM title_akas'))
    title_akas_entries = result.fetchall()
    return render_template('title_akas.html', title_akas_entries=title_akas_entries)

# Feature 1: sort by rating
@app.route('/Sort_by_rating')
def sort_by_rating():
    sql_path = 'SQL/Feature3_sort_by_rating.sql'
    with open(sql_path, 'r') as file:
        query = text(file.read())
    result = db.session.execute(query)
    output = result.fetchall()
    return render_template('sort_by_rating.html', sorted_table = output)
    

if __name__ == "__main__":
    app.run(debug=True)