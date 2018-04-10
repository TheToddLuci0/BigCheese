from flask import Flask, render_template, request, redirect, url_for, flash, make_response
from flask_login import (LoginManager, current_user, login_required,
                            login_user, logout_user, UserMixin,
                            confirm_login, fresh_login_required)
from flask_sqlalchemy import SQLAlchemy
import backend
from flask_bootstrap import Bootstrap
import logging



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
    if request.cookies.get('loggedIn'):
        if request.method == 'POST':
            if request.cookies.get('loggedIn'):
                result = request.form
                #logging.info(result)
                backend.addReview(result['Name'], result['Review'], int(result['Score']), request.cookies.get('username'))
                #return render_template('employer.html', result=backend.getCompany())
                return redirect("http://www.bigcheese.review/employers")#.format(result['Name']))
            else:
              return render_template('login.html')
        #return redirect("http://www.bigcheese.review/employers")
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
            logging.info("got your shit")
            result = request.form
            logging.info(result)
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
        logging.info(result)
        success = backend.addUser(result['display_name'], result['password'], result['email'], result['first_name'], result['last_name'])
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
        logging.info(result)
        success = backend.addUser(result['display_name'], result['password'], result['email'], result['first_name'], result['last_name'])
        if success:
            return render_template('userProfile.html', username=username)
        else:
            return render_template('error.html', name=result['display_name'])


@app.route('/check/', methods=['POST', 'GET'])
def checkPassword():
    logging.info("Are you here?")
    if request.method == 'POST':
        result = request.form
        logging.info(result)
        success = backend.checkPassword(result['email'], result['password'])
        if success:
            logging.info(result['email'])
            username = backend.userForEmail(result['email'])
            logging.info(username)
            logging.info("It is true")
            resp = make_response(render_template('userProfile.html', username=username))
            resp.set_cookie('loggedIn', 'True')
            resp.set_cookie('username', username)
            logging.info(request.cookies.get('username'))
            logging.info(request.cookies.get('loggedIn'))

            return resp
        else:
            return render_template('error.html', name=result['email'])
    else:
        logging.info("Not a post?")


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
            logging.info("got your shit")
            result = request.form
            logging.info(result)
            backend.addCompany(result['Name'], result['About'])
            return " ".join(str(x) for x in backend.getCompany())
        else:
            return render_template('login.html')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, filename="logfile", filemode="a+",
                        format="%(asctime)-15s %(levelname)-8s %(message)s")
    app.run()
