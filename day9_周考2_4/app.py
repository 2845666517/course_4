from flask import Flask,request,jsonify,render_template,redirect
from utils.db_client import Mongodb

app = Flask(__name__)
from blueprint.users import users
app.register_blueprint(users)

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/123')
def h123():  # put application's code here
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
