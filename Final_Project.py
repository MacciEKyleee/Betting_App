import os
import sqlite3

from flask import Flask, render_template, session, redirect

from auth import auth_bp
from db import database_bp
from forms.forms import forms_bp
from db_utils import get_all_information_matches, get_connection, get_all_results


app = Flask(__name__)

# https://flask.palletsprojects.com/en/1.1.x/config/#configuring-from-environment-variables
SECRET_KEY = os.environ.get("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("No SECRET_KEY set for Flask application")

app.secret_key = SECRET_KEY

app.register_blueprint(auth_bp)
app.register_blueprint(database_bp)
app.register_blueprint(forms_bp)


@app.route('/')
def index():
    matches = get_all_information_matches()
    results = get_all_results()
    username = session.get('username')

    conn = get_connection()
    c = conn.cursor()

    query = c.execute('SELECT * FROM "users" WHERE username = ?', (username,))
    user_data = str(query.fetchall())

    query_2 = c.execute('SELECT "points" FROM "final" WHERE "user_id" = ?', (username,))
    user_points = str(query_2.fetchall())

    context = {
        'id': session.get('user_id'),
        'username': session.get('username'),
        'is_admin': session.get('is_admin'),
        'points': user_points,
        'matches': matches,
        'results': results
    }

    return render_template('index.html', **context)


@app.route('/add/<int:indeks>')
def matches(indeks):
    matches = get_all_information_matches()

    indeks = int(indeks)

    context = {
        'id': session.get('user_id'),
        'username': session.get('username'),
        'match_id': indeks,
        'matches': matches
    }

    return render_template('add.html', **context)


@app.route('/result_form')
def result():
    matches = get_all_information_matches()
    results = get_all_results()
    username = session.get('username')

    conn = get_connection()
    c = conn.cursor()

    query = c.execute('SELECT * FROM "users" WHERE username = ?', (username,))
    user_data = query.fetchone()

    context = {
        'id': session.get('user_id'),
        'username': session.get('username'),
        'is_admin': user_data['is_admin'],
        'matches': matches,
        'results': results
    }

    return render_template('result.html', **context)


@app.route('/result_form/<int:indeks>')
def add_result(indeks):
    matches = get_all_information_matches()
    results = get_all_results()
    username = session.get('username')

    indeks = int(indeks)

    conn = get_connection()
    c = conn.cursor()

    query = c.execute('SELECT * FROM "users" WHERE username = ?', (username,))
    user_data = query.fetchone()

    context = {
        'id': session.get('user_id'),
        'username': session.get('username'),
        'is_admin': user_data['is_admin'],
        'matches': matches,
        'match_id': indeks,
        'results': results
    }

    return render_template('add_match_result.html', **context)


if __name__ == '__main__':
    app.run(debug=True)