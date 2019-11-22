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

    print(data)

    new_reservation = Calendar(reservation_id=data['reservation_id'],
                                workspace_id=data['workspace_id'],
                                user_id=data['user_id'],
                                effective_from=data['effective_from'],
                                effective_to=data['effective_to']
                                )

    print('workspace_id: ',new_reservation.workspace_id)

    reservations = Calendar.query.filter_by(workspace_id=new_reservation.workspace_id)
    #reservations = Calendar.query.all()

    return jsonify({'success':'yeah'})

    #print(reservations.workspace_id)