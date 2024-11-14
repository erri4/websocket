from flask import Flask, Response, render_template, redirect, url_for

app = Flask(__name__)


@app.route('/admin')
def admin() -> str:
    return render_template('console.html')


@app.route('/')
@app.route('/<custom_page>')
def index(custom_page = None) -> (str | Response):
    return render_template('index.html') if custom_page is None else redirect(url_for('index'))
