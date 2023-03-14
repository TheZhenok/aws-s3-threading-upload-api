# Python
from werkzeug.datastructures import FileStorage

# Flask
import flask

# Local
import services
import config


app: flask.Flask = flask.Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload():
    # Получаем файл из запроса.
    file: FileStorage = flask.request.files['file']
    file_handler = services.FileHandler()

    # Загружаем файл на S3.
    file_handler.upload_to_s3(file)

    return '', 200

@app.route('/')
def main_page():
    return flask.render_template('index.html')

if __name__ == "__main__":
    app.run(
        host=config.SERVER_HOST,
        port=config.SERVER_PORT,
        debug=config.SERVER_DEBUG
    )
