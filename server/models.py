from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime

db = SQLAlchemy()


class Message(db.Model, SerializerMixin):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String, nullable=False)  # Message content
    username = db.Column(db.String, nullable=False)  # User who posted
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow
    )  # Timestamp of creation
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )  # Timestamp of last update

    def __repr__(self):
        # This is useful for debugging; consider removing or modifying for production
        return f"<Message {self.id}, {self.username}>"
