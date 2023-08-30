from flask import Flask
from views.user_view import user
from views.task_view import task

app = Flask(__name__)

app.register_blueprint(task, url_prefix='/tasks')
app.register_blueprint(user)


@app.route("/")
def index():
    return "HOME"


if __name__ == "__main__":
    app.run()
