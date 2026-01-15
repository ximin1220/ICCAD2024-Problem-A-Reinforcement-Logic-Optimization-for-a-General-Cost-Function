import re
import random
import string

# Generate a random string for buffer instance names
def generate_string():
    characters = string.ascii_letters + string.digits
    random_chars = ''.join(random.choices(characters, k=10))
    return 'g' + random_chars

# Regex pattern to find signal connections
pattern = re.compile(r'(\.A|\.B)\((\w+)\)')

# Function to replace inputs with buffer signals if applicable
def replace_input_with_check(match, buf_wires):
    port = match.group(1)
    signal = match.group(2)
    if f'{signal}_b' in buf_wires:
        return f'{port}({signal}_b)'
    else:
        return f'{port}({signal})'

# Parse Verilog file to extract outputs and wires
def parse_verilog(file_path):
    outputs = []
    wires = []
    
    with open(file_path, 'r') as file:
        content = file.read()

        # Extract outputs
        output_match = re.search(r'output\s+([\w,\s]+);', content)
        if output_match:
            outputs = [signal.strip() for signal in output_match.group(1).split(',')]

        # Extract wires
        wire_match = re.search(r'wire\s+([\w,\s]+);', content)
        if wire_match:
            wires = [signal.strip() for signal in wire_match.group(1).split(',')]

    return outputs, wires

# Function to process Verilog code and add buffers
def add_buffers_to_gates(verilog_code, gates, outputs, buf_name):
    buf_wires = []
    processed_lines = []
    
    for line in verilog_code:
        modified_line = pattern.sub(lambda match: replace_input_with_check(match, buf_wires), line)
        processed_lines.append(modified_line)

        # Check if the line contains any of the gates we are interested in
        if any(gate in line for gate in gates) and 'buf' not in line:
            output_signal = line.split('.Y(')[1].split(')')[0]
            buffer_signal = output_signal + '_b'
            if output_signal not in outputs:
                buf_wires.append(buffer_signal)
                # Add the wire declaration and buffer instance
                processed_lines.append(f"  wire {buffer_signal};\n")
                processed_lines.append(f"  {buf_name}           {generate_string()}(.A({output_signal}), .Y({buffer_signal}));\n")

    return processed_lines

# Main function to process the Verilog file and write the output
def adding_buf(file_path, output_file_path, buf_name):
    # Gates we are interested in
    gates = ['and', 'nor', 'not', 'or', 'nand', 'xor', 'xnor']

    # Parse the input Verilog file
    outputs, wires = parse_verilog(file_path)

    # Read the contents of the input Verilog file
    with open(file_path, 'r') as file:
        verilog_code = file.readlines()

    # Process the Verilog code to add buffers
    processed_verilog_code = add_buffers_to_gates(verilog_code, gates, outputs, buf_name)

    # Write the processed Verilog code to the output file
    with open(output_file_path, 'w') as file:
        file.writelines(processed_verilog_code)

    return output_file_path

# _add_buf('design_optimized.v', 'add_buf_test.v', buf_name)