from flask import Flask
from actblue.actblue import mod as actblue_module

app = Flask(__name__)
app.register_blueprint(actblue_module, url_prefix="/actblue")


@app.route("/")
def index():
    return "Hello from EW!", 200

if __name__ == "__main__":
    app.run()
