import numpy as np
import re
import json
import sys

baseWidth = 5

class Node:
    def __init__(self, selfcalled, selftime, childtime, totalpct, name):
        self.self_call = selfcalled
        self.self_time = selftime
        self.child_time = childtime
        self.total_pct = totalpct 
        self.name = name
        self.print_msg = 'Function {}. Called: {}, self running time: {}, child running time: {}, total CPU percentage: {}.'.format(self.name, self.self_call, self.self_time, self.child_time, self.total_pct)
    
    def __repr__(self):
        return self.print_msg
    
    def __str__(self):
        return self.print_msg

class Edge:
    def __init__(self, parent, child, childcalled, childtime, cctime):
        self.parent = parent
        self.child = child
        self.child_called = childcalled
        self.child_time = childtime
        self.grandchild_time = cctime
        self.print_msg = '{} called {} {} times. Time in child function: {}, time in grandchild function: {}'.format(self.parent, self.child, self.child_called, self.child_time, self.grandchild_time)
    
    def __repr__(self):
        return self.print_msg
    
    def __str__(self):
        return self.print_msg
        

def valid_check(raw_txt):
    '''
        check for valid call graph header
        input: 
            raw_txt     content of call graph text
    '''
    if (len(raw_txt) < 6):
        return 0

    if (re.sub('\s+', '', raw_txt[0])[:9] != "Callgraph"):
        return 0
    
    if (raw_txt[1] != '\n'):
        return 0
    
    if (raw_txt[2] != '\n'):
        return 0
    
    if (raw_txt[3].split(':')[0] != 'granularity'):
        return 0
    
    if (raw_txt[4] != '\n'):
        return 0
    
    if (re.sub('\s+', '', raw_txt[5]) != 'index%timeselfchildrencalledname'):
        return 0
    
    return 1


def extract(call_graph_path):
    '''
        input: file path of the call graph
    '''
    try:
        with open(call_graph_path, 'r') as f:
            raw_txt = f.readlines()
    except FileNotFoundError:
        print("No call graph input.")
        return

    # valid check
    if (valid_check(raw_txt) == 0):
        print("Wrong call graph text format.")
        return
    
    index_to_func = {}
    func_to_index = {}
    total_edge = []

    for i in range(6, len(raw_txt)):
        # <spontaneous> implies calling main or from signal process
        # do not support safe signal handler call graph
        if ('<spontaneous>' in raw_txt):
            continue
        
        if not 'cycle' in raw_txt[i]:
            # normal function
            info = re.sub('\s+', ',', raw_txt[i]).split(',')[:-1]
        else:
            # cycle
            new_cycle_index = re.search('<cycle (\w+) as a whole>', raw_txt[i])
            if new_cycle_index:
                # a whole cycle entry
                new_cycle_index = new_cycle_index.group(1)
            
                info = re.sub('<cycle \w+ as a whole>', '<cycle_{}>'.format(new_cycle_index), raw_txt[i])
                info = re.sub('\s+', ',', info).split(',')[:-1]
            else:
                # a component of the whole cycle
                new_func_name, prev_cycle_index = re.search('(\w+) <cycle (\w+)>', raw_txt[i]).group(1,2)
                info = re.sub('\w+ <cycle \w+>', '{}_<cycle_{}>'.format(new_func_name, prev_cycle_index), raw_txt[i])
                info = re.sub('\s+', ',', info).split(',')[:-1]


        new_entry = re.match('\[\d+\]', info[0])

        ''' Enter a new entry '''
        if (new_entry):
            new_index = int(new_entry[0][1:-1])
            new_func_name = info[-2]
            totalpct = float(info[1])
            selftime = float(info[2])
            childtime = float(info[3])
            if new_func_name == 'main':
                # assert(len(info) == 6)
                selfcalled = 1
            else:
                assert(len(info) == 7)
                if ('+' in info[4]):
                    # recursive calls
                    selfcalled = int(info[4].split('+')[0])
                else:
                    selfcalled = int(info[4])

            new_func = Node(selfcalled, selftime, childtime, totalpct, new_func_name)
            index_to_func[new_index] = new_func
            if new_func_name not in func_to_index:
                func_to_index[new_func_name] = new_index
            
            ''' Read the whole entry '''
            while(1):
                i += 1
                # end of this entry
                if raw_txt[i][0] == '-':
                    break
                
                child_info = raw_txt[i]
                # child infomation
                if '<cycle' in raw_txt[i]:
                    # neglect calling from another component in cycle
                    if '_<cycle' in new_func_name:
                        continue
                    # calling from other functions
                    else:
                        _child_func_name, _cycle_index = re.search('(\w+) <cycle (\w+)>', child_info).group(1,2)
                        child_info = re.sub('\w+ <cycle \w+>', '{}_<cycle_{}>'.format(_child_func_name, _cycle_index), child_info)

                child_info = re.sub('\s+', ',', child_info).split(',')[1:-1]

                # call itself recursively
                if child_info[-2] == new_func_name:
                    assert(len(child_info) == 3)
                    total_edge.append(Edge(new_func_name, new_func_name, int(child_info[0]), selftime, selftime))
                    continue

                # call other function
                assert(len(child_info) == 5)
                child_index = int(child_info[-1][1:-1])
                child_func_name = child_info[-2]
                if child_func_name not in func_to_index:
                    func_to_index[child_func_name] = child_index

                child_time = float(child_info[0])
                grandchild_time = float(child_info[1])
                # normal function with a /
                if '/' in child_info[2]:
                    child_called = int(child_info[2].split('/')[0])
                # cycle components do not have
                else:
                    child_called = int(child_info[2])
                total_edge.append(Edge(new_func_name, child_func_name, child_called, child_time, grandchild_time))

        elif (re.sub('\s+', '', raw_txt[i]) == ''):
            # end of all entries
            break
        else:
            # not new entry and child information
            # already save this edge from previous call
            i += 1
            continue
    
    return total_edge, index_to_func, func_to_index

