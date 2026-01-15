import re
# get names [and, nand, nor]
def mapping_nand(input_file, output_file, gate_names):
    s = set()
    with open(input_file, 'r') as file:
        lines = file.readlines()
    
    with open(output_file, 'w', newline = '\n') as file:
        for line in lines:
            # 使用正則表達式匹配 gate name 並將其去掉
            if not line.split() or line.split()[0] != 'assign':
                file.write(line)
            else: 
                line_split = line.split()
                if len(line_split) == 4:
                    if line_split[3][0] == '~':
                        file.write(f'{gate_names[1]} ({line_split[3][1:-1]}, {line_split[3][1:-1]}, {line_split[1]});'+'\n')
                    else:
                        file.write(f'{gate_names[3]} ({line_split[3][:-1]}, {line_split[1]});'+'\n') 
                else:
                    i1 = line_split[3]
                    i2 = line_split[5]
                    new_i1 = i1
                    new_i2 = i2[:-1]
                    if i1[0] == '~' and i2[0] == '~':
                        file.write(f'{gate_names[2]} ({new_i1[1:]}, {new_i2[1:]}, {line_split[1]});'+'\n')
                    else:
                        if i1[0] == '~':
                            nw = i1[1:] + '_n'
                            if not nw in s:
                                s.add(nw)
                                file.write(f'{gate_names[1]} ({i1[1:]}, {i1[1:]}, {nw});'+'\n')
    #                         file.write(f'wire {nw};\n')
                            new_i1 = nw
                        if i2[0] == '~':
                            nw = i2[1:-1] + '_n'
    #                         file.write(f'wire {nw};\n')
                            if not nw in s:
                                s.add(nw)
                                file.write(f'{gate_names[1]} ({i2[1:-1]}, {i2[1:-1]}, {nw});'+'\n')
                            new_i2 = nw
                        file.write(f'{gate_names[0]} ({new_i1}, {new_i2}, {line_split[1]});'+'\n')
                    



