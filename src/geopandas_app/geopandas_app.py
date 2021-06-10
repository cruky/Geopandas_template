import pathlib, os

from flask import Flask, request, redirect, url_for, Response, jsonify
from werkzeug.utils import secure_filename

import src.geopandas_app.feature_class as feature_class

ALLOWED_EXTENSIONS = {'csv', 'zip'}

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024 # Max 20 megabytes file
app.config["UPLOAD_FOLDER"] = pathlib.Path('./file_storage')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def redirect_user():
    '''Redirect the user to our main page'''
    return redirect(url_for('upload_files'))


@app.route('/upload', methods=['POST'])
def upload_files():
    '''Get the file from the user'''
    errors = {}
    success = True
    gdb_path, csv_path = '', ''

    # check if the post request has the file part
    if 'files[]' not in request.files:
        resp = jsonify({'message': 'No file part in the request'})
        resp.status_code = 400
        return resp

    files = request.files.getlist('files[]')

    if all(not file.filename for file in files):
        resp = jsonify({'message': 'No files provided'})
        resp.status_code = 400
        return resp

    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = app.config['UPLOAD_FOLDER'] / filename
            file.save(file_path)
            if file_path.suffix == '.zip':
                gdb_path = file_path
            elif file_path.suffix == '.csv':
                csv_path = file_path
        else:
            success = False
            errors[file.filename] = 'File type is not allowed'

    if success:
        resp = jsonify({'Results': feature_class.run_geo_app(gdb_path,csv_path)})
        resp.status_code = 201
        return resp
    else:
        resp = jsonify(errors)
        resp.status_code = 500
        return resp



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.getenv('PORT')) # production
    # TODO: When running publicly rather than in development, you should not use the built-in development server . The development server is provided by Werkzeug for convenience,
    #  but is not designed to be particularly efficient, stable, or secure.
    # app.run(port=8000) # development
