from flask import Flask, jsonify, abort, make_response, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/')
def index():
    return "Hello, World! Zażółć gęślą jaźń dwa razy."


@app.route('/elo')
def elo():
    return jsonify(["No siema."])


class TasksList(Resource):
    def get(self):
        return {'tasks': tasks}

    def post(self):
        if (not request.json) or ('title' not in request.json):
            abort(400)
        task = {
            'id': tasks[-1]['id'] + 1,
            'title': request.json['title'],
            'description': request.json.get('description', ""),
            'done': False
        }
        tasks.append(task)
        return {'task': task}, 201


class Task(Resource):
    def get(self, id):
        task = [task for task in tasks if task['id'] == id]
        if len(task) == 0:
            abort(404)
        return {'task': task[0]}


api.add_resource(TasksList, '/todo/api/v0.1/tasks', endpoint='tasks')
api.add_resource(Task, '/todo/api/v0.1/tasks/<int:id>', endpoint='task')


if __name__ == '__main__':
    app.run(debug=True, port=5005)
