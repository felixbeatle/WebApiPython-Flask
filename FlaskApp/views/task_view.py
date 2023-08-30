from flask import Blueprint, jsonify, request
from models.task_model import Task
from helpers.token_validation import validateToken
from database.__init__ import database

task = Blueprint("task", __name__)


@task.route("/", methods=["POST"])
def create_task():
    try:
        # Get the token from the request headers
        token = request.headers.get('x-access-token')

        # Validate the token using the validateToken function
        token_info = validateToken()
        if isinstance(token_info, int):
            if token_info == 400:
                return jsonify({"error": 'Token is missing in the request, please try again'}), 401
            elif token_info == 401:
                return jsonify({"error": 'Invalid authentication token, please login again'}), 403

        # Check if 'description' and 'assignedToUid' keys are present in the request data
        data = request.get_json()
        if 'description' not in data or 'assignedToUid' not in data:
            raise ValueError('Error validating form')

        # Get the user who is making the request (createdBy)
        created_by_uid = token_info['id']

        # Get the assignedTo user from the request data
        assigned_to_uid = data['assignedToUid']

        # Create a new Task object with the provided data
        new_task = Task(
            createdByUid=created_by_uid,
            assignedToUid=assigned_to_uid,
            description=data['description']
        )

        # Save the new task to the database
        collection = database.dataBase['tasks']
        created_task = collection.insert_one(new_task.to_dict())

        return jsonify({'id': str(created_task.inserted_id)})

    except ValueError as err:
        return jsonify({"error": str(err)}), 400


@task.route("/tasks/createdby/", methods=["GET"])
def get_tasks_created_by_user():
    try:
        # Get the token from the request headers
        token = request.headers.get('x-access-token')

        # Validate the token using the validateToken function
        token_info = validateToken()
        if isinstance(token_info, int):
            if token_info == 400:
                return jsonify({"error": 'Token is missing in the request, please try again'}), 401
            elif token_info == 401:
                return jsonify({"error": 'Invalid authentication token, please login again'}), 403

        # Get the createdBy user from the token information
        created_by_uid = token_info['id']

        # Access the Database and fetch all tasks created by the user
        collection = database.dataBase['tasks']
        user_created_tasks = collection.find({'createdByUid': created_by_uid}, {'_id': 0})

        # Prepare the list of tasks to be returned in the response
        tasks_list = [task for task in user_created_tasks]

        return jsonify(tasks_list)

    except ValueError as err:
        return jsonify({"error": str(err)}), 400


@task.route("/tasks/assignedto/", methods=["GET"])
def get_tasks_assigned_to_user():
    try:
        # Get the token from the request headers
        token = request.headers.get('x-access-token')

        # Validate the token using the validateToken function
        token_info = validateToken()
        if isinstance(token_info, int):
            if token_info == 400:
                return jsonify({"error": 'Token is missing in the request, please try again'}), 401
            elif token_info == 401:
                return jsonify({"error": 'Invalid authentication token, please login again'}), 403

        # Get the assignedTo user from the token information
        assigned_to_uid = token_info['id']

        # Access the Database and fetch all tasks assigned to the user
        collection = database.dataBase['tasks']
        user_assigned_tasks = collection.find({'assignedToUid': assigned_to_uid}, {'_id': 0})

        # Prepare the list of tasks to be returned in the response
        tasks_list = [task for task in user_assigned_tasks]

        return jsonify(tasks_list)

    except ValueError as err:
        return jsonify({"error": str(err)}), 400

from bson import ObjectId

@task.route("/tasks/<taskUid>", methods=["PATCH"])
def update_task(taskUid):
    try:
        # Get the token from the request headers
        token = request.headers.get('x-access-token')

        # Validate the token using the validateToken function
        token_info = validateToken()
        if isinstance(token_info, int):
            if token_info == 400:
                return jsonify({"error": 'Token is missing in the request, please try again'}), 401
            elif token_info == 401:
                return jsonify({"error": 'Invalid authentication token, please login again'}), 403

        # Get the assignedTo user from the token information
        assigned_to_uid = token_info['id']

        # Check if 'done' key is present in the request data
        data = request.get_json()
        if 'done' not in data:
            return jsonify({"error": 'Status done not found in the request'}), 400

        # Convert the taskUid to ObjectId format
        task_object_id = ObjectId(taskUid)

        # Access the Database and find the task to be updated
        collection = database.dataBase['tasks']
        task_to_update = collection.find_one({'_id': task_object_id})

        if not task_to_update:
            raise ValueError('Task not found')

        # Check if the assignedToUid for that task matches the user Uid making the request
        if task_to_update['assignedToUid'] != assigned_to_uid:
            raise ValueError('Users can only change status when the task is assigned to them.')

        # Update the 'done' status of the task in the database
        collection.update_one({"_id": task_object_id}, {"$set": {"done": data['done']}})

        return jsonify({"taskUid": taskUid})

    except ValueError as err:
        return jsonify({"error": str(err)}), 400


@task.route("/tasks/<taskUid>", methods=["DELETE"])
def delete_task(taskUid):
    try:
        # Get the token from the request headers
        token = request.headers.get('x-access-token')

        # Validate the token using the validateToken function
        token_info = validateToken()
        if isinstance(token_info, int):
            if token_info == 400:
                return jsonify({"error": 'Token is missing in the request, please try again'}), 401
            elif token_info == 401:
                return jsonify({"error": 'Invalid authentication token, please login again'}), 403

        # Get the createdBy user from the token information
        created_by_uid = token_info['id']

        # Convert the taskUid to ObjectId format
        task_object_id = ObjectId(taskUid)

        # Access the Database and find the task to be deleted
        collection = database.dataBase['tasks']
        task_to_delete = collection.find_one({'_id': task_object_id})

        if not task_to_delete:
            raise ValueError('Task not found')

        # Check if the createdByUid for that task matches the user Uid making the request
        if task_to_delete['createdByUid'] != created_by_uid:
            raise ValueError('Users can only delete when the task is created by them.')

        # Delete the task from the database
        task_delete_attempt = collection.delete_one({"_id": task_object_id})

        return jsonify({'tasksAffected': task_delete_attempt.deleted_count}), 200

    except ValueError as err:
        return jsonify({"error": str(err)}), 400
