from flask import Flask
from flask import jsonify
from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy
import user_api
from calendar_api import get_workspace_reservations
from calendar_api import set_reservation_valid
import requests
import json
import time

workspace_api = Blueprint('workspace_api', __name__)

from api import db

class Workspace(db.Model):
    # Attributes from extern api
    id = db.Column(db.Integer, primary_key=True)
    xml_id = db.Column(db.Integer)
    occupied = db.Column(db.Boolean)
    occupied_preliminary = db.Column(db.Boolean)
    latitude = db.Column(db.Integer)
    longitude = db.Column(db.Integer)
    level = db.Column(db.Integer)
    #additional_info
    ignored = db.Column(db.Boolean)
    last_change = db.Column(db.Integer)
    last_contact = db.Column(db.Integer)
    reserved = db.Column(db.Boolean)
    has_display = db.Column(db.Boolean)
    parking_lot_id = db.Column(db.Integer)
    # our own Attributes
    workspace_name = db.Column(db.String(50))

@workspace_api.route('/workspace/<int:id>/name/<string:new_name>', methods=['PUT'])
def change_workspace_name(id, new_name):

    workspace = Workspace.query.filter_by(id=id).first()

    if not workspace:
        return jsonify({'failure':'no user found'})

    workspace.name = new_name
    db.session.flush()
    db.session.commit()

    return jsonify({'success':'workspace name changed'})

def is_workspace_reserved_with_calendar(workspace_info):
    reserved = False
    reservations = json.loads(get_workspace_reservations(workspace_info["id"]).get_data(as_text=True))
    print(reservations)
    current_time = int(time.time())
    reservation_buffer_time = 60*10

    # Reservation validation
    for reservation in reservations:
        reservation_time = reservation["effective_from"] <= workspace_info["last_change"] and workspace_info["last_change"] <= reservation["effective_to"]+ reservation_buffer_time
        reservation_current = reservation["effective_from"] <= current_time and current_time <= reservation["effective_to"]+ reservation_buffer_time
        if reservation_time or reservation_current:
            reserved = True
    return reserved
            

def dict_to_workspace(workspace_info):
    id = workspace_info["id"]
    workspace = Workspace.query.filter_by(id=id).first()
    last_contact = 0
    if "last_contact" in workspace_info:
        last_contact = workspace_info["last_contact"]

    
    reserved_buffer_time_seconds = 15
    reserved = False
    # Checke Parkuhr System
    if workspace_info["occupied"]  == False and int(time.time())-int(workspace_info["last_change"]) < reserved_buffer_time_seconds:
        reserved = True
    # Checke ob Arbeitsplatz vom Kalender aus reserviert ist
    elif is_workspace_reserved_with_calendar(workspace_info):
        reserved = True
    else:
        reserved = workspace_info["reserved"]

    occupied = workspace_info["occupied"]
    # http://127.0.0.1:5000/workspace/61671
    hard_coded_occupied_workspace_ids = [61671, 61720, 61718, 61719]
    for hard_code_id in hard_coded_occupied_workspace_ids:
        if hard_code_id == id:
            occupied = True

    if not workspace:
        print("create new workspace[id='"+str(id)+"']")
        workspace = Workspace(
            id=workspace_info["id"],
            xml_id = workspace_info["xml_id"],
            occupied = occupied,
            occupied_preliminary = workspace_info["occupied_preliminary"],
            latitude = workspace_info["latitude"],
            longitude = workspace_info["longitude"],
            level = workspace_info["level"],
            ignored = workspace_info["ignored"],
            last_change = workspace_info["last_change"],
            last_contact = last_contact,
            reserved = reserved,
            has_display = workspace_info["has_display"],
            parking_lot_id = workspace_info["parking_lot_id"],
            workspace_name = "not defined"
        )
        db.session.add(workspace)
        db.session.commit()
    else:
        print("update old workspace[id='"+str(id)+"']")
        workspace.xml_id = workspace_info["xml_id"]
        workspace.occupied = occupied
        workspace.occupied_preliminary = workspace_info["occupied_preliminary"]
        workspace.latitude = workspace_info["latitude"]
        workspace.longitude = workspace_info["longitude"]
        workspace.level = workspace_info["level"]
        #additional_info
        workspace.ignored = workspace_info["ignored"]
        workspace.last_change = workspace_info["last_change"]
        workspace.last_contact = last_contact
        workspace.reserved = reserved
        workspace.has_display = workspace_info["has_display"]
        workspace.parking_lot_id = workspace_info["parking_lot_id"]
    db.session.flush()
    db.session.commit()

def refresh_workspace(id):
    url="https://api.parking-pilot.com/parkingspaces/"+str(id)+"?api_key=HUK_Team4"
    print(url)
    answer=requests.get(url=url).text
    print("############# response #############\n"+answer)
    workspace_info = json.loads(answer)
    dict_to_workspace(workspace_info)

def workspace_to_dic(workspace):
    workspace_info = {}
    workspace_info["id"] = workspace.id
    workspace_info["xml_id"] = workspace.xml_id
    workspace_info["occupied"] = workspace.occupied
    workspace_info["occupied_preliminary"] = workspace.occupied_preliminary
    workspace_info["latitude"] = workspace.latitude
    workspace_info["longitude"] = workspace.longitude
    workspace_info["level"] = workspace.level
    #additional_info
    workspace_info["ignored"] = workspace.ignored
    workspace_info["last_change"] = workspace.last_change
    workspace_info["last_contact"] = workspace.last_contact
    workspace_info["reserved"] = workspace.reserved
    workspace_info["has_display"] = workspace.has_display
    workspace_info["parking_lot_id"] = workspace.parking_lot_id
    workspace_info["workspace_name"] = workspace.workspace_name

    return workspace_info

# http://127.0.0.1:5000/workspace/56308
@workspace_api.route('/workspace/<int:id>', methods=['GET'])
def get_workspace_info(id):
    refresh_workspace(id)
    workspace = Workspace.query.filter_by(id=id).first()
    if not workspace:
        return jsonify({'failure':'no workspace found'})

    workspace_info = workspace_to_dic(workspace)

    return jsonify(workspace_info)

def refresh_all_workspaces():
    url="https://api.parking-pilot.com/parkinglots/1778/parkingspaces?api_key=HUK_Team4"
    print(url)
    answer=requests.get(url=url).text
    workspaces_info = json.loads(answer)
    for workspace_info in workspaces_info:
        dict_to_workspace(workspace_info)

@workspace_api.route('/workspace/all', methods=['GET'])
def get_all_workspaces():
    refresh_all_workspaces()
    workspaces = Workspace.query.all()
    output = []

    for workspace in workspaces:
        workspace_info = workspace_to_dic(workspace)
        output.append(workspace_info)

    return jsonify({'workspaces':output})
