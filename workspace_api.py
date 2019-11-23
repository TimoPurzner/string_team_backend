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

# Workspace spiegelt die Arbeitsplaetze wieder, die man ueber die Platform reservieren kann. 
#	id: 			ist eine eineindeutige ID des Arbeitsplatzes
#	xml_id: 		ist eine eindeutige ID innerhalb eines Bereiches der Arbeitsplaetze enthaelt
#	occupied: 		gibt an ob der Platz gerade besetzt ist
#	occupied_preliminary: 	ist ein voruebergehendes besetzen zur Validierung
#	latitude und longitude: sind GPS Koordinaten
#	level:			Stockwerk auf dem sich der Platz befindet
#	ignored: 		ob dieser Angezeigt werden soll oder nicht
#	last_change: 		wann sich zuletzt jemand auf den Platz registriert hat
#	reserved: 		gibt wieder ob der Platz reserviert ist
#	has_display: 		ob der Platz ueber ein Display verfuegt
#	parking_lot_id: 	ID des Bereichs dem der Arbeitsplatz zugeordnet ist
#	workspace_name:		Name des Arbeitsplatzes
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

# Diese methode aendert den Namen des Arbeitsplatzes. Hierzu wird der neue Name in die
# Datenbank des dazugehoerigen Eintrags eingetragen.
#	return json "success" bei Erfolg
#	return json "failure" wenn kein Arbeitsplatz mit der ID id gefunden wurde
@workspace_api.route('/workspace/<int:id>/name/<string:new_name>', methods=['PUT'])
def change_workspace_name(id, new_name):

    workspace = Workspace.query.filter_by(id=id).first()

    if not workspace:
        return jsonify({'failure':'no user found'})

    workspace.name = new_name
    db.session.flush()
    db.session.commit()

    return jsonify({'success':'workspace name changed'})

# Diese Methode erwartet ein Workspace Dictionary workspace_info. Sie ueberprueft im Kalender
# ob der Arbeitsplatz reserviert ist oder nicht. Weiterhin ueberprueft sie die Gueltigkeit von
# Reservierungen und setzt diesen, wenn der Platz nicht in der vorgegebenen Zeit occupied wurde.
#	return True wenn Arbeitsplatz besetzt
#	return False wenn Arbeitsplatz nicht im Kalender reserviert
def is_workspace_reserved_with_calendar(workspace_info):
    reserved = False
    reservations = json.loads(get_workspace_reservations(workspace_info["id"]).get_data(as_text=True))
    print(reservations)
    current_time = int(time.time())
    reservation_buffer_time = 60*10

    # Reservation validation
    for reservation in reservations:
        reservation_time = workspace_info["last_change"] <= reservation["effective_from"]+ reservation_buffer_time
        reservation_current = reservation["effective_from"] <= current_time and current_time <= reservation["effective_from"]+ reservation_buffer_time
        print("reservation_id:"+str(reservation["reservation_id"])+" last_change:" + str(reservation_time) + " current:" + str(reservation_current))        
        str_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(reservation["effective_from"]+ reservation_buffer_time))
        print("reservation_id:"+str(reservation["reservation_id"])+" buffer till:" +str(str_time))
        if reservation_time and reservation_current:
            reserved = True
        else:
            set_status = json.loads(set_reservation_valid(reservation["reservation_id"], False).get_data(as_text=True))
            print("reservation_id:"+str(reservation["reservation_id"]) + str(set_status))
    return reserved
            
# Speichert ein Workspace Dictionary in der Datenbank ab. Weiterhin aktuallisiert diese Methode den
# Status und Values der Arbeitsplaetze in der Server eigenen Datenbank. Sollte der uebergebene
# Arbeitsplatz noch nicht in der Datenbank existierten, wird dieser erzeugt.
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

# Ruft die aktuellen Daten eines Arbeitsplatzes der Parking-Pilot API ueber einen
# GET-Request ab und speichert/updated die abgerufenden Daten ueber die Methode 
# dict_to_workspace in der Server eingenen Datenbank ab.
def refresh_workspace(id):
    url="https://api.parking-pilot.com/parkingspaces/"+str(id)+"?api_key=HUK_Team4"
    print(url)
    answer=requests.get(url=url).text
    print("############# response #############\n"+answer)
    workspace_info = json.loads(answer)
    dict_to_workspace(workspace_info)

# Wandelt ein Workspace Objekt in ein Workspace Dictionary um
#	return Workspace Dictionary
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


# Liefert die Aktuellen Daten eines Arbeitsplatzes als JSON-String zurueck.
# 	Beispiel URL: http://127.0.0.1:5000/workspace/56308
#	return JSON-String
@workspace_api.route('/workspace/<int:id>', methods=['GET'])
def get_workspace_info(id):
    refresh_workspace(id)
    workspace = Workspace.query.filter_by(id=id).first()
    if not workspace:
        return jsonify({'failure':'no workspace found'})

    workspace_info = workspace_to_dic(workspace)

    return jsonify(workspace_info)

# Updated alle Arbeitsplaetze mit ueber die Parking-Pilot API. und speichert diese
# in die Server eigene Datenbank ab.
def refresh_all_workspaces():
    url="https://api.parking-pilot.com/parkinglots/1778/parkingspaces?api_key=HUK_Team4"
    print(url)
    answer=requests.get(url=url).text
    workspaces_info = json.loads(answer)
    for workspace_info in workspaces_info:
        dict_to_workspace(workspace_info)

# Liefert alle Arbeitsplaetze als JSON-String zurueck.
#	return JSON-String
@workspace_api.route('/workspace/all', methods=['GET'])
def get_all_workspaces():
    refresh_all_workspaces()
    workspaces = Workspace.query.all()
    output = []

    for workspace in workspaces:
        workspace_info = workspace_to_dic(workspace)
        output.append(workspace_info)

    return jsonify({'workspaces':output})
