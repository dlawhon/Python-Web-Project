from flask import Flask
from flask_login import LoginManager
from views import views
from datetime import timedelta

app = Flask(__name__)

app.app_context().push()

app.register_blueprint(views, url_prefix="/views")

app.secret_key = "D4PKmibxBeEnaYycm3Lo"

app.permanent_session_lifetime = timedelta(minutes=5)

if __name__ == '__main__':
    app.run(debug=True, port=8000)