from flask import Flask, render_template, url_for, request
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
database_name = "imdb_data" # change to imdb_data for production data



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{quote(username)}:{quote(password)}@{quote(host)}/{quote(database_name)}?charset=utf8mb4"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


@app.route('/')
def index():
    return render_template("index.html")


# fetching details based on original title
@app.route('/<titleId>', methods=['GET'])
def title_details(titleId):
    sql_path = 'SQL/title_details.sql'
    with open(sql_path, 'r') as file:
        query = text(file.read()).params(titleId=titleId)
    result = db.session.execute(query)
    details_result = result.fetchall()
    return render_template('title_details.html', details_result=details_result)

# Feature 6, search title
@app.route('/search_title', methods=['GET', 'POST'])
def search_title():
    search_result = None
    if request.method == 'POST':
        title = request.form['title']
        sql_path = 'SQL/Feature6_search_title.sql'
        with open(sql_path, 'r') as file:
            query = text(file.read()).params(usr_input=f"%{title}%")
        result = db.session.execute(query)
        search_result = result.fetchall()
    return render_template('search_by_title.html', search_result=search_result)


# Feature 1: sort by rating
@app.route('/Sort_by_rating')
def sort_by_rating():
    sql_path = 'SQL/Feature3_sort_by_rating.sql'
    with open(sql_path, 'r') as file:
        query = text(file.read())
    result = db.session.execute(query)
    output = result.fetchall()
    return render_template('sort_by_rating.html', sorted_table = output)

# Feature 4: Top 10 in Genres
@app.route('/Top10_In_Genres')
def Top_Genres():
    genre = request.args.get('genre')
    sql_path = 'SQL/Feature4_Top10_In_Genres.sql'
    with open(sql_path, 'r') as file:
        query = text(file.read())
    result = db.execute(query, {"usr_input": f"%{genre}%"})
    output = result.fetchall()
    return render_template('template.html', sorted_table=output)

if __name__ == "__main__":
    app.run(debug=True)