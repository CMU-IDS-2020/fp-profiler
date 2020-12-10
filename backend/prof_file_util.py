import pandas as pd
import re
from callgraph_json import extract, sort_node, generate_js_input

def load_source(source_file):
    code_lines = []
    line_num = 0
    for line in open(source_file, 'r'):
        line_num += 1
        code_lines.append(str(line_num) + '\t\t' + line)

    # print('Num of lines', len(code_lines))
    return code_lines    

def load_ctags_output(ctags_file):
    num_func_dict = {}
    for line in open(ctags_file, 'r'):
        tokens = line.strip().split('\t')
        if tokens[3] != 'f':
            continue
        func = tokens[0]
        begin_line_num = int(tokens[4].split(':')[1])
        end_line_num = int(tokens[6].split(':')[1])

        for idx in range(begin_line_num, end_line_num + 1):
            num_func_dict[idx] = func

    return num_func_dict

# with certain prof format
def load_profile(prof_file):
    line_num_dct = {}
    with open(prof_file, 'r') as rf:
        while True:
            line = rf.readline()
            if line.startswith(' time   seconds   seconds'):
                break

        while True:
            line = rf.readline()
            if line.startswith(' %         the percentage of'):
                break
            
            token_lst = re.split(r'[ ]+', line.strip())
            if len(token_lst) < 5:
                continue

            line_number = token_lst[-3]
            # print(line_number[(line_number.find(':') + 1):])
            line_number = int(line_number[(line_number.find(':') + 1):])

            line_num_dct[line_number] = [float(token_lst[0]), float(token_lst[1]),\
                float(token_lst[2]), token_lst[-4]]

    return line_num_dct
            
# return the data frame
def load_line_profile(source_file, prof_file):
    code_lines = load_source(source_file)
    line_num_dct = load_profile(prof_file)
    num_func_dct = load_ctags_output('ctags_output')

    time_percentage = []
    self_seconds = []
    func_names = []
    line_numbers = list(range(1, len(code_lines) + 1))
    
    for idx in line_numbers:
        if idx in line_num_dct:
            time_percentage.append(line_num_dct[idx][0])
            self_seconds.append(line_num_dct[idx][2])
        else:
            time_percentage.append(0.0)
            self_seconds.append(0.0)

        # use the dict built from ctags output
        if idx in num_func_dct:
            func_names.append(num_func_dct[idx])
        else:
            func_names.append('<not sampled>')

    return pd.DataFrame({
        'Line Number': line_numbers,
        'Source': code_lines,
        'Time %': time_percentage,
        'Time': self_seconds,
        'Func': func_names
    })

def load_graph_profile(graph_file):
    res = extract(graph_file)
    if res is None:
        return None
    total_edge, index_to_func, func_to_index = res
    node_list, edge_list = sort_node(total_edge, func_to_index, index_to_func)
    return generate_js_input(node_list, edge_list)
    

if __name__ == "__main__":
    # load_source('demo.c')
    # print(load_profile('linewise_file'))
    print(load_line_profile('demo.c', 'linewise_file'))
