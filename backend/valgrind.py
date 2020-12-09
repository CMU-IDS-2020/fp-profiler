import re
import numpy as np
def extrace_valgrind_result(mode, f_res):
    try:
        if mode == "memory_leak":
            with open(f_res) as f:
                current_block = {"lines" : [], "error" : False, "bytes_num": 0}
                mem_leak_dic = {}
                for line in f.readlines():
                    datas = line.split("==")
                    if len(datas) < 3 or (len(datas) == 3 and datas[2] == " \n"):
                        if current_block["error"] == False:
                            current_block["lines"] = []
                        else:
                            error_line = current_block["lines"][-1]
                            line_num = int(re.search(r':\d*\)', error_line).group()[1:-1])
                            if current_block["error"]:
                                if line_num in mem_leak_dic:
                                    mem_leak_dic[line_num] += current_block["bytes_num"]
                                else:
                                    mem_leak_dic[line_num] = current_block["bytes_num"]
                            current_block["error"] = False
                            current_block["lines"] = []
                            current_block["bytes_num"] = 0
     
                    elif "loss record" in datas[2]:
                        current_block["error"] = True
                        current_block["bytes_num"] = int(re.search(r"^(\d+(?:,\d+)*)bytes", re.sub(r' ', '', datas[2])).group()[0:-5].replace(',', ''))
                    else:
                        current_block["lines"].append(line)
            return mem_leak_dic
        
        else:
            with open(f_res) as f:
                current_block = {"lines" : [], "error_type" : ""}
                uninitialised_buffer = []
                invalid_write_buffer = []
                for line in f.readlines():
                    datas = line.split("==")
                    if len(datas) < 3 or (len(datas) == 3 and datas[2] == " \n"):
                        if current_block["error_type"] == "":
                            current_block["lines"] = []
                        else:
                            error_line = current_block["lines"][-1]
                            line_num = int(re.search(r':\d*\)', error_line).group()[1:-1])
                            if current_block["error_type"] == "uninitialised":
                                uninitialised_buffer.append(line_num)
                            elif current_block["error_type"] == "invalid_write":
                                invalid_write_buffer.append(line_num)
                            current_block["error_type"] = ""
                            current_block["lines"] = []
     
                    elif "uninitialised" in datas[2]:
                        current_block["error_type"] = "uninitialised"
                        current_block["lines"].append(line)
                    elif "write" in datas[2]:
                        current_block["error_type"] = "invalid_write"
                        current_block["lines"].append(line)
                    else:
                        current_block["lines"].append(line)
                return (np.unique(uninitialised_buffer), np.unique(invalid_write_buffer))
    except:
        if mode == "memory_leak":
            return None
        else:
            return (None, None)
