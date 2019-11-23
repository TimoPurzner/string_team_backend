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

# Die Klasse User beinhaltet die Daten eines User der einen Arbeitsplatz reservieren kann.
#	id:		eineindeutige ID des Users
#	name:		Name des Users
#	psid:		ID des aktuellen Arbeitsplatzes den er besetzt
#	group_name:	JSON-String-List an Gruppennamen denen der User zugeordnet ist
class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    psid = db.Column(db.Integer)
    group_name = db.Column(db.String(50))


# Speicher einen neues User in der lokalen Datenbank des Servers ab.
#	return JSON-String message bei Erfolg
@user_api.route('/user', methods=['POST'])
def create_user():

    data = request.get_json()

    new_user = User(id=data['id'], name=data['name'], psid=None, group='default')
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'status':'new user created'})

# Entfernt einen User aus der lokalen Datenbank des Servers.
#	return JSON-String failure wenn User mit id nicht gefunden
#	return JSON-Strinf success wenn User erflogreich aus der Datenbank geloescht
@user_api.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):

    user = User.query.filter_by(id=id).first()

    if not user:

        return jsonify({'failure':'no user found'})

    db.session.delete(user)
    db.session.commit()

    return jsonify({'success':'user deleted'})

# Setzt den Namen new_name des Users mit der ID id in der Datenbank.
#	return JSON-String failure wenn User mit id nicht gefunden
#	return JSON-Strinf success wenn der Name geaendert wurde
@user_api.route('/user/<int:id>/name/<string:new_name>', methods=['PUT'])
def set_user_name(id, new_name):

    user = User.query.filter_by(id=id).first()

    if not user:

        return jsonify({'failure':'no user found'})

    user.name = new_name
    db.session.flush()
    db.session.commit()

    return jsonify({'success':'user name changed'})


# Liefert die Informationen eines Users mit der ID id als JSON-String zurueck.
#	return JSON-String failure wenn User nicht gefunden
#	return JSON-String User wenn erfolgreich
@user_api.route('/user/<int:id>', methods=['GET'])
def get_user_info(id):

    user = User.query.filter_by(id=id).first()
    
    if not user:

        return jsonify({'failure':'no user found'})

    user_info = {}
    user_info['id']=user.id
    user_info['name']=user.name
    user_info['psid']=user.psid
    user_info['group']=user.group_name

    return jsonify(user_info)

# Liefert alle User als JSON-String-List zurueck.
#	return JSON-String-List
@user_api.route('/user/all', methods=['GET'])
def get_all_users():

    users = User.query.all()

    output = []

    for user in users:
        user_info = {}
        user_info['id']=user.id
        user_info['name']=user.name
        user_info['psid']=user.psid
        user_info['group']=user.group_name
        output.append(user_info)

    return jsonify({'users':output})

# Liefert den Namen des Users mit der ID id als JSON-String zurueck.
#	return JSON-String failure wenn User nicht gefunden wurde
#	return JSON-String name bei Erfolg
@user_api.route('/user/<int:id>/name', methods=['GET'])
def get_user_name(id):

    user = User.query.filter_by(id=id).first()

    if not user:

        return jsonify({'failure':'no user found'})

    return jsonify({'name':user.name})

# Liefert die ID des aktuellen Arbeitsplatzes der dem User zugeordnet 
# ist als JSON-String zureck.
#	return JSON-String failure wenn User nicht gefunden
#	return JSON-String psid bei Erfolg
@user_api.route('/user/<int:id>/psid', methods=['GET'])
def get_user_psid(id):

    user = User.query.filter_by(id=id).first()

    if not user:

        return jsonify({'failure':'no user found'})

    return jsonify({'psid':user.psid})

# Sets die ID psid des aktuellen Arbeitsplatzes des Users mit der ID id.
#	return JSON-String failure wenn User nicht gefunden
#	return JSON-String success wenn psid gesetzt wurde
@user_api.route('/user/<int:id>/psid/<string:new_psid>', methods=['PUT'])
def set_user_psid(id, new_psid):

    user = User.query.filter_by(id=id).first()

    if not user:

        return jsonify({'failure':'no user found'})

    user.psid = new_psid
    db.session.flush()
    db.session.commit()

    return jsonify({'success':f'user psid changed to {user.psid}'})


# Gibt die Gruppen eines Users mit der ID id als String-String-List zurueck.
#	return JSON-String-List wenn erfolgreich
#	return JSON-String failure wenn User nicht gefunden wurde
@user_api.route('/user/<int:id>/group', methods=['GET'])
def get_user_group(id):

    user = User.query.filter_by(id=id).first()

    if not user:

        return jsonify({'failure':'no user found'})

    return jsonify({'group':user.group_name})


# Setzt die Gruppen new_group des Users mit der ID id.
#	return JSON-String failure wenn User nicht gefunden
#	return JSON-String success bei Erfolg
@user_api.route('/user/<int:id>/group/<string:new_group>', methods=['PUT'])
def set_user_group(id, new_group):

    user = User.query.filter_by(id=id).first()

    if not user:

        return jsonify({'failure':'no user found'})

    user.group_name = new_group
    db.session.flush()
    db.session.commit()

    return jsonify({'success':f'user group_name changed to {user.group_name}'})


    


#if __name__ == '__main__':

#    app.run(debug=True)

