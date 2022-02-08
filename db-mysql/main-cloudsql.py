# imports
from flask import Flask, request, make_response
from flask_sqlalchemy import SQLAlchemy
from os import environ

# initializing Flask app
app = Flask(__name__)

#Este codigo usa CloudSQL con una base de datos MySQL

# Google Cloud SQL (change this accordingly)
PASSWORD = environ.get('PASSWORD')
PUBLIC_IP_ADDRESS = environ.get('PUBLIC_IP_ADDRESS')
DBNAME = environ.get('DBNAME')
PROJECT_ID = environ.get('PROJECT_ID')
INSTANCE_NAME = environ.get('INSTANCE_NAME')
CLOUD_SQL_PORT = environ.get('CLOUD_SQL_PORT')


# configuration
app.config["SECRET_KEY"] = "yoursecretkey"
app.config["SQLALCHEMY_DATABASE_URI"]=f"mysql+mysqldb://root:{PASSWORD}@{PUBLIC_IP_ADDRESS}:{CLOUD_SQL_PORT}/{DBNAME}?unix_socket=/cloudsql/{PROJECT_ID}:{INSTANCE_NAME}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= True

db = SQLAlchemy(app)

# User ORM for SQLAlchemy
class Users(db.Model):
	id = db.Column(db.Integer, primary_key = True, nullable = False)
	name = db.Column(db.String(50), nullable = False)
	email = db.Column(db.String(50), nullable = False, unique = True)

@app.route('/add', methods =['POST'])
def add():
	# getting name and email
	name = request.values.get('name')
	email = request.values.get('email')
	# checking if user already exists
	user = Users.query.filter_by(email = email).first()
	print("{}{}".format(name,email))

	if not user:
		try:
			# creating Users object
			user = Users(
				name = name,
				email = email
			)
			# adding the fields to users table
			db.session.add(user)
			db.session.commit()
			# response
			responseObject = {
				'status' : 'success',
				'message': 'Successfully registered.'
			}

			return make_response(responseObject, 200)
		except:
			responseObject = {
				'status' : 'fail',
				'message': 'Some error occured !!'
			}

			return make_response(responseObject, 400)
		
	else:
		# if user already exists then send status as fail
		responseObject = {
			'status' : 'fail',
			'message': 'User already exists !!'
		}

		return make_response(responseObject, 403)

@app.route('/view')
def view():
	# fetches all the users
	users = Users.query.all()
	# response list consisting user details
	response = list()

	for user in users:
		response.append({
			"name" : user.name,
			"email": user.email
		})

	return make_response({
		'status' : 'success',
		'message': response
	}, 200)


if __name__ == "__main__":
	# serving the app directly
	app.run()
