from flask import Flask, render_template, request
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



@app.route('/creature/<creature_type>')
def render_creatures(creature_type):
    title = creature_type.upper()
    query = "SELECT name, description, origin  FROM creatures WHERE type=?"
    con = create_connection(DATABASE)
    cur = con.cursor()

    cur.execute(query, (title, ))
    creature_list = cur.fetchall()
    con.close()
    return render_template('creatures.html', creatures=creature_list, title=title)


def get_creatures(creature_type):
    title = creature_type.upper()
    query = "SELECT name, description, origin FROM creatures WHERE type=?"
    con = create_connection(DATABASE)
    cur = con.cursor()

    cur.execute(query, (title, ))
    creature_list = cur.fetchall()
    con.close()

    return creature_list

def get_types():
    con=create_connection(DATABASE)
    query="SELECT DISTINCT type from creatures ORDER BY type ASC"
    cur=con.cursor()
    cur.execute(query)
    records = cur.fetchall()
    print(records)
    for i in range(len(records)):
        records[i] = records[i][0]
    print(records)
    return records

@app.route('/search', methods=['GET', 'POST'])
def render_search():
    """Find all records which contain search item
    POST contain search value
    return a rendered page"""
    search = request.form['search']
    title = "Search for " + search
    query = "SELECT name, description FROM creatures WHERE "\
    "name LIKE ? or description LIKE ?"
    search = "%" + search + "%"
    con = create_connection(DATABASE)
    cur = con.cursor()
    cur.execute(query, (search, search))
    creature_list = cur.fetchall()
    con.close()

    return render_template("creatures.html", creatures=creature_list, title=title, types=get_types())






if __name__ == "__main__":
    app.run(debug=True)

