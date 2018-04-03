from flask import Flask,  render_template, request
from flask_sqlalchemy import SQLAlchemy
import backend



app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:steve@localhost/theCellar'
db = SQLAlchemy(app)
db.init_app(app)


@app.route('/')
def getCompanyName():
    return render_template('companyInput.html')
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

@app.route('/result',methods = ['POST', 'GET'])
def displayCompany():
    if request.method == 'POST':
        result = request.form

        return " ".join(str(x) for x in backend.getCompany())

if __name__ == '__main__':
    app.run()
