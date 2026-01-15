import os
import re
import subprocess

# Function to rearrange gate lines by placing the output first
def rearrange_gate_line(line):
    # Use regex to capture the gate type, gate name, and the signals in the format of .A(x), .B(y), .Y(z)
    match_two_input = re.match(r'(\s*\w+\s+\w+)\s*\((\.A\((\w+)\),)?\s*(\.B\((\w+)\),)?\s*\.Y\((\w+)\)\);', line)
    match_single_input = re.match(r'(\s*\w+\s+\w+)\s*\((\.A\((\w+)\),)?\s*\.Y\((\w+)\)\);', line)
    
    if match_two_input:
        gate_type_name = match_two_input.group(1)  # e.g., 'nand_5 g00'
        A_signal = match_two_input.group(3) or ''  # Extract A signal (if it exists)
        B_signal = match_two_input.group(5) or ''  # Extract B signal (if it exists)
        Y_signal = match_two_input.group(6)        # Extract Y signal (output)
        
        # Rebuild the line with the primary output (Y_signal) first, followed by A_signal and B_signal
        reordered_signals = [Y_signal, A_signal, B_signal]
        reordered_signals = ', '.join([signal for signal in reordered_signals if signal])  # Join non-empty signals

        return f'{gate_type_name}({reordered_signals});\n'
    
    elif match_single_input:
        gate_type_name = match_single_input.group(1)  # e.g., 'buf_1 g00'
        A_signal = match_single_input.group(3)        # Extract A signal (input)
        Y_signal = match_single_input.group(4)        # Extract Y signal (output)

        # Rebuild the line with the primary output (Y_signal) first, followed by A_signal
        reordered_signals = f'{Y_signal}, {A_signal}'
        return f'{gate_type_name}({reordered_signals});\n'
    
    return line

# Function to remove the number suffix from gate names
def remove_number_suffix(line):
    # Use regex to match the gate type and remove any trailing underscore followed by numbers
    line = re.sub(r'(\s*\w+)_\d+', r'\1', line)
    return line

# Function to remove the gate instance name (e.g., g00)
def remove_gate_instance_name(line):
    # Use regex to match and remove the gate instance name between the gate type and the signal list
    line = re.sub(r'(\s*\w+)\s+\w+\(', r'\1(', line)
    return line

# Main function to process the verilog file
def process_verilog_file(input_file, output_file):
    with open(input_file, 'r') as file:
        verilog_code = file.readlines()

    # Step 1: Rearrange the gate lines
    modified_verilog_code = [rearrange_gate_line(line) if '(' in line and ');' in line else line for line in verilog_code]

    # Step 2: Remove number suffixes from gate names
    modified_verilog_code = [remove_number_suffix(line) for line in modified_verilog_code]

    # Step 3: Remove gate instance names
    final_verilog_code = [remove_gate_instance_name(line) for line in modified_verilog_code]

    # Save the final modified file
    with open(output_file, 'w') as final_file:
        final_file.writelines(final_verilog_code)

# Example usage:
#process_verilog_file('test_paradox.v', 'output_d1.v')

def test_cec(original_file, to_parse_file):
    is_eq = False
    process_verilog_file(to_parse_file, 'can_cec.v')
    commands = [
            f'cec {original_file} can_cec.v'
        ]
    abc_command = ';'.join(commands)
    try:
        process = subprocess.Popen(['./abc2', '-c', abc_command], 
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode == 0:
            print("Successfully")
            print("Stdout:")
            print((stdout.decode('utf-8')).split(' '))
            mes =  (stdout.decode('utf-8')).split(' ') 
            if 'equivalent.' in mes:
                is_eq = True
        else:
            print(f"An error occurred while executing ABC commands: {stderr.decode('utf-8')}")
    except Exception as e:
        print(f"error: {e}")
    return is_eq

# print(test_cec('rm_gate.v', 'test_paradox.v'))