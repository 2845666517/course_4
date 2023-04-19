from flask import Flask

app = Flask(__name__)
from blueprint.home.homes import homes
app.register_blueprint(homes)

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
