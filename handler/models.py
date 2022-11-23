from server import db
import marshmallow as ma
from flask_marshmallow import Marshmallow
    
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    required_arg = db.Column(db.String(16), nullable=False)
    args = db.Column(db.JSON, nullable=False)
    result = db.Column(db.JSON, nullable=True)
    status = db.Column(db.String(16), nullable=True)
    created = db.Column(db.Integer, nullable=False)
    expire = db.Column(db.Integer, nullable=False)

    def to_json(self):
        return {"id": self.id, "required_arg": self.required_arg, "created": self.created, "expire": self.expire, "args": self.args, "status": self.status, "result": self.result}
    
    def __repr__(self):
        return f'<Task {self.id}>'

class TaskSchema(ma.Schema):
    class Meta:
        fields = ("id", "required_arg", "created", "expire", "args", "status",  "result")
        model = Task

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)
    
db.create_all()
db.engine.dispose()