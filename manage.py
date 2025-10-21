import os
import unittest
from app import blueprint
from app.main import create_app, db
from flask import Flask
from flask_migrate import Migrate
from app.main.model import user
from app.main.model import user_expense

app = create_app()
app.register_blueprint(blueprint)

migrate = Migrate(app, db)

@app.cli.command("runserver")
def runserver():
    """Run the Flask development server."""
    app.run(debug=True)


@app.cli.command("test")
def test():
    """Run unit tests."""
    tests = unittest.TestLoader().discover("app/test", pattern="test*.py")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        print("✅ All tests passed!")
        return 0
    else:
        print("❌ Some tests failed.")
        return 1

if __name__ == '__main__':
    app.run(debug=True)
