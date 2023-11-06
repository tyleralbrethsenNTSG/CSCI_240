#! /usr/bin/python3

from flask import Flask, render_template, url_for, request

app = Flask(__name__)

navbar = """<a href="/">Index</a> <a href="/page1">Page 1</a> <a href="/page2">Page 2</a>"""

form_input = [
    ('Tyler', 'Alb', 'Prez'),
    ('Lily', 'Vaughn', 'Vice Prez')
]

@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        print(request.form)
        form_input.append(
            (
                request.form.get('First Name'),
                request.form.get('Last Name'),
                request.form.get('Board Position')
            )
        )
    return render_template("mu_base.html", navbar=navbar)

@app.route('/page1')
def renderPage1():
    output = render_template('mu_page1.html', entries = form_input, navbar=navbar)
    return output 


if __name__ == '__main__':
    app.run(port=8000, host="0.0.0.0")