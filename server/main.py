from flask import Flask, render_template
from flask_cors import CORS

from database import create_database
from handler import handle_upload_file

app = Flask(__name__)
CORS(app)  # Allow CORS for all routes


@app.route("/")
def index():
    return render_template("index.html")


# Endpoint for uploading files
@app.route("/upload", methods=["POST"])
def upload_file():
    try:
        isSuccess, message, code = handle_upload_file()
        if isSuccess:
            filename, response = message.split("\n", 1)
            return render_template("response.html", filename=filename, message=response)
        else:
            return render_template(
                "error.html", title=message, error_message=message, code=code
            )
    except Exception as e:
        return render_template(
            "error.html", title=message, error_message=str(e), code=code
        )


if __name__ == "__main__":
    # create_database()
    app.run(debug=True)
