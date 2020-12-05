from flask import Flask, request
import os
from subprocess import Popen, PIPE
import json

from prof_file_util import load_line_profile
from linewise_barchart import linewise_barchart

app = Flask(__name__)


@app.route('/upload-file', methods = ['POST'])
def hello():
    file = request.files['file']
    local_path = os.path.join('temp', file.filename)
    file.save(local_path)

    process = Popen(['wc', '-l', local_path], stdout=PIPE)
    (output, err) = process.communicate()
    exit_code = process.wait()

    print(output)
    # with open('test.json') as f:
    #     s = json.load(f)

    '''
    Invoke compiler (if need) and profiler to generate the results.
    '''
    os.system('gcc -g -pg {} -o prog'.format(local_path))
    os.system('./prog')
    os.system('gprof --graph prog gmon.out  > graph_file')
    os.system('gprof -l prog gmon.out  > linewise_file')

    '''
    Now we have the outputs. Visualize and pass it back to the frontend.
    '''
    # for debug purpose. Only linux can host grof so far.
    if os.path.isfile('linewise_file'):
        df = load_line_profile(local_path, 'linewise_file')
        chart = linewise_barchart(df)
        # chart.save('new.json')


        '''
        TODO: Maybe the temporary files should be cleared or
        stored somewhere serving as history data.
        '''
        return json.loads(chart.to_json())
    else:
        return json.load('test.json')
