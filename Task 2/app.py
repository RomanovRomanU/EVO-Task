from flask import Flask
from flask import render_template, request, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from hashlib import sha256
from threading import Lock

ALLOWED_EXTENSIONS = ('txt', 'pdf', 'doc', 'docx', 'jpg')
app = Flask(__name__,static_url_path = "/static")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////documents.db'
db = SQLAlchemy(app)
lock = Lock()

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Sha will represent like hex (length = 64)
    hex_sha = db.Column(db.String(64), unique=True)
    # How many times this document was uploaded
    count = db.Column(db.Integer)

    def __init__(self, hex_sha):
        self.hex_sha = hex_sha
        self.count = 1

    def __repr__(self):
        return 'SHA of file is: %s' % self.hex_sha


def allowed_filename(filename):
    if '.' not in filename:
        return False
    extension = filename.split('.')[1].lower()
    if extension not in ALLOWED_EXTENSIONS:
        return False
    else:
        return True


# Route for rendering all appointments in database
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/download', methods=['POST'])
def download_file():
    # If there is no file dowloaded
    if 'file' not in request.files:
        return
    file = request.files['file']
    # If the file isn`t empty and having proper filename
    if file and allowed_filename(file.filename):
        # Reading the content of file
        file_repr = str(file.stream.read())
        # Convert it to utf-8
        # Ignore means,that we pass chars,that we can`t convert
        file_repr = file_repr.encode('utf-8')
        file_hex_sha = sha256(file_repr)
        # file_hex_sha.update(file_repr)
        file_hex_sha = file_hex_sha.hexdigest()
        lock.acquire()
        # Searching for the same document in database
        db_file = Document.query.filter_by(hex_sha=file_hex_sha).first()
        # DEBUG
        debug = (str(Document.query.all()))
        # If there is no such document in database
        if db_file is None:
            new_db_file = Document(file_hex_sha)
            db.session.add(new_db_file)
            db.session.commit()
            response = '%s %s' % (
                str(new_db_file.hex_sha), str(new_db_file.count)
                )
            response += " %s" % str(new_db_file.id)
            response += " " + debug
            lock.release()
            return response
        # If we found same document
        else:
            db_file.count += 1
            new_count = db_file.count
            db.session.commit()
            response = '%s %s' % (str(db_file.hex_sha), str(new_count))
            response += " %s" % str(db_file.id)
            response += " " + debug
            lock.release()
            return response
    else:
        # Bad request
        abort(400)


if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0', port=8080, threaded=False)
