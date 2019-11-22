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
def set_user_name(id, new_name):

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

    user_info = {}
    user_info['id']=user.id
    user_info['name']=user.name
    user_info['psid']=user.psid
    user_info['group']=user.group

    return jsonify(user_info)


@user_api.route('/user/all', methods=['GET'])
def get_all_users():

    users = User.query.all()

    output = []

    for user in users:
        user_info = {}
        user_info['id']=user.id
        user_info['name']=user.name
        user_info['psid']=user.psid
        user_info['group']=user.group
        output.append(user_info)

    return jsonify({'users':output})


@user_api.route('/user/<int:id>/name', methods=['GET'])
def get_user_name(id):

    user = User.query.filter_by(id=id).first()

    if not user:

        return jsonify({'failure':'no user found'})

    return jsonify({'name':user.name})


@user_api.route('/user/<int:id>/psid', methods=['GET'])
def get_user_psid(id):

    user = User.query.filter_by(id=id).first()

    if not user:

        return jsonify({'failure':'no user found'})

    return jsonify({'psid':user.psid})


@user_api.route('/user/<int:id>/psid/<string:new_psid>', methods=['PUT'])
def set_user_psid(id, new_psid):

    user = User.query.filter_by(id=id).first()

    if not user:

        return jsonify({'failure':'no user found'})

    user.psid = new_psid
    db.session.flush()
    db.session.commit()

    return jsonify({'success':f'user psid changed to {user.psid}'})


@user_api.route('/user/<int:id>/group', methods=['GET'])
def get_user_group(id):

    user = User.query.filter_by(id=id).first()

    if not user:

        return jsonify({'failure':'no user found'})

    return jsonify({'group':user.group})


@user_api.route('/user/<int:id>/group/<string:new_group>', methods=['PUT'])
def set_user_group(id, new_group):

    user = User.query.filter_by(id=id).first()

    if not user:

        return jsonify({'failure':'no user found'})

    user.group = new_group
    db.session.flush()
    db.session.commit()

    return jsonify({'success':f'user group changed to {user.group}'})


    


#if __name__ == '__main__':

#    app.run(debug=True)

