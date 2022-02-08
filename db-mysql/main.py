from flask import Flask,render_template, request
from flask_mysqldb import MySQL
 
app = Flask(__name__)
 
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask'
 
mysql = MySQL(app)
 
@app.route('/form')
def form():
    return render_template('form.html')
 
@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'GET':
        return "Login via the login Form"
     
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        print("{}{}".format(name,age))
        cursor = mysql.connection.cursor()
        #Nombre de tabla:testing
        cursor.execute(''' INSERT INTO testing VALUES(%s,%s)''',(name,age))
        mysql.connection.commit()
        cursor.close()
        return f"Done!!"
 
app.run(host='localhost', port=5000)