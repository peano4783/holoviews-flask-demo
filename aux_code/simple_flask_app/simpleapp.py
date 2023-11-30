"""
Simple Flask application
"""

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index_page():
    greeting = ''
    if request.method == 'POST':
        username = request.form.get('user_name')
        greeting = 'Hello ' + username + '!'

    return render_template('index.html',
                           title='Simple Flask application',
                           greeting=greeting)

if __name__ == '__main__':
    app.run(debug=True)