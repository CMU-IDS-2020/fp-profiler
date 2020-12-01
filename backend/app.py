from flask import Flask, request
import os
from subprocess import Popen, PIPE

app = Flask(__name__)


@app.route('/upload-file', methods = ['POST'])
def hello():
    file = request.files['file']
    local_path = os.path.join('temp', file.filename)
    file.save(local_path)

    process = Popen(['wc', '-l', local_path], stdout=PIPE)
    (output, err) = process.communicate()
    exit_code = process.wait()

    return output
