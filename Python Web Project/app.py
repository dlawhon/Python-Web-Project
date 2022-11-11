from flask import Flask
from views import views
from datetime import timedelta

#app = Flask(__name__)
app = Flask(__name__, template_folder='./')

app.app_context().push()

app.register_blueprint(views, url_prefix="/views")

app.secret_key = "helloTest"

app.permanent_session_lifetime = timedelta(minutes=5)

if __name__ == '__main__':
    app.run(debug=True, port=8000)