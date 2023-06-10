from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)


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

@app.route('/')
def hello_world():
    return 'this is daniels portfolio check change'


@app.route('/tasks', methods=['GET'])
def get_tasks():
    with app.app_context():
        tasks = Task.query.all()
        tasks = [task.to_dict() for task in tasks]
        return jsonify(tasks)


@app.route('/tasks', methods=['POST'])
def create_task():
    with app.app_context():
        data = request.get_json()
        text = data.get('text')
        if not text:
            return jsonify({'error': 'Text is required'}), 400
        task = Task(text=text)
        db.session.add(task)
        db.session.commit()
        return jsonify(task.to_dict()), 201


@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    with app.app_context():
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


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    with app.app_context():
        task = Task.query.get(task_id)
        if not task:
            return jsonify({'error': 'Task not found'}), 404
        db.session.delete(task)
        db.session.commit()
        return '', 204


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()
