
from flask import Flask
from views import views
from datetime import timedelta
import sqlalchemy


app = Flask(__name__)
app.register_blueprint(views, url_prefix="/views")

app.secret_key = "helloTest"

app.permanent_session_lifetime = timedelta(minutes=5)

if __name__ == '__main__':
    app.run(debug=True, port=8000)

