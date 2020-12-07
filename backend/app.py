from flask import Flask, request
import os
from subprocess import Popen, PIPE
import json

from prof_file_util import load_source, load_line_profile
from linewise_barchart import linewise_barchart

app = Flask(__name__)


@app.route('/upload-file', methods = ['POST'])
def hello():
    '''
    shall return a json dict
    if succeeds, 
    {
        'error': 0,
        'vega_json': ...
        'node_json': ...
        'edge_json': ...
        ...
    }
    if fails,
    {
        'error': 1,
        'source': formatted source code,
        'error_message': the compile failure message
    }
    '''
    code = request.get_json()['code']
    print(code)
    local_path = 'temp.c' # TODO: hash file names to handle concurrency issues
    with open(local_path, 'w') as f:
        f.write(code)

    process = Popen(['wc', '-l', local_path], stdout=PIPE)
    (output, err) = process.communicate()
    exit_code = process.wait()

    print(output)
    # with open('test.json') as f:
    #     s = json.load(f)

    ret_dict = {}

    '''
    Invoke compiler (if need) and profiler to generate the results.
    '''
    os.system('clang-format -i {}'.format(local_path))
    compile_retvalue = os.system('gcc -g -pg {} -o prog > gcc_output'.format(local_path))
    # handle compiling error
    if compile_retvalue != 0:
        ret_dict['error'] = 1
        ret_dict['source'] = ''.join(load_source(local_path))
        ret_dict['error_message'] = ''.join(list(open('gcc_output', 'r').readlines()))
        return ret_dict

    os.system('./prog')
    os.system('ctags --fields=+ne -o - --sort=no {} > ctags_output'.format(local_path))
    os.system('gprof --graph prog gmon.out  > graph_file')
    os.system('gprof -l prog gmon.out  > linewise_file')

    '''
    Now we have the outputs. Visualize and pass it back to the frontend.
    '''
    # for debug purpose. Only linux can host grof so far.
    ret_dict['error'] = 0
    if os.path.isfile('linewise_file') and os.path.getsize('linewise_file') > 0\
        and os.path.isfile('graph_file') and os.path.getsize('graph_file') > 0:
        df = load_line_profile(local_path, 'linewise_file')
        chart = linewise_barchart(df)
        # chart.save('new.json')
        '''
        TODO: Maybe the temporary files should be cleared or
        stored somewhere serving as history data.
        '''
        ret_dict['vega_json'] = json.loads(chart.to_json())
    else:
        ret_dict['vega_json'] = json.load(open('test.json', 'r'))

    return ret_dict
