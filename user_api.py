from flask import Flask
from flask import jsonify
from flask import request
from flask import Blueprint
#from api import db
from flask_sqlalchemy import SQLAlchemy

#app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

#db = SQLAlchemy(app)

user_api = Blueprint('user_api', __name__)

from api import db

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    psid = db.Column(db.Integer)
    group = db.Column(db.String(50))


@user_api.route('/user', methods=['POST'])
def create_user():

    data = request.get_json()

    new_user = User(id=data['id'], name=data['name'], psid=None, group='default')
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'status':'new user created'})


@user_api.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):

    user = User.query.filter_by(id=id).first()

    if not user:

        return jsonify({'failure':'no user found'})

    db.session.delete(user)
    db.session.commit()

    return jsonify({'success':'user deleted'})


@user_api.route('/user/<int:id>/name/<string:new_name>', methods=['PUT'])
def change_user_name(id, new_name):

    user = User.query.filter_by(id=id).first()

    if not user:

        return jsonify({'failure':'no user found'})

    user.name = new_name
    db.session.flush()
    db.session.commit()

    return jsonify({'success':'user name changed'})


@user_api.route('/user/<int:id>', methods=['GET'])
def get_user_info(id):

    user = User.query.filter_by(id=id).first()

    if not user:

        return jsonify({'failure':'no user found'})

    return '1'

@user_api.route('/user/<int:id>/name', methods=['GET'])
def get_user_name(id):

    user = User.query.filter_by(id=id).first()

    if not user:

        return jsonify({'failure':'no user found'})

    return jsonify({'name':user.name})

    


#if __name__ == '__main__':

#    app.run(debug=True)
