import sys
from server import app, api
from resources.web import *

api.add_resource(NewTask, '/task/new')
api.add_resource(ViewTask, '/task/<int:task_id>/view')
api.add_resource(Ping, '/ping')

@app.route('/')
def documentation():
    return "You can view the server-end documentation on <a href='https://github.com/brenopelegrin/flask-tasks/'>GitHub.</a>"

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port='5000')
    
