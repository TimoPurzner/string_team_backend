from flask import Flask
from flask import jsonify
from flask import request
from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy

calendar_api = Blueprint('calendar_api', __name__)

from api import db

# In diesem Objekt werden alle Reservierung eines Arbeitsplates abgespeicher und verwaltet.
#	reservation_id:		eineindeutige ID der Reservierung
#	workspace_id:		ID des Arbeitsplatzes der reserviert werden soll
#	user_id:		ID des Users der die Reservierung getaetigt hat
#	effective_from:		Startzeit der Reservierung als Epoch Time (Time since 1970 in seconds)
#	effective_to:		Endzeit der Reservierung als Epoch Time (Time since 1970 in seconds)
#	valid:			Flag ob die Reservierung gueltig ist oder nicht
class Calendar(db.Model):

    reservation_id = db.Column(db.Integer, primary_key=True)
    workspace_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    effective_from = db.Column(db.Integer)
    effective_to = db.Column(db.Integer)
    valid = db.Column(db.Integer)

# Erstellt eine Reservierung und speichert diesen in der Server eigenen Datenbank ab
#	return JSON-String mit reservation_id bei Erfolg
#	return Conflict String message bei Ueberschneidungen mit anderen Resrevierungen
@calendar_api.route('/calendar', methods=['POST'])
def create_reservation():

    data = request.get_json()
    print(data)

    # generate reservation_id
    max_reservtion_id = db.session.query(Calendar.reservation_id).order_by(Calendar.reservation_id.desc()).first()[0]

    new_reservation = Calendar(reservation_id=max_reservtion_id+1,
                                workspace_id=data['workspace_id'],
                                user_id=data['user_id'],
                                effective_from=data['effective_from'],
                                effective_to=data['effective_to'],
                                valid=1
                                )

    # all reservations for this workspace
    reservations = Calendar.query.filter(Calendar.workspace_id==new_reservation.workspace_id,
    Calendar.effective_from<new_reservation.effective_to,
    Calendar.effective_to>new_reservation.effective_from,
    Calendar.valid==1)

    conflict_output = {}

    for reservation in reservations:

        conflict_output[reservation.reservation_id] = 'conflict with this reservation_id'

    if len(conflict_output):

        return jsonify(conflict_output)

    # add new reservation
    db.session.add(new_reservation)
    db.session.commit()

    return jsonify({'reservation_id':new_reservation.reservation_id})

    #print(reservations.workspace_id)


# Gibt alle Reservierungen eines Users mit der ID user_id als JSON-String zurueck.
#	return JSON-String List reservations
@calendar_api.route('/calendar/user/<int:user_id>', methods=['GET'])
def get_user_reservations(user_id):

    reservations = db.session.query(Calendar).filter(Calendar.user_id==user_id)

    output = []

    for reservation in reservations:

        output_file = {}
        output_file['reservation_id'] = reservation.reservation_id
        output_file['workspace_id'] = reservation.workspace_id
        output_file['user_id'] = reservation.user_id
        output_file['effective_from'] = reservation.effective_from
        output_file['effective_to'] = reservation.effective_to
        output_file['valid'] = reservation.valid
        output.append(output_file)

    return jsonify(output)

# Gibt alle Reservierungen eines Platzes mit der ID workspace_id als JSON-String zurueck.
#	return JSON-String List reservations
@calendar_api.route('/calendar/workspace/<int:workspace_id>', methods=['GET'])
def get_workspace_reservations(workspace_id):

    reservations = db.session.query(Calendar).filter(Calendar.workspace_id==workspace_id)

    output = []

    for reservation in reservations:

        output_file = {}
        output_file['reservation_id'] = reservation.reservation_id
        output_file['workspace_id'] = reservation.workspace_id
        output_file['user_id'] = reservation.user_id
        output_file['effective_from'] = reservation.effective_from
        output_file['effective_to'] = reservation.effective_to
        output_file['valid'] = reservation.valid
        output.append(output_file)

    return jsonify(output)


# Gibt eine Reservierung mit der ID reservation_id als JSON-String zurueck
#	return JSON-String reservation
@calendar_api.route('/calendar/reservation/<int:reservation_id>', methods=['GET'])
def get_reservations(reservation_id):

    reservations = db.session.query(Calendar).filter(Calendar.reservation_id==reservation_id)

    output = []

    for reservation in reservations:

        output_file = {}
        output_file['reservation_id'] = reservation.reservation_id
        output_file['workspace_id'] = reservation.workspace_id
        output_file['user_id'] = reservation.user_id
        output_file['effective_from'] = reservation.effective_from
        output_file['effective_to'] = reservation.effective_to
        output_file['valid'] = reservation.valid
        output.append(output_file)

    return jsonify(output)

# Gibt alle Reservierungen als JSON-String-List zurueck.
#	return JSON-String-List reservation
@calendar_api.route('/calendar/reservation/all', methods=['GET'])
def get_all_reservations():

    reservations = db.session.query(Calendar).all()

    output = []

    for reservation in reservations:

        output_file = {}
        output_file['reservation_id'] = reservation.reservation_id
        output_file['workspace_id'] = reservation.workspace_id
        output_file['user_id'] = reservation.user_id
        output_file['effective_from'] = reservation.effective_from
        output_file['effective_to'] = reservation.effective_to
        output_file['valid'] = reservation.valid
        output.append(output_file)

    return jsonify(output)

# Mit dieser Methode kann man das Flag fuer die valid einer Reservierung setzen.
#	return boolean of valid Flag as JSON-String
#	return json "failure" wenn keine zugehoerige Reservierung gefunden wurde
@calendar_api.route('/calendar/valid/<int:reservation_id>/<int:valid>', methods=['PUT'])
def set_reservation_valid(reservation_id, valid):

    reservation = db.session.query(Calendar).filter(Calendar.reservation_id==reservation_id).first()

    if not reservation:

        return jsonify({'failure':'no reservation found'})

    reservation.valid = valid
    db.session.flush()
    db.session.commit()

    return jsonify({'valid':reservation.valid})
