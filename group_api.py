from flask import Flask
from flask import jsonify
from flask import request
from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy

group_api = Blueprint('group_api', __name__)

from api import db

class Groupname(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(50))
    valid_psid = db.Column(db.String())


@group_api.route('/group', methods=['POST'])
def create_group():

    data = request.get_json()

    new_group = Groupname(id=data['id'], group_name=data['name'], valid_psid=None)
    db.session.add(new_group)
    db.session.commit()

    return jsonify({'status':'new group created'})


@group_api.route('/group/<int:id>', methods=['DELETE'])
def delete_group(id):

    group = Groupname.query.filter_by(id=id).first()

    if not group:

        return jsonify({'failure':'no group found'})

    db.session.delete(group)
    db.session.commit()

    return jsonify({'success':'group deleted'})


@group_api.route('/group/<int:id>/name', methods=['GET'])
def get_group_name(id):

    group = Groupname.query.filter_by(id=id).first()

    if not group:

        return jsonify({'failure':'no group found'})

    return jsonify({'group':group.group_name})


@group_api.route('/group/<int:id>/name/<string:new_name>', methods=['PUT'])
def set_group_name(id, new_name):

    group = Groupname.query.filter_by(id=id).first()

    if not group:

        return jsonify({'failure':'no group found'})

    group.group_name = new_name
    db.session.flush()
    db.session.commit()

    return jsonify({'success':f'group name changed to {group.group_name}'})


@group_api.route('/group/<int:id>/valid_psid', methods=['GET'])
def get_group_valid_psid(id):

    group = Groupname.query.filter_by(id=id).first()

    if not group:

        return jsonify({'failure':'no group found'})

    return jsonify({'group':group.valid_psid})


@group_api.route('/group/<int:id>/valid_psid/<string:new_psid>', methods=['PUT'])
def set_group_valid_psid(id, new_psid):

    group = Groupname.query.filter_by(id=id).first()

    if not group:

        return jsonify({'failure':'no group found'})

    group.valid_psid = new_psid
    db.session.flush()
    db.session.commit()

    return jsonify({'success':f'group valid_psid changed to {group.valid_psid}'})


@group_api.route('/group/<int:id>', methods=['GET'])
def get_group_info(id):

    group = Groupname.query.filter_by(id=id).first()

    if not group:

        return jsonify({'failure':'no group found'})

    group_info = {}
    group_info['id']=group.id
    group_info['group_name']=group.group_name
    group_info['valid_psid']=group.valid_psid


    return jsonify(group_info)


@group_api.route('/group/all', methods=['GET'])
def get_all_groups():

    groups = Groupname.query.all()

    output = []

    for group in groups:
        group_info = {}
        group_info['id']=group.id
        group_info['group_name']=group.group_name
        group_info['valid_psid']=group.valid_psid
        output.append(group_info)

    return jsonify({'groups':output})