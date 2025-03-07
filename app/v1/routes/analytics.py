from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import io
from app.models.task import Task
from app.services.upload import UploadService

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route("/", methods=['GET'])
@jwt_required()
def get_task_analytics():
  tasks = Task.query.all()

  if not tasks:
    return jsonify({"error": "No tasks available"})

  df = pd.DataFrame([task.to_dict() for task in tasks])

  # Convert date columns
  df['created_at'] = pd.to_datetime(df['created_at'])
  df['completed_at'] = pd.to_datetime(df['completed_at'])

  if df['completed_at'].isna().all():
    return jsonify({"error": "No tasks have been completed yet"}), 400

  insights = {}

  # ** Task Completion Rate Over Time (Line Chart)**
  if "completed_at" in df.columns:
    completion_trends = df.resample("D", on="completed_at").count()["id"]
    plt.figure(figsize=(12, 4))
    sns.lineplot(x=completion_trends.index, y=completion_trends.values)
    plt.xlabel("Date")
    plt.ylabel("Tasks Completed")
    plt.title("Task Completion Rate Over Time")
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    insights["completion_trends_url"] = UploadService.to_s3(buffer, "completion_trends.png")

  # ** Average Time to Completion per Priority Level (Bar Chart)**
  if "completed_at" in df.columns and "due_date" in df.columns:
    df["completed_at"] = pd.to_datetime(df["completed_at"], errors='coerce')
    df["due_date"] = pd.to_datetime(df["due_date"], errors='coerce')
    df["completion_time"] = (df["completed_at"] - df["due_date"]).dt.total_seconds() / 3600
    avg_completion_time = df.groupby("priority")["completion_time"].mean()
    plt.figure(figsize=(8, 4))
    sns.barplot(y=avg_completion_time.index, x=avg_completion_time.values)
    plt.ylabel("Priority Level")
    plt.xlabel("Avg Completion Time (Hours)")
    plt.title("Average Time to Completion per Priority Level (Sorted)")
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    insights["completion_time_url"] = UploadService.to_s3(buffer, "completion_time.png")

  # ** Distribution of Tasks by Status (Pie Chart)**
  status_counts = df["status"].value_counts()
  plt.figure(figsize=(6, 6))
  plt.pie(status_counts, labels=status_counts.index, autopct="%1.1f%%", startangle=140)
  plt.title("Distribution of Tasks by Status")
  buffer = io.BytesIO()
  plt.savefig(buffer, format="png")
  buffer.seek(0)
  insights["status_distribution_url"] = UploadService.to_s3(buffer, "status_distribution.png")

  # Return JSON Response**
  insights["total_tasks"] = len(df)
  insights["completed_tasks"] = df[df["status"] == "completed"].shape[0]
  insights["pending_tasks"] = df[df["status"] == "pending"].shape[0]
  insights["in_progress_tasks"] = df[df["status"] == "in_progress"].shape[0]

  return jsonify(insights), 200
