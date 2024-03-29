from flask import Flask, render_template, request, redirect, make_response
from flask_bootstrap import Bootstrap
from flask_login import (UserMixin)
from flask_sqlalchemy import SQLAlchemy

import backend

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
    #    resp = render_template('index.html')
    #    resp.set_cookie('FLAG', 'cdc{chocolateChip}')
    return render_template('index.html')


@app.route('/employer/<name>', methods=['POST', 'GET'])
def employer(name):
    if request.cookies.get('loggedIn'):
        if request.method == 'POST':
            result = request.form
            backend.addReview(result['Name'], result['Review'], int(result['Score']), request.cookies.get('username'))
            return render_template('employers.html', result=backend.getCompany())
            # return redirect("http://www.bigcheese.review/employers")#.format(result['Name']))
        # return redirect("http://www.bigcheese.review/employers")
        return render_template('employer.html', name=name, reviews=backend.getReviews(name))
    else:
        return render_template('login.html')


@app.route('/addReview/<name>')
def addReview(name):
    if request.cookies.get('loggedIn'):
        return render_template('addReview.html', name=name)
    else:
        return render_template('login.html')


@app.route('/employers/', methods=['POST', 'GET'])
def employers():
    if request.method == 'POST':

        if request.cookies.get('loggedIn'):
            # print("got your shit")
            result = request.form
            # print(result)
            success = backend.addCompany(result['Name'], result['About'])
            if success:
                where = "http://www.bigcheese.review/employer/{}".format(result['Name'])
                return redirect(where)
            #                return render_template('employer.html', result=backend.getCompany())
            else:
                return render_template('error.html', name=result['Name'])
        else:
            return render_template('login.html')
    return render_template('employers.html', result=backend.getCompany())


@app.route('/user/', methods=['POST', 'GET'])
def user():
    if request.method == 'POST':
        result = request.form
        # print(result)
        success = backend.addUser(result['display_name'], result['password'], result['email'], result['first_name'],
                                  result['last_name'])
        if success:
            return render_template('userProfile.html', username=result['display_name'])
        else:
            return render_template('error.html', name=result['display_name'])

    username = request.cookies.get('username')
    return render_template('userProfile.html', name=username)


@app.route('/user/<display_name>', methods=['POST', 'GET'])
def profile(display_name):
    if request.method == 'POST':
        result = request.form
        # print(result)
        success = backend.addUser(result['display_name'], result['password'], result['email'], result['first_name'],
                                  result['last_name'])
        if success:
            return render_template('userProfile.html', username=username)
        else:
            return render_template('error.html', name=result['display_name'])


@app.route('/check/', methods=['POST', 'GET'])
def checkPassword():
    # print("Are you here?")
    if request.method == 'POST':
        result = request.form
        # print(result)
        success = backend.checkPassword(result['email'], result['password'])
        if success:
            # print(result['email'])
            username = backend.userForEmail(result['email'])
            # print(username)
            # print("It is true")
            resp = make_response(render_template('userProfile.html', username=username))
            resp.set_cookie('loggedIn', 'True')
            resp.set_cookie('username', username)
            # print(request.cookies.get('username'))
            # print(request.cookies.get('loggedIn'))

            return resp
        else:
            return render_template('error.html', name=result['email'])


@app.route('/about/')
def about():
    return render_template('about.html')


@app.route('/test/')
def test():
    if request.cookies.get('loggedIn'):
        return request.cookies.get('username')


@app.route('/login/')
def login():
    return render_template('login.html')


@app.route('/signup/')
def signup():
    return render_template('signup.html')


@app.route('/addNewCompany')
def getCompanyName():
    if request.cookies.get('loggedIn'):
        return render_template('companyInput.html')
    else:
        return render_template('login.html')


@app.route('/result', methods=['POST', 'GET'])
def displayCompany():
    if request.method == 'POST':

        if request.cookies.get('loggedIn'):
            # print("got your shit")
            result = request.form
            # print(result)
            backend.addCompany(result['Name'], result['About'])
            return " ".join(str(x) for x in backend.getCompany())
        else:
            return render_template('login.html')


if __name__ == '__main__':
    app.run()
