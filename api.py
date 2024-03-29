from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
CORS(app)


db = SQLAlchemy(app)

from user_api import user_api
from group_api import group_api
from calendar_api import calendar_api
from workspace_api import workspace_api

app.register_blueprint(user_api)
app.register_blueprint(group_api)
app.register_blueprint(calendar_api)
app.register_blueprint(workspace_api)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run(debug=True)
