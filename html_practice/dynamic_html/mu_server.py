#! /usr/bin/python3

from flask import Flask, render_template, url_for, request

app = Flask(__name__)

navbar = """<a href="/">Index</a> <a href="/page1">Page 1</a> <a href="/page2">Page 2</a>"""

form_input = [
    ('Tyler', 'Alb', 'Prez'),
    ('Lily', 'Vaughn', 'Vice Prez')
]

@app.route('/', methods = ['GET'])
def index():
    first = request.args.get('FirstName')
    last = request.args.get('LastName')
    position = request.args.get('BoardPosition')

    if first is not None and last is not None and position is not None:
        print(request.args)
        form_input.append(
            (
                request.args.get('FirstName'),
                request.args.get('LastName'),
                request.args.get('BoardPosition')
            )
        )
    return render_template("mu_base.html", navbar=navbar)

@app.route('/page1')
def renderPage1():
    output = render_template('mu_page1.html', entries = form_input, navbar=navbar)
    return output 


if __name__ == '__main__':
    app.run(port=8000, host="0.0.0.0")