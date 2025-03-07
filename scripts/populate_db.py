import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.models.task import Task
from app import create_app, db
from datetime import datetime, timedelta
import random

app = create_app()

# Task titles and descriptions
TASK_TITLES = [
    "Fix bug in API", "Implement login system", "Optimize database queries", "Update documentation",
    "Refactor authentication module", "Deploy new version", "Improve test coverage", "Set up CI/CD pipeline",
    "Write unit tests", "Research AWS scalability options"
]
TASK_DESCRIPTIONS = [
    "This task requires fixing a major issue.", "User authentication needs enhancements.",
    "Optimize queries for better performance.", "Documentation needs an update.",
    "Refactoring needed for better maintainability.", "Prepare deployment for production.",
    "Increase test coverage for better stability.", "Setup continuous integration pipeline.",
    "Ensure unit tests cover all edge cases.", "Look into AWS auto-scaling solutions."
]

try:
   with app.app_context():
        print("Dropping all tables... 🚨")
        db.drop_all()  # Deletes all tables
        print("All tables dropped!")

        print("Recreating all tables... 🔄")
        db.create_all()  # Recreates tables based on models
        print("Database reset successfully! 🎯")

        for i in range(50):
            title = random.choice(TASK_TITLES)
            description = random.choice(TASK_DESCRIPTIONS)
            priority = random.choice(["low", "medium", "high"])
            due_date = datetime.fromisoformat("2025-03-10T18:00:00")

            # 50% of tasks should be completed
            is_completed = random.choice([True, False])

            if is_completed:
                status = "completed"
                completed_at = datetime.now() - timedelta(days=random.randint(1, 30))  # Completed in past 1-30 days
            else:
                status = random.choice(["pending", "in_progress"])  # Keep some tasks as pending/in_progress
                completed_at = None  # Not completed

            new_task = Task(
                title=title,
                description=description,
                status=status,
                priority=priority,
                due_date=due_date,
                completed_at=completed_at
            )

            db.session.add(new_task)

        db.session.commit()
        print("✅ 50 tasks added successfully! (50% completed)")

except Exception as e:
    with app.app_context():
        db.session.rollback()  # Rollback in case of failure
        print(f"❌ Error occurred: {e}", file=sys.stderr)

finally:
    with app.app_context():
        db.session.remove()  # Close database session
    sys.exit(0)  # Exit script
