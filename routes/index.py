from flask import render_template

def index_route():
    return render_template('index.html')