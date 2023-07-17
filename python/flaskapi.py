import os
from flask import render_template, request, redirect, url_for, Flask
import psycopg2

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(host=os.getenv("POSTGRES_SERVICE_HOST"), 
                            database=os.getenv("db_name"), 
                            user='postgres', 
                            password=os.getenv("db_root_password"))

def get_table():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM person;')
    person = cur.fetchall()
    cur.close()
    conn.close()
    return(person)

@app.route("/")
def home_page():   
    return render_template("home_page.html")

@app.route("/table")
def show_table():
    return render_template("table_page.html", person=get_table())

@app.route("/add", methods=('GET', 'POST'))
def add_page():
    if (request.method == 'POST'):

        fname = request.form['fname']
        lname = request.form['lname']
        gender = request.form['gender']
        date = request.form['bdate']
        email = None if request.form['email'] == "" else request.form['email']
        country = request.form['bcountry']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO person (first_name, last_name, gender, date_of_birth, email, country_fo_birth)'
                    'VALUES (%s, %s, %s, %s, %s, %s)', (fname, lname, gender, date, email, country))           
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('add_page'))
    return render_template("add_page.html")

@app.route("/delete", methods=('GET', 'POST'))
def delete_row():
    if (request.method == 'POST'):
        conn = get_db_connection()
        cur = conn.cursor()
        ids = request.form.getlist('id')
        for id in ids :
            cur.execute('DELETE FROM person WHERE id = (%s)', (id,))             
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('delete_row'))
    return render_template("delete_page.html", person=get_table())
      
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)