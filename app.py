from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

application = Flask(__name__)
cors = CORS(application)

application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(application)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'completed': self.completed
        }

@application.route('/')
def hello_world():
    return 'this is daniels portfolio check change'


@application.route('/tasks', methods=['GET'])
def get_tasks():
    with application.app_context():
        tasks = Task.query.all()
        tasks = [task.to_dict() for task in tasks]
        return jsonify(tasks)


@application.route('/tasks', methods=['POST'])
def create_task():
    with application.app_context():
        data = request.get_json()
        text = data.get('text')
        if not text:
            return jsonify({'error': 'Text is required'}), 400
        task = Task(text=text)
        db.session.add(task)
        db.session.commit()
        return jsonify(task.to_dict()), 201


@application.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    with application.app_context():
        task = Task.query.get(task_id)
        if not task:
            return jsonify({'error': 'Task not found'}), 404
        data = request.get_json()
        text = data.get('text')
        completed = data.get('completed')
        if text:
            task.text = text
        if completed is not None:
            task.completed = completed
        db.session.commit()
        return jsonify(task.to_dict())


@application.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    with application.app_context():
        task = Task.query.get(task_id)
        if not task:
            return jsonify({'error': 'Task not found'}), 404
        db.session.delete(task)
        db.session.commit()
        return '', 204


if __name__ == '__main__':
    with application.app_context():
        db.create_all()
    application.run()
