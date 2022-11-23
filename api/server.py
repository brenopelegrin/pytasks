from flask import Flask, request, Response
from sqlalchemy import UniqueConstraint, JSON, func
from flask_restful import reqparse, abort, Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
import json

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL').replace('postgres', 'postgresql', 1)
frontend_url = os.getenv('FRONTEND_URL')

SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_pre_ping': True
}

app.config['SQLALCHEMY_ENGINE_OPTIONS'] = SQLALCHEMY_ENGINE_OPTIONS

api = Api(app)
cors = CORS(app, resources={r"/*": {"origins": frontend_url}})
db = SQLAlchemy(app)
