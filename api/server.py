from flask import Flask, request, Response
from flask_restx import reqparse, abort, Api, Resource
from flask_cors import CORS
import os
import json

app = Flask(__name__)
frontend_url = os.getenv('FRONTEND_URL')

api = Api(app, title='pytasks API', description='pytasks API',  version='1.0')
cors = CORS(app, resources={r"/*": {"origins": frontend_url}})