from flask import Flask, render_template
from flask_bootstrap import Bootstrap

bootstrap = Bootstrap()

def create_app(test_config=None):
  app = Flask(__name__, instance_relative_config=True)
  
  bootstrap.init_app(app)

  from .routes import studentroute, courseroute

  app.register_blueprint(courseroute.course_bp)
  app.register_blueprint(studentroute.student_bp)

  @app.route('/')
  def index():
      return render_template('homepage.html')

  return app
