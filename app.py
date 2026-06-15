from flask import Flask
from config import Config
from database.db import init_db
from controllers.student_controller import student_bp
from controllers.course_controller import course_bp
from controllers.auth_controller import auth_bp
from controllers.payment_controller import payment_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key = Config.SECRET_KEY
    init_db()  # Create SQLite tables
    app.register_blueprint(student_bp)
    app.register_blueprint(course_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(payment_bp)
    return app

if __name__=='__main__':
    app=create_app()
    app.run(debug=True)