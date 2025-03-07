from app import db
from app.utils.security import hash_password, verify_password
import uuid

class User(db.Model):
  __tablename__ = 'users'
  id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
  username = db.Column(db.String(150), unique=True, nullable=False)
  password_hash = db.Column(db.String(255), nullable=False)
  created_at = db.Column(db.DateTime, server_default=db.func.now())

  def set_password(self, password):
    self.password_hash = hash_password(password)

  def check_password(self, password):
    return verify_password(self.password_hash, password)

  def to_dict(self):
    return {"id": self.id, "username": self.username, "created_at": self.created_at}