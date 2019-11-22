from flask import Flask
from flask import jsonify
from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy
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

def refresh_workspace(id):

    url="https://api.parking-pilot.com/parkingspaces/"+str(id)+"?api_key=HUK_Team4"
    print(url)
    answer=requests.get(url=url).text
    print("############# respnse #############\n"+answer)
    workspace_info = json.loads(answer)
    workspace = Workspace.query.filter_by(id=id).first()
    if not workspace:
        print("create new workspace")
        workspace = Workspace(
            id=workspace_info["id"],
            xml_id = workspace_info["xml_id"],
            occupied = workspace_info["occupied"],
            occupied_preliminary = workspace_info["occupied_preliminary"],
            latitude = workspace_info["latitude"],
            longitude = workspace_info["longitude"],
            level = workspace_info["level"],
            ignored = workspace_info["ignored"],
            last_change = workspace_info["last_change"],
            last_contact = workspace_info["last_contact"],
            reserved = workspace_info["reserved"],
            has_display = workspace_info["has_display"],
            parking_lot_id = workspace_info["parking_lot_id"],
            workspace_name = "not defined"
        )
        db.session.add(workspace)
        db.session.commit()
    else:
        print("update old workspace")
        workspace.xml_id = workspace_info["xml_id"]
        reserved_buffer_time_seconds = 15
        workspace.occupied = workspace_info["occupied"]
        workspace.occupied_preliminary = workspace_info["occupied_preliminary"]
        workspace.latitude = workspace_info["latitude"]
        workspace.longitude = workspace_info["longitude"]
        workspace.level = workspace_info["level"]
        #additional_info
        workspace.ignored = workspace_info["ignored"]
        workspace.last_change = workspace_info["last_change"]
        workspace.last_contact = workspace_info["last_contact"]
        if workspace_info["occupied"]  == False and int(time.time())-int(workspace_info["last_change"]) < reserved_buffer_time_seconds:
            workspace.reserved = True
        else:
            workspace.reserved = workspace_info["reserved"]
        workspace.has_display = workspace_info["has_display"]
        workspace.parking_lot_id = workspace_info["parking_lot_id"]
    db.session.flush()
    db.session.commit()

@workspace_api.route('/workspace/<int:id>', methods=['GET'])
def get_workspace_info(id):
    refresh_workspace(id)
    workspace = Workspace.query.filter_by(id=id).first()
    if not workspace:
        return jsonify({'failure':'no workspace found'})

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

    return jsonify(workspace_info)
