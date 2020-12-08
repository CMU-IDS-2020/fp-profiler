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

class fullNodeInfo:
    def __init__(self, ID, name, selfTime, totalTime, parent, child, called):
        self.ID = ID
        self.name = name
        self.selfTime = selfTime
        self.totalTime = totalTime
        self.parent = parent # a list of edge index
        self.child = child
        self.called = called

class baseNodeArr:
    def __init__(self, ID, name, time, isExpanded, percent, hide, timePct):
        self.ID = ID
        self.name = name
        self.time = time
        self.isExpanded = True
        self.percent = 1
        self.hide = False
        self.timePct = timePct

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
        
class fullEdgeInfo:
    def __init__(self, _from, _to, called, time, cTime, gcTime):
        self._from = _from
        self.to = _to
        self.called = called
        self.time = time
        self.cTime = cTime
        self.gcTime = gcTime

class baseEdgeArr:
    def __init__(self, _from, _to, validcalled, validTime, validCTime, validGcTime):
        self._from = _from
        self.to = _to
        self.validcalled = validcalled
        self.validTime = validTime
        self.validCTime = validCTime
        self.validGcTime = validGcTime
        self.hide = False

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

def sort_node(total_edge, func_to_index, index_to_func):
    
    func_in_edge_num = {}
    func_out_edge = {}
    self_cycle_func = []
    for func in func_to_index:
        func_in_edge_num[func] = 0 # function name string
    
    for edge in total_edge:
        func_in_edge_num[edge.child] += 1
        if edge.parent in func_out_edge:
            func_out_edge[edge.parent].append(edge)
        else:
            func_out_edge[edge.parent] = [edge]
        if edge.child == edge.parent:
            self_cycle_func.append(edge.child)
    
    func_list = []
    func_to_sorted_index = {}
    cur_idx = 0

    while (1):
        if (cur_idx == len(func_to_index)):
            break
        
        for func in func_in_edge_num:
            if (func_in_edge_num[func] == 0) or (func_in_edge_num[func] == 1 and func in self_cycle_func):
                func_to_sorted_index[func] = cur_idx
                func_list.append(index_to_func[func_to_index[func]])
                
                if func in func_out_edge:
                    for edge in func_out_edge[func]:
                        func_in_edge_num[edge.child] -= 1
                
                cur_idx += 1
                func_in_edge_num[func] = -1
    
    full_edge_info_whole_list = []
    for func in func_list:
        full_edge_info_list = []
        if func.name in func_out_edge:
            for edge in func_out_edge[func.name]:
                full_edge = fullEdgeInfo(func_to_sorted_index[edge.parent], func_to_sorted_index[edge.child], edge.child_called, edge.child_time + edge.grandchild_time, edge.child_time, edge.grandchild_time)
                if full_edge._from == full_edge.to:
                    full_edge.time = 0
                    full_edge.cTime = 0
                    full_edge.gcTime = 0
                    
                full_edge_info_list.append(full_edge)
        sorted(full_edge_info_list, key=lambda ele:ele.to)
        full_edge_info_whole_list += full_edge_info_list

    parent_list = []
    for i in range(len(func_list)):
        parent_list.append([])
    child_list = []
    for i in range(len(func_list)):
        child_list.append([])

    for i in range(len(full_edge_info_whole_list)):
        _from = full_edge_info_whole_list[i]._from
        _to = full_edge_info_whole_list[i].to

        parent_list[_to].append(i)
        child_list[_from].append(i)
    
    node_list = []
    for i in range(len(func_list)):
        func = func_list[i]
        new_node = fullNodeInfo(i, func.name, func.self_time, func.self_time + func.child_time, parent_list[i], child_list[i], func.self_call)
        node_list.append(new_node)
    
    return node_list, full_edge_info_whole_list 


def generate_js_input(node_list, edge_list, output=''):
    whole_js = {}

    json_fullNodeInfo = []
    json_baseNodeArr = []
    json_fullEdgeInfo = []
    json_baseEdgeArr = []

    for i in range(len(node_list)):
        new_node = {}
        node = node_list[i]
        new_node["ID"] = i
        new_node["name"] = node.name
        new_node["selfTime"] = node.selfTime
        new_node["totalTime"] = node.totalTime
        new_node["parent"] = node.parent
        new_node["child"] = node.child
        new_node["called"] = node.called

        json_fullNodeInfo.append(new_node)

        new_base_node = {}
        new_base_node["key"] = i
        new_base_node["name"] = node.name
        new_base_node["time"] = node.selfTime
        new_base_node["isExpanded"] = True
        new_base_node["percent"] = 1
        new_base_node["hide"] = False
        new_base_node["timePct"] = node.selfTime / node_list[0].totalTime

        json_baseNodeArr.append(new_base_node)



    for i in range(len(edge_list)):
        new_edge = {}
        edge = edge_list[i]
        new_edge['from'] = edge._from
        new_edge['to'] = edge.to
        new_edge['called'] = edge.called
        new_edge['time'] = edge.time
        new_edge['cTime'] = edge.cTime
        new_edge['gcTime'] = edge.gcTime

        json_fullEdgeInfo.append(new_edge)

        new_base_edge = {}
        new_base_edge['from'] = edge._from
        new_base_edge['to'] = edge.to
        new_base_edge['validcalled'] = edge.called
        new_base_edge['validTime'] = edge.time
        new_base_edge['validCTime'] = edge.cTime
        new_base_edge['validGcTime'] = edge.gcTime
        new_base_edge['hide'] = False

        json_baseEdgeArr.append(new_base_edge)       
    
    whole_js["fullNodeInfo"] = json_fullNodeInfo
    whole_js["fullEdgeInfo"] = json_fullEdgeInfo
    whole_js["baseNodeArr"] = json_baseNodeArr
    whole_js["baseEdgeArr"] = json_baseEdgeArr

    if output != '':
        with open(output, 'w') as f:
            f.write(json.dumps(whole_js))

    return whole_js    

if __name__ == '__main__':    
    call_graph_path = '../data/call_graph.out'
    outfile_edge = '../data/graph_edge.json'
    outfile_node = '../data/graph_node.json'
    output = '../data/demo-4.json'


    total_edge, index_to_func, func_to_index = extract(call_graph_path)
    node_list, edge_list = sort_node(total_edge, func_to_index, index_to_func)
    generate_js_input(node_list, edge_list, output)
