#!/usr/bin/env python3

from random import choice as rc
from faker import Faker

from app import app
from models import db, Message

fake = Faker()

usernames = [fake.first_name() for _ in range(4)]
if "Liza" not in usernames:
    usernames.append("Liza")


def make_messages():
    """Seed the database with fake data for testing."""
    with app.app_context():
        # Clear existing messages
        Message.query.delete()

        # Generate 20 fake messages
        messages = [
            Message(
                body=fake.sentence(),
                username=rc(usernames),
            )
            for _ in range(20)
        ]

        # Add sample test message
        test_message = Message(body="Hello 👋", username="Liza")
        messages.append(test_message)

        # Commit to the database
        db.session.add_all(messages)
        db.session.commit()

        print(f"Seeded {len(messages)} messages.")


if __name__ == "__main__":
    make_messages()