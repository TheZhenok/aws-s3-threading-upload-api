# Python
from werkzeug.datastructures import FileStorage

# Flask
import flask

# Local
import services
import config


app: flask.Flask = flask.Flask(__name__)
file_handler = services.FileHandler()

@app.route('/upload', methods=['POST'])
def upload():
    # Получаем файл из запроса.
    file: FileStorage = flask.request.files['file']

    # Загружаем файл на S3.
    is_successful: bool = file_handler.upload_to_s3(file)
    if is_successful:
        return '', 200
    
    return flask.jsonify({'error': 'file is not upload'}), 521

@app.route('/')
def main_page():
    return flask.render_template('index.html')

if __name__ == "__main__":
    app.run(
        host=config.SERVER_HOST,
        port=config.SERVER_PORT,
        debug=config.SERVER_DEBUG
    )
