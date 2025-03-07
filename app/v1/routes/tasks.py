from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.task import Task
from app.services.task import TaskService
from app import db

#Define the Blueprint
tasks_bp = Blueprint('tasks', __name__)

# Define valid enums for validation
VALID_STATUSES = {"pending", "in_progress", "completed"}
VALID_PRIORITIES = {"low", "medium", "high"}

# CREATE TASK
@tasks_bp.route('/', methods=['POST'])
@jwt_required()
def create_task():
  data = request.json

  # Check for missing fields
  REQUIRED_FIELDS = ["title", "status", "priority", "due_date"]
  missing_fields = [field for field in REQUIRED_FIELDS if field not in data]
  if missing_fields:
    return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400


  try:
    due_date = datetime.fromisoformat(data['due_date'])  # Convert to datetime
  except (ValueError, KeyError):
    return jsonify({"error": "Invalid or missing due_date. Use ISO format: YYYY-MM-DDTHH:MM:SS"}), 400

  if "status" in data and data["status"] not in VALID_STATUSES:
    return jsonify({
      "error": f"Invalid status '{data['status']}'. Allowed values: {list(VALID_STATUSES)}"
    }), 400

  # Validate `priority` if provided
  if "priority" in data and data["priority"] not in VALID_PRIORITIES:
    return jsonify({
      "error": f"Invalid priority '{data['priority']}'. Allowed values: {list(VALID_PRIORITIES)}"
    }), 400

  completed_at = None # Defaulted to null

  new_task = Task(
    title=data['title'],
    description=data.get('description'),
    status=data['status'],
    priority=data['priority'],
    due_date=due_date,
    completed_at=completed_at
  )

  db.session.add(new_task)
  db.session.commit()
  return jsonify(new_task.to_dict()), 201

# RETRIEVE ALL TASKS
@tasks_bp.route('/', methods=['GET'])
def get_tasks():
  tasks = Task.query.all()

  return jsonify([task.to_dict() for task in tasks]), 200

# RETRIEVE ONE TASK BY ID
@tasks_bp.route('/<uuid:task_id>', methods=['GET'])
def get_task(task_id):
  task = TaskService.get_task(task_id)

  if not task:
    return jsonify({"error": "Task not found"}), 404

  return jsonify(task.to_dict()), 200

# UPDATE ONE TASK BY ID
@tasks_bp.route('/<uuid:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
  task = TaskService.get_task(task_id)

  if not task:
    return jsonify({"error": "Task not found"}), 404

  data = request.json
  if "status" in data and data["status"] not in VALID_STATUSES:
    return jsonify({
      "error": f"Invalid status '{data['status']}'. Allowed values: {list(VALID_STATUSES)}"
    }), 400

  # Validate `priority` if provided
  if "priority" in data:
    if data["priority"] not in VALID_PRIORITIES:
      return jsonify({
        "error": f"Invalid priority '{data['priority']}'. Allowed values: {list(VALID_PRIORITIES)}"
      }), 400

  # Prevent users from directly modifying completed_at
  if 'completed_at' in data:
      return jsonify({"error": "You cannot modify completed_at manually"}), 403

  # Validate `due_date`
  if 'due_date' in data:
    try:
      due_date = datetime.fromisoformat(data['due_date'])  # Convert to datetime
      if due_date < datetime.now():
        return jsonify({"error": "due_date cannot be in the past"}), 400  # Prevent past due_date
      task.due_date = due_date  # Set valid due_date

    except (ValueError, KeyError):
      return jsonify({"error": "Invalid or missing due_date. Use ISO format: YYYY-MM-DDTHH:MM:SS"}), 400

  updated_task = TaskService.update_task(data, task)

  db.session.commit()
  return jsonify({"message": "Task updated", "task": updated_task.to_dict()}), 200

# DELETE TASK
@tasks_bp.route('/<uuid:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
  task = TaskService.get_task(task_id)

  if not task:
    return jsonify({"error": "Task not found"}), 404

  db.session.delete(task)
  db.session.commit()
  return jsonify({"message": "Task deleted successfully"}), 200
