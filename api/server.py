from flask import Flask, request, Response
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS
import os
import json

app = Flask(__name__)
frontend_url = os.getenv('FRONTEND_URL')

api = Api(app)
cors = CORS(app, resources={r"/*": {"origins": frontend_url}})