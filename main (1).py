from flask import Flask, render_template
import sqlite3
from sqlite3 import Error

app = Flask(__name__)
DATABASE = "mythical_creatures.db"

def create_connection(db_file):
    """
    Creates a connection to the database
    :parameter    db_file - the name of the file
    :returns      connection - a connection to the database
    """
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except Error as e:
        print(e)
    return None


@app.route('/')
def render_home():
    return render_template('index.html')


@app.route('/celestial')
def render_celestial():
    query = "SELECT name, description, origin FROM creatures WHERE type='celestial'"
    con = create_connection(DATABASE)
    cur = con.cursor()

    cur.execute(query)
    creature_list = cur.fetchall()
    con.close()
    return render_template('celestial.html', creatures=creature_list)


@app.route('/terrestrial')
def render_terrestrial():
    query = "SELECT name, description, origin  FROM creatures WHERE type='terrestrial'"
    con = create_connection(DATABASE)
    cur = con.cursor()

    cur.execute(query)
    creature_list = cur.fetchall()
    con.close()
    return render_template('terrestrial.html', creatures=creature_list)


if __name__ == "__main__":
    app.run(debug=True)
