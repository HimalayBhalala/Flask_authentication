from flask.cli import FlaskGroup
from src import app, db
from src.accounts.models import User
import unittest
import os

cli = FlaskGroup(app)

@cli.command("test")
def test():
    """Runs the unit tests without coverage."""
    tests_dir = "tests"
    if not os.path.exists(tests_dir):
        print("Tests directory not found.")
        return 1

    tests = unittest.TestLoader().discover(tests_dir)
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    else:
        return 1

if __name__ == "__main__":
    cli()

import getpass

@cli.command("create_admin")
def create_admin():
    """Creates the admin user."""
    email = input("Enter email address: ")
    password = getpass.getpass("Enter password: ")
    confirm_password = getpass.getpass("Enter password again: ")
    if password != confirm_password:
        print("Passwords don't match")
        return 1
    try:
        user = User(email=email, password=password, is_admin=True)
        db.session.add(user)
        db.session.commit()
    except Exception:
        print("Couldn't create admin user.")
