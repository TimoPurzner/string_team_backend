from flask import Flask
from flask import jsonify
from flask import request
from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy

group_api = Blueprint('group_api', __name__)

from api import db

class Group(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(50))
    valid_psid = db.Column(db.String())

