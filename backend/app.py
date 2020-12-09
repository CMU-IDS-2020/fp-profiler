from flask import Flask, request
import os
from subprocess import Popen, PIPE
import json

from prof_file_util import load_source, load_line_profile, load_graph_profile
from linewise_barchart import linewise_barchart
from valgrind import extract_valgrind_result
from mem_issue_visualize import mem_issue_visualize

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
    # print(code)
    local_path = 'temp.c' # TODO: hash file names to handle concurrency issues
    with open(local_path, 'w') as f:
        f.write(code)

    process = Popen(['wc', '-l', local_path], stdout=PIPE)
    (output, err) = process.communicate()
    exit_code = process.wait()

    # print(output)
    # with open('test.json') as f:
    #     s = json.load(f)

    ret_dict = {}

    '''
    Invoke compiler (if need) and profiler to generate the results.
    '''
    os.system('clang-format -i {}'.format(local_path))
    compile_retvalue = os.system('gcc -g -pg {} -o prog 1> gcc_output 2>&1'.format(local_path))
    # handle compiling error
    if compile_retvalue != 0:
        ret_dict['error'] = 1
        ret_dict['source'] = ''.join(list(open(local_path, 'r').readlines()))
        ret_dict['error_message'] = ''.join(list(open('gcc_output', 'r').readlines()))
        return ret_dict

    os.system('./prog')
    os.system('ctags --fields=+ne -o - --sort=no {} 1> ctags_output 2>&1'.format(local_path))
    os.system('gprof --graph prog gmon.out 1> graph_file 2>&1')
    os.system('gprof -l prog gmon.out 1> linewise_file 2>&1')

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
        graph_dct = load_graph_profile('graph_file')
        for k, v in graph_dct.items():
            ret_dict[k] = v
    else:
        ret_dict['vega_json'] = json.load(open('test.json', 'r'))
    # print(uninitialised_buffer, invalid_write_buffer, mem_leak_dic)

    return ret_dict

@app.route('/mem-profile', methods = ['POST'])
def mem_profile():
    '''
    shall return a json dict
    if succeeds, 
    {
        'error': 0,
        'vega_json': ...
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
    # print(code)
    local_path = 'temp.c' # TODO: hash file names to handle concurrency issues
    with open(local_path, 'w') as f:
        f.write(code)

    process = Popen(['wc', '-l', local_path], stdout=PIPE)
    (output, err) = process.communicate()
    exit_code = process.wait()

    # print(output)
    # with open('test.json') as f:
    #     s = json.load(f)

    ret_dict = {}
    '''
    Invoke compiler (if need) and profiler to generate the results.
    '''
    os.system('clang-format -i {}'.format(local_path))
    compile_retvalue = os.system('gcc -pedantic -g {} -o exec 1> gcc_output 2>&1'.format(local_path))

    if compile_retvalue != 0:
        ret_dict['error'] = 1
        ret_dict['source'] = ''.join(list(open(local_path, 'r').readlines()))
        ret_dict['error_message'] = ''.join(list(open('gcc_output', 'r').readlines()))
        return ret_dict

    os.system('valgrind ./exec > valgrind.txt')
    uninitialised_buffer, invalid_write_buffer = extract_valgrind_result('other', 'valgrind.txt')
    os.system('valgrind --leak-check=full ./exec > valgrind_leak.txt')
    mem_leak_dic = extract_valgrind_result('memory_leak', 'valgrind_leak.txt')


    ret_dict['error'] = 0
    vega_chart = mem_issue_visualize(local_path, uninitialised_buffer, invalid_write_buffer, mem_leak_dic)
    ret_dict['vega_json'] = json.loads(vega_chart.to_json())

    return ret_dict

    