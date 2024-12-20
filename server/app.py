from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, Message

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

CORS(app)
migrate = Migrate(app, db)
db.init_app(app)


@app.route("/messages", methods=["GET"])
def get_messages():
    """Retrieve all messages ordered by creation time."""
    messages = Message.query.order_by(Message.created_at).all()
    return jsonify([message.to_dict() for message in messages]), 200


@app.route("/messages", methods=["POST"])
def create_message():
    """Create a new message."""
    data = request.get_json()
    if not data.get("body") or not data.get("username"):
        return jsonify({"error": "Both 'body' and 'username' are required."}), 400

    new_message = Message(body=data["body"], username=data["username"])
    db.session.add(new_message)
    db.session.commit()
    return jsonify(new_message.to_dict()), 201


@app.route("/messages/<int:id>", methods=["PATCH"])
def update_message(id):
    """Update the body of an existing message."""
    data = request.get_json()
    message = db.session.get(Message, id)  # Updated to use Session.get()

    if not message:
        return jsonify({"error": "Message not found"}), 404

    if "body" in data:
        message.body = data["body"]
    db.session.commit()
    return jsonify(message.to_dict()), 200


@app.route("/messages/<int:id>", methods=["DELETE"])
def delete_message(id):
    """Delete a message."""
    message = db.session.get(Message, id)  # Updated to use Session.get()

    if not message:
        return jsonify({"error": "Message not found"}), 404

    db.session.delete(message)
    db.session.commit()
    return "", 204


if __name__ == "__main__":
    app.run(port=5555)