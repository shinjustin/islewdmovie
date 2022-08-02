from flask import Flask, render_template, redirect, url_for, request
from islewdmovie import search_media, get_parents_guide
from datetime import datetime

app = Flask(__name__)

@app.context_processor
def this_year():
    now = datetime.now()
    this_year = datetime.strftime(now, '%Y')
    return dict(this_year=this_year)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search/', methods=['GET', 'POST'])
def search_post():
    if request.method == 'POST':
        query = request.form['query']
        query = query.replace(' ', '%20')
        return redirect(url_for('search', query=query))
    else:
        return redirect(url_for('index'))

@app.route('/search/<query>')
def search(query=None):
    results = search_media(query)
    results = results['d']
    return render_template('search.html', results=results)

@app.route('/result/<tid>')
def result(tid):
    results = get_parents_guide(tid)
    return render_template('result.html', results=results)
