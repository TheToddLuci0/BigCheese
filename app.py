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

@app.route('/result',methods = ['POST', 'GET'])
def displayCompany():
    if request.method == 'POST':
        result = request.form

        return " ".join(str(x) for x in backend.getCompany())

if __name__ == '__main__':
    app.run()
