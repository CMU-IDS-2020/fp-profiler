import pandas as pd
import re

def load_source(source_file):
    code_lines = []
    for line in open(source_file, 'r'):
        code_lines.append(line)

    # print('Num of lines', len(code_lines))
    return code_lines    

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

    time_percentage = []
    self_seconds = []
    func_names = []
    line_numbers = list(range(1, len(code_lines) + 1))
    
    for idx in line_numbers:
        if idx in line_num_dct:
            time_percentage.append(line_num_dct[idx][0])
            self_seconds.append(line_num_dct[idx][2])
            func_names.append(line_num_dct[idx][3])
        else:
            time_percentage.append(0.0)
            self_seconds.append(0.0)
            func_names.append('<not sampled>')

    return pd.DataFrame({
        'Line Number': line_numbers,
        'Source': code_lines,
        'Time %': time_percentage,
        'Time': self_seconds,
        'Func': func_names
    })
    

    

if __name__ == "__main__":
    # load_source('demo.c')
    # print(load_profile('linewise_file'))
    print(load_line_profile('demo.c', 'linewise_file'))