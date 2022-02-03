from flask import Flask

app = Flask(__name__)

#Decorador que convierte una función Python regular en una función vista de Flask
@app.route('/')
def hello():
    return 'Hello, World!'

# Para correr se deben usar los siguientes comandos:
# export FLASK_APP=hello
# export FLASK_ENV=development
# flask run --host=0.0.0.0