import sys
from server import app, api
from resources.web import NewTask, ViewTask, Ping, ProtectedByJwt, GenerateTokenForUser, ViewTaskList

#   Unprotected routes (except protected tasks)
api.add_resource(NewTask, '/task/new')
api.add_resource(ViewTask, '/task/<string:task_id>/view')
api.add_resource(ViewTaskList, '/tasks')
api.add_resource(Ping, '/ping')

#   Protected routes
api.add_resource(ProtectedByJwt, '/protected')

#   Generate token route
api.add_resource(GenerateTokenForUser, '/token')

@app.route('/')
def documentation():
    return "You can view the server-end documentation on <a href='https://github.com/brenopelegrin/flask-tasks-docker/'>GitHub.</a>"

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port='5000')
    
