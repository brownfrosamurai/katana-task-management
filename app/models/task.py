from app import db
import uuid
from datetime import datetime

class Task(db.Model):
  __tablename__ = 'tasks'

  id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
  title = db.Column(db.String(255), nullable=False)
  description = db.Column(db.Text, nullable=True)
  status = db.Column(db.Enum('pending', 'in_progress', 'completed', name='task_status'), nullable=False)
  priority = db.Column(db.Enum('low', 'medium', 'high', name='task_priority'), nullable=False)
  due_date = db.Column(db.DateTime, nullable=False)
  completed_at = db.Column(db.DateTime, nullable=True)
  created_at = db.Column(db.DateTime, server_default=db.func.now())
  updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

  def to_dict(self):
    return {
      "id": self.id,
      "title": self.title,
      "description": self.description,
      "status": self.status,
      "priority": self.priority,
      "due_date": self.due_date,
      "completed_at": self.completed_at,
      "created_at": self.created_at,
      "updated_at": self.updated_at
    }