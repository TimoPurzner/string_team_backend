from flask import Flask
from flask import jsonify
from flask import request
from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy

calendar_api = Blueprint('calendar_api', __name__)

from api import db

class Calendar(db.Model):

    reservation_id = db.Column(db.Integer, primary_key=True)
    workspace_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    effective_from = db.Column(db.Integer)
    effective_to = db.Column(db.Integer)


@calendar_api.route('/calendar', methods=['POST'])
def create_reservation():

    data = request.get_json()

    # generate reservation_id
    max_reservtion_id = db.session.query(Calendar.reservation_id).order_by(Calendar.reservation_id.desc()).first()[0]

    new_reservation = Calendar(reservation_id=max_reservtion_id+1,
                                workspace_id=data['workspace_id'],
                                user_id=data['user_id'],
                                effective_from=data['effective_from'],
                                effective_to=data['effective_to']
                                )

    # all reservations for this workspace
    reservations = Calendar.query.filter(Calendar.workspace_id==new_reservation.workspace_id,
    Calendar.effective_from<new_reservation.effective_to,
    Calendar.effective_to>new_reservation.effective_from)

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
        output.append(output_file)

    return jsonify(output)


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
        output.append(output_file)

    return jsonify(output)


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
        output.append(output_file)

    return jsonify(output)


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
        output.append(output_file)

    return jsonify(output)
