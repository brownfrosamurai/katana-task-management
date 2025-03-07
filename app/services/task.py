from flask.json import jsonify
from app.models.task import Task
from datetime import datetime
from app import db

class TaskService:
  @staticmethod
  def get_task(task_id):
    #Reteive task by id
    task = Task.query.get(str(task_id))
    return task

  @staticmethod
  def update_task(data, task):
     # Update only allowed fields
    allowed_fields = ['title', 'description', 'status', 'priority']
    for field in allowed_fields:
      if field in data:
        setattr(task, field, data[field])  # Update task fields

    # Automatically set completed_at when status is changed to 'completed'
    if task.status == 'completed' and task.completed_at is None:
      task.completed_at = db.func.now()

    # Reset completed_at if status changes from 'completed' to anything else
    elif task.completed_at and task.status != 'completed':
      task.completed_at = None

    return task

        # Validate `status` if provided
    if "status" in data:
      if data["status"] not in TaskService.VALID_STATUSES:
        return jsonify({
          "error": f"Invalid status '{data['status']}'. Allowed values: {list(TaskService.VALID_STATUSES)}"
        }), 400

    # Validate `priority` if provided
    if "priority" in data:
      if data["priority"] not in TaskService.VALID_PRIORITIES:
        return jsonify({
          "error": f"Invalid priority '{data['priority']}'. Allowed values: {list(TaskService.VALID_PRIORITIES)}"
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

