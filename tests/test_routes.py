import unittest
from app import create_app, db
from app.models.task import Task
from flask_jwt_extended import create_access_token

class TaskManagementTestCase(unittest.TestCase):
  def setUp(self):
    self.app = create_app()
    self.client = self.app.test_client()
    with self.app.app_context():
      db.create_all()
      self.token = create_access_token(identity="testuser")

  def tearDown(self):
    with self.app.app_context():
      db.session.remove()
      db.drop_all()

  # def test_create_task(self):
  #   response = self.client.post(
  #     "/task/",
  #     json={"title": "Test Task", "status": "pending", "priority": "high", "due_date": "2025-03-10T12:00:00"},
  #     headers={"Authorization": f"Bearer {self.token}"}
  #   )
  #   self.assertEqual(response.status_code, 201)
  #   self.assertIn("task", response.json)

  def test_analytics_no_completed_tasks(self):
    response = self.client.get("/tasks/analytics/", headers={"Authorization": f"Bearer {self.token}"})
    self.assertEqual(response.status_code, 400)
    self.assertIn("No tasks have been completed yet", response.json["error"])

if __name__ == "__main__":
  unittest.main()