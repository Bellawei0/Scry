from flask import Flask, redirect, render_template, request, url_for, flash
import os

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def login():
    print("a")
    error = None
    if request.method == 'POST':
        print("b")
        if request.form['email'] != 'yourmom@aol.com' or request.form['password'] != '12345678':
            error = 'Invalid Credentials, Please Try Again.'
            flash(error, category=error)
        else:
            return redirect(url_for('home'))
    return render_template('index.html', error = error)

@app.route('/home')
def home():
    return render_template('home.html')

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='0.0.0.0', port=4000)