# color mapping level 1->5 (cost little -> cost much)
map_color = {
    1: '#ee9779',
    2: '#ea7254',
    3: '#dc4a38',
    4: '#bb2f29',
    5: '#8c1a18'
}

def generate_js_input(total_edge, index_to_func, outfile_edge, outfile_node):
    json_node = []
    json_edge = []
    for edge in total_edge:
        new_edge = {}
        new_edge['from'] = edge.parent
        new_edge['to'] = edge.child
        new_edge['called'] = 'called {} times'.format(edge.child_called)
        # new_edge['ctime'] = edge.child_time
        # new_edge['gctime'] = edge.grandchild_time
        
        total_child_time = index_to_func[func_to_index[edge.parent]].child_time
        if (total_child_time == 0):
            new_edge['ewidthpct'] = 1
        else:
            new_edge['ewidthpct'] = (edge.child_time + edge.grandchild_time)/total_child_time
        new_edge['ewidth'] = new_edge['ewidthpct'] * baseWidth
        json_edge.append(new_edge)

    for node_idx in index_to_func:
        new_node = {}
        node = index_to_func[node_idx]
        new_node['key'] = node.name
        # new_node['selfcall'] = node.self_call
        # new_node['selftime'] = node.self_time
        # new_node['childtime'] = node.child_time
        # new_node['totalpct'] = node.total_pct
        if node.total_pct == 0:
            new_node['color'] = 1
        else:
            # scale to 0.5 - 1
            colorpct = (node.total_pct * node.self_time / (node.self_time + node.child_time) / 100)
            if colorpct < 0.2:
                new_node['color'] = 1
            elif colorpct < 0.4:
                new_node['color'] = 2
            elif colorpct < 0.6:
                new_node['color'] = 3
            elif colorpct < 0.8:
                new_node['color'] = 4
            else:
                new_node['color'] = 5
        new_node['color'] = map_color[new_node['color']]
        new_node['info'] = '{}\\ncalls:{}\\ntime:{:.2f}'.format(node.name, node.self_call, node.self_time)
        json_node.append(new_node)
    
    with open(outfile_edge, 'w') as f:
        json_edge = json.dumps(json_edge)
        f.write(json_edge)

    with open(outfile_node, 'w') as f:
        json_node = json.dumps(json_node)
        f.write(json_node)
    
    return json_node, json_edge

def generate_html(sample_html, demo_html, nodes, edges):
    # generate html by filling 
    # "myDiagram.model = new go.GraphLinksModel()" 
    # in the sample_html
    
    with open(sample_html, 'r') as f:
        sample = f.readlines()
    
    sample = ''.join(sample)
    model_empty = "myDiagram\.model = new go\.GraphLinksModel\(\)"
    model_fill = "myDiagram.model = new go.GraphLinksModel({}, {})".format(nodes, edges)
    instance = re.sub(model_empty, model_fill, sample)

    with open(demo_html, 'w') as f:
        f.write(instance)

# Modify the arguments to call
call_graph_path = 'data/graph_file'
outfile_edge = 'data/graph_edge.json'
outfile_node = 'data/graph_node.json'
sample_html = 'pageFlowSample.html'
run_html = 'demo.html'

total_edge, index_to_func, func_to_index = extract(call_graph_path)
nodes, edges = generate_js_input(total_edge, index_to_func, outfile_edge, outfile_node)
generate_html(sample_html, run_html, nodes, edges)