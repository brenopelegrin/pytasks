from flask import Flask
from sqlalchemy import UniqueConstraint, JSON, func
from flask_sqlalchemy import SQLAlchemy
import os
import json

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL').replace('postgres', 'postgresql', 1)

SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_pre_ping': True
}

app.config['SQLALCHEMY_ENGINE_OPTIONS'] = SQLALCHEMY_ENGINE_OPTIONS

db = SQLAlchemy(app)
