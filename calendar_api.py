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
    #reservations = Calendar.query.all()

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