#!/usr/bin/env python3
#./cada0009_beta -cost_function cost_estimator_1 -library lib1.json -netlist design1.v -output design_optimized.v
#./test2/cost_estimator_6 -library test2/lib1.json -netlist design_optimized.v -output cf3_ex2.out
import argparse
import subprocess
import random
import sys
import shutil
import math
import os
import stat
from py_lib.mapping_not import mapping_not
from py_lib.mapping_nand import *
from py_lib.remove_gate import remove_gate_names
from py_lib.get_gate import *
from py_lib.find_and import *
from py_lib.find_not import *
from py_lib.find_nand import *
from py_lib.find_2input import *
from py_lib.find_1input import find_min_cost_module_1input
from py_lib.change_to_nand import *
from py_lib.change_to_and import *
from py_lib.change_to_nor import *
from py_lib.write_genlib import *
from py_lib.refresh_gate import *
from py_lib.add_buf_func import adding_buf
from py_lib.compute_cost import *
from py_lib.test_cec import *
from py_lib.paradox import *

os.chmod('abc2', stat.S_IEXEC)

parser = argparse.ArgumentParser(description="解析命令列參數")
# parser.add_argument('script', type=str, help='Script name')
parser.add_argument('-cost_function', type=str, required=True, help='Cost function')
parser.add_argument('-library', type=str, required=True, help='Library file')
parser.add_argument('-netlist', type=str, required=True, help='Netlist file')
parser.add_argument('-output', type=str, required=True, help='Output file')

args = parser.parse_args()

