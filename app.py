from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/employer/<name>')
def employer(name):
    return render_template('employer.html', name=name)


@app.route('/employers/')
def employers():
    return render_template('employers.html')


@app.route('/user/')
@app.route('/user/<username>')
def profile(username):
    return render_template('userProfile.html', username=username)


@app.route('/about/')
def about():
    return render_template('about.html')


@app.route('/login/')
def login():
    return render_template('login.html')


if __name__ == '__main__':
    app.run()
