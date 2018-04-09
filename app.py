from flask import Flask, render_template, request, redirect, url_for, flash
from flask.ext.login import (LoginManager, current_user, login_required,
                            login_user, logout_user, UserMixin,
                            confirm_login, fresh_login_required)
from flask_sqlalchemy import SQLAlchemy
import backend
from flask_bootstrap import Bootstrap


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:steve@localhost/theCellar'
db = SQLAlchemy(app)
db.init_app(app)
Bootstrap(app)


class User(UserMixin):
    def __init__(self, name, id, active=True):
        self.name = name
        self.id = id
        self.active = active

    def is_active(self):
        return self.active








@app.route('/')
def index():
    return render_template('index.html')


@app.route('/employer/<name>', methods=['POST', 'GET'])
def employer(name):
    if request.method == 'POST':
        result = request.form
        print(result)
        backend.addReview(result['Name'], result['Review'], int(result['Score']), "ThatOneJerk")
        return render_template('employers.html', result=backend.getCompany())
    return render_template('employer.html', name=name, reviews=backend.getReviews(name))

@app.route('/addReview/<name>')
def addReview(name):
    return render_template('addReview.html', name=name)


@app.route('/employers/', methods=['POST', 'GET'])
def employers():
    if request.method == 'POST':
        print("got your shit")
        result = request.form
        print(result)
        success = backend.addCompany(result['Name'], result['About'])
        if success:
            return render_template('employers.html', result=backend.getCompany())
        else:
            return render_template('error.html', name=result['Name'])
    return render_template('employers.html', result=backend.getCompany())


@app.route('/user/', methods=['POST', 'GET'])
def user():
    if request.method == 'POST':
        result = request.form
        print(result)
        success = backend.addUser(result['display_name'], result['password'], result['email'], result['first_name'], result['last_name'])
        if success:
            return render_template('userProfile.html', username=result['display_name'])
        else:
            return render_template('error.html', name=result['display_name'])

    return render_template('userProfile.html')


@app.route('/user/<display_name>', methods=['POST', 'GET'])
def profile(display_name):
    if request.method == 'POST':
        result = request.form
        print(result)
        success = backend.addUser(result['display_name'], result['password'], result['email'], result['first_name'], result['last_name'])
        if success:
            return render_template('userProfile.html', username=username)
        else:
            return render_template('error.html', name=result['display_name'])

@app.route('/check/', methods=['POST', 'GET'])
def checkPassword():
    print("Are you here?")
    if request.method == 'POST':
        result = request.form-signin
        print(result)
        success = backend.checkPassword(result['email'], result['password'])
        if success:
            return render_template('userProfile.html', username=result['email'])
        else:
            return render_template('error.html', name=result['email'])
    else:
        print("Not a post?")


@app.route('/about/')
def about():
    return render_template('about.html')


@app.route('/test/')
def test():
    return render_template('test.html')


@app.route('/login/')
def login():
    return render_template('login.html')


@app.route('/signup/')
def signup():
    return render_template('signup.html')


@app.route('/addNewCompany')
def getCompanyName():
    return render_template('companyInput.html')

@app.route('/result',methods = ['POST', 'GET'])
def displayCompany():
    if request.method == 'POST':
        print("got your shit")
        result = request.form
        print(result)
        backend.addCompany(result['Name'], result['About'])
        return " ".join(str(x) for x in backend.getCompany())

if __name__ == '__main__':
    app.run()
