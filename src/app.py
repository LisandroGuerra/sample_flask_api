from flask import Flask, request, jsonify
from models.task import Task

app = Flask(__name__)

tasks = []
task_id_control = 1

@app.route('/tasks', methods=['POST'])
def create_task():
    global task_id_control
    data = request.get_json()
    new_task = Task(id=task_id_control ,title=data['title'], description=data.get('description', ''))
    task_id_control += 1
    tasks.append(new_task)
    print(tasks)
    return jsonify({"message": "Task created successfully", "id": new_task.id}), 201
    # return jsonify(new_task.to_dict()), 201

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks_list = [task.to_dict() for task in tasks]

    output = {
        "tasks": tasks_list,
        "total_tasks": len(tasks_list)
    }

    return jsonify(output), 200

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    for task in tasks:
        if task.id == task_id:
            return jsonify(task.to_dict()), 200
    return jsonify({"message": "Task not found"}), 404

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    for task in tasks:
        if task.id == task_id:
            task.title = data['title']
            task.description = data.get('description', '')
            task.completed = data.get('completed', False)
            return jsonify({"message": "Task updated successfully"}), 201
    return jsonify({"message": "Task not found"}), 404

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
            return jsonify({"message": "Task deleted successfully"}), 200
    return jsonify({"message": "Task not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
