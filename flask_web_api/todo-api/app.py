from flask import Flask,jsonify,abort,request,url_for
import json
from flask_httpauth import HTTPBasicAuth
app = Flask(__name__)
auth = HTTPBasicAuth()
tasks = [
    {
        'id':1,
        'title':u'buy groceries',
        'description':u'milk,cheese,pizza,fruit,tylenol',
        'done':False
    },
    {
        'id':2,
        'title':u'learn python',
        'description':u'need to find a good python tutorial on web',
        'done':False
    }
]
@auth.get_password
def get_password(username):
    if username == 'ok':
        return 'python'
    return None

@auth.error_handler
def unauthorized():
    return jsonify({'error':'Unauthorized access'}),401

def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_tasks', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    # print(new_task)
    return new_task

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks1():
    return jsonify({'tasks': list(map(make_public_task, tasks))})

@app.route('/todo/api/v1.0/tasks/<int:task_id>',methods=['GET'])
@auth.login_required
def get_tasks(task_id):
    task = list(filter(lambda t:t['id'] == task_id,tasks))
    #　print(task)
    if len(task) ==0:
        abort(404)
    return jsonify({'tasks': list(map(make_public_task, task))[0]})

@app.route('/todo/api/v1.0/tasks',methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)

    task = {
        'id':tasks[-1]['id'] +1,
        'title': request.json['title'],
        'description': request.json.get('description',""),
        'done':False

    }
    tasks.append(task)
    return jsonify({'task':task}),201

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = list(filter(lambda t:t['id'] == task_id,tasks))

    if len(task) ==0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json :
        abort(400)
    if 'description' in request.json :
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)

    task[0]['title'] = request.json.get('title',task[0]['title'])
    task[0]['description'] = request.json.get('description',task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])

    return jsonify({'task': task[0]})

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
def delete(task_id):
    task = list(filter(lambda t:t['id'] ==task_id,tasks))
    if len(task) ==0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result':True})

if __name__ == '__main__':
    app.run(debug=True)