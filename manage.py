from flask.cli import FlaskGroup
from src import app,db
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

import getpass
from sqlalchemy.exc import SQLAlchemyError

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
        user = User(email=email, password=password, is_admin=1)
        db.session.add(user)
        db.session.commit()
        print("Admin user created successfully.")
    except SQLAlchemyError as e:
        print("Couldn't create admin user:", str(e))
        db.session.rollback()
    except Exception as e:
        print("An unexpected error occurred:", str(e))
        db.session.rollback()


if __name__ == "__main__":
    cli()