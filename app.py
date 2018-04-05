from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import backend
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:steve@localhost/theCellar'
db = SQLAlchemy(app)
db.init_app(app)
Bootstrap(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/employer/<name>')
def employer(name):
    return render_template('employer.html', name=name)


@app.route('/employers/', methods=['POST', 'GET'])
def employers():
    if request.method == 'POST':
    print("got your shit")
    result = request.form
    print(result)
    backend.addCompany(result['Name'], result['About'])
    return render_template('employers.html', result=backend.getCompany())


@app.route('/user/')
def user():
    return render_template('userProfile.html')


@app.route('/user/<username>')
def profile(username):
    return render_template('userProfile.html', username=username)


@app.route('/about/')
def about():
    return render_template('about.html')


@app.route('/test/')
def test():
    return render_template('test.html')


@app.route('/login/')
def login():
    return render_template('login.html')


@app.route('/addNewCompany')
def getCompanyName():
    return render_template('companyInput.html')


@app.route('/result', methods=['POST', 'GET'])
def displayCompany():
d


if __name__ == '__main__':
    app.run()