def simulated_annealing(map_form, best_cost, cost_func, lib_file, rm_gate_input, abc_exe_path, initial_temp, cooling_rate, iterations, genlib_file, final_file, new_genlib):


    # best_gates = random_mapping(lib_file, es_gates, cost_func, init_file)
    after_abc_readable = 'after_abc.v'
    to_refresh = 'to_refresh.v'
    after_refresh = 'after_refresh.v'
    in_iteration = 'in_iteration.v'
    shutil.copy(rm_gate_input, in_iteration)

    # actions = ['rewrite', 'rewrite -z', 'balance', 'refactor', 'refactor -z', 'resub', 'resub -z', 'if -g']
    actions = ['strash;satclp -C 200;strash;dch', 'rewrite', 'refactor -z', 'resub', 'resub -z', 'if -g', 'dfraig', 'drf', 'drw', 'drwsat', 'icut', 'ifraig', 'iresyn', 'irw', 'irws', 'isat', 'istrash', 'if -x', 'csweep', 'dc2']
    #actions = ['strash;satclp;strash;dch', 'so', 'sif', 'r3b', 'r3', 'r3f', 'rewrite', 'refactor -z', 'resub', 'resub -z', 'if -g', 'dfraig', 'drf', 'drw', 'drwsat', 'icut', 'ifraig', 'iresyn', 'irw', 'irws', 'isat', 'istrash', 'if -x', 'csweep', 'dc2']
    
    ending = [
        f'write_verilog {after_abc_readable}',
        'strash',
        map_form,
        f'write_verilog {to_refresh}',
        'quit'
    ]

    current_cost = float('inf')
    # best_cost = float('inf')
    temp = initial_temp
    min_temp = 1e-3

    for i in range(iterations):
        commands = [
            f'read {in_iteration}',
            f'read_library {new_genlib}',
            'strash',
            'print_fanio'
        ]
        for j in range(10):
            selected_action = random.choice(actions)
            while selected_action == 'strash;satclp -C 200;strash;dch':
                if i <= 4:
                    selected_action = random.choice(actions)
                else:
                    actions.pop(0)
                    break
            commands.append(selected_action)
        commands = commands + ending
        abc_command = ';'.join(commands)
        
        try:
            process = subprocess.Popen([abc_exe_path, '-c', abc_command], 
                                        stdout=subprocess.PIPE, 
                                        stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()

            if process.returncode == 0:
                print(f'{i+1} : {selected_action}')
                print("Stdout:")
                print(stdout.decode('utf-8'))  
            else:
                print(f"An error occurred while executing ABC commands: {stderr.decode('utf-8')}")
                print("Stderr:")
                print(stderr.decode('utf-8'))
                continue
        except Exception as e:
            print(f"error: {e}")
            continue

        refresh_gate(to_refresh, after_refresh, best_gate_dic)
        # mapping_not(to_map, output_file, best_gates)
        # mapped = 'after_abc.v'

        result = subprocess.run([f'./{cost_func}', '-library', lib_file, '-netlist', after_refresh, '-output', 'owo.out'],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

        with open('owo.out', 'r') as f:
            output_data = f.read().strip()
            if output_data.startswith("cost = "):
                new_cost = float(output_data.split("=")[1].strip())
                print(new_cost)
                
                if new_cost < current_cost or random.uniform(0, 1) < math.exp((current_cost - new_cost) / temp):
                    current_cost = new_cost
                    shutil.copy(after_abc_readable, in_iteration)
                    # shutil.copy(after_refresh, final_file)
                else:
                    shutil.copy(in_iteration, after_abc_readable)
                    # shutil.copy(final_file, after_refresh)
                if new_cost < best_cost:
                    best_cost = new_cost
                        # shutil.copy('after_abc.v', 'best.v')
                    shutil.copy(after_refresh, final_file)
        
        temp = max(temp * cooling_rate, min_temp)

    # shutil.copy('best.v', sys.argv[8])
    print(f'Best cost: {best_cost}')
    return best_cost



if __name__ == "__main__":
    if len(sys.argv) != 9:
        print("Usage: python3.6 test.py cost_function cost_function_1 -library low_vt.lib -netlist design.v -output design_optimized.v")
        sys.exit(1)

    # cost_func = sys.argv[2]
    # lib_file = sys.argv[4]
    # input_v = sys.argv[6]
    # optimized_v = sys.argv[8]
    cost_func = args.cost_function
    lib_file = args.library
    input_v = args.netlist
    optimized_v = args.output
    original_rm_gate = 'original_rm_gate.v'
    rm_gate_input = 'rm_gate.v'
    abc_exe_path = './abc2'
    genlib_file = 'testgen.genlib'
    os.chmod(cost_func, stat.S_IEXEC)
    remove_gate_names(input_v, original_rm_gate)
    remove_gate_names(input_v, rm_gate_input)

    with open(genlib_file, 'w') as f:
        pass

    all_gates = ('and', 'not', 'nor', 'nand', 'buf', 'xor', 'xnor', 'or')
    try:
        best_gate_dic = {}
        gate_names = get_gate(lib_file) # (and, not, nor, nand, buf, xor, xnor, or)
        # print(gate_names)
        best_gate_dic['and'] = find_min_cost_module_2input(cost_func, lib_file, 'owo.out', gate_names[0], genlib_file, 'and')
        best_gate_dic['not'] = find_min_cost_module_1input(cost_func, lib_file, 'owo.out', gate_names[1], genlib_file, 'not')
        best_gate_dic['nor'] = find_min_cost_module_2input(cost_func, lib_file, 'owo.out', gate_names[2], genlib_file, 'nor')
        best_gate_dic['nand'] = find_min_cost_module_2input(cost_func, lib_file, 'owo.out', gate_names[3], genlib_file, 'nand')
        best_gate_dic['buf'] = find_min_cost_module_1input(cost_func, lib_file, 'owo.out', gate_names[4], genlib_file, 'buf')
        best_gate_dic['xor'] = find_min_cost_module_2input(cost_func, lib_file, 'owo.out', gate_names[5], genlib_file, 'xor')
        best_gate_dic['xnor'] = find_min_cost_module_2input(cost_func, lib_file, 'owo.out', gate_names[6], genlib_file, 'xnor')
        best_gate_dic['or'] = find_min_cost_module_2input(cost_func, lib_file, 'owo.out', gate_names[7], genlib_file, 'or')
        # es_gates = [best_and, best_not, best_nor, best_buf]
        # print('bgd\n', best_gate_dic)
        new_dic = change_to_nand(best_gate_dic, 'gates', cost_func, lib_file)
        new_dic = change_to_nor(best_gate_dic, 'gates', cost_func, lib_file)
        # new_dic = change_to_and(best_gate_dic, 'gates', cost_func, lib_file)
        # print('nd', new_dic)
        new_genlib = 'new_genlib.genlib'
        # print('bgd\n', best_gate_dic)
        
        write_genlib(new_dic, new_genlib)
    except:
        new_dic = {}
        for g in all_gates:
            new_dic[g] = (g, 1)
        new_genlib = 'new_genlib.genlib'
        write_genlib(new_dic, new_genlib)

    commands = [
        f'read {rm_gate_input}',
        'strash',
        'print_stats',
        'write_verilog init.v',
        'quit'
    ]
    abc_command = ';'.join(commands)
    try:
        process = subprocess.Popen([abc_exe_path, '-c', abc_command], 
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode == 0:
            print("Successfully")
            print("Stdout:")
            print(stdout.decode('utf-8'))  
        else:
            print(f"An error occurred while executing ABC commands: {stderr.decode('utf-8')}")
    except Exception as e:
        print(f"error: {e}")

    init_file = 'init.v'

    initial_temp = 200.0
    cooling_rate = 0.98
    iterations = 250
 
    now_best = float('inf')
    now_best = simulated_annealing('map ', now_best, cost_func, lib_file, rm_gate_input, abc_exe_path, initial_temp, cooling_rate, 5, genlib_file, optimized_v, new_genlib)
    testing_adding_buf_cost = now_best
    best_buf_file = 'best_add_buf.v'
    optimized_v_copy = 'optimized_v_copy.v'
    shutil.copy(optimized_v, optimized_v_copy)
    try:
        for buf_ in gate_names[4]:
            add_buf_file = 'add_buffer.v'
            adding_buf(optimized_v_copy, add_buf_file, buf_)
            add_buf_cost = compute_cost(add_buf_file, cost_func, lib_file)
            if add_buf_cost < testing_adding_buf_cost:
                shutil.copy(add_buf_file, best_buf_file)
                testing_adding_buf_cost = add_buf_cost
        if testing_adding_buf_cost < now_best and test_cec(rm_gate_input, best_buf_file):
            shutil.copy(best_buf_file, optimized_v)
            now_best = testing_adding_buf_cost
    except:
        print('add_buf error')

    now_best = simulated_annealing('map ', now_best, cost_func, lib_file, rm_gate_input, abc_exe_path, initial_temp, cooling_rate, 5, genlib_file, optimized_v, new_genlib)

    try:
        add_paradox_file = 'add_paradox.v'
        paradox_f(optimized_v_copy, add_paradox_file, new_dic['xnor'][0], new_dic['and'][0])
        add_paradox_cost = compute_cost(add_paradox_file, cost_func, lib_file)
        if add_paradox_cost < now_best and test_cec(rm_gate_input, add_paradox_file):
            shutil.copy(add_paradox_file, optimized_v)
            now_best = add_paradox_cost
    except:
        print('add_paradox error')
    

    for i in range(5):
        now_best = simulated_annealing('map -f', now_best, cost_func, lib_file, rm_gate_input, abc_exe_path, initial_temp, cooling_rate, 1, genlib_file, optimized_v, new_genlib)
        now_best = simulated_annealing('map -a', now_best, cost_func, lib_file, rm_gate_input, abc_exe_path, initial_temp, cooling_rate, 1, genlib_file, optimized_v, new_genlib)
        now_best = simulated_annealing('map ', now_best, cost_func, lib_file, rm_gate_input, abc_exe_path, initial_temp, cooling_rate, 1, genlib_file, optimized_v, new_genlib)
    for i in range(10):
        now_best = simulated_annealing('map -f', now_best, cost_func, lib_file, rm_gate_input, abc_exe_path, initial_temp, cooling_rate, iterations, genlib_file, optimized_v, new_genlib)
        now_best = simulated_annealing('map -a', now_best, cost_func, lib_file, rm_gate_input, abc_exe_path, initial_temp, cooling_rate, iterations, genlib_file, optimized_v, new_genlib)
        now_best = simulated_annealing('map ', now_best, cost_func, lib_file, rm_gate_input, abc_exe_path, initial_temp, cooling_rate, iterations, genlib_file, optimized_v, new_genlib)

#'csweep', 'dc2', 'dch', 'dchoice'
#'dfraig', 'drf', 'drw', 'drwsat', 'icut', 'ifraig', 'iresyn', 'irw', 'irws', 'isat', 'istrash', 'qbf'