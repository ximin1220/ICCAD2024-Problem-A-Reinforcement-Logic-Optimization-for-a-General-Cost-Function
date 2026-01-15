import re

def refresh_gate(input_file, output_file, best_gate_dic):
    best_nand = best_gate_dic['nand'][0]
    best_nor = best_gate_dic['nor'][0]
    best_and = best_gate_dic['and'][0]
    with open(input_file, 'r') as file:
        lines = file.readlines()
    
    with open(output_file, 'w') as file:
        for line in lines:
            # Check if the line starts with 'change_nand_not'
            if line.strip().startswith('change_nand_not'):
                # Replace 'change_nand_not' with 'nand_5' and adjust the arguments
                modified_line = re.sub(r'change_nand_not\s+(\w+)\(\.A\((\w+)\),\s*\.Y\((\w+)\)\);', 
                                       rf'{best_nand}          \1(.A(\2), .B(\2), .Y(\3));', 
                                       line)
                file.write(modified_line)
            # Check if the line starts with 'change_nor_not'
            elif line.strip().startswith('change_nor_not'):
                # Replace 'change_nor_not' with 'nor_5' and adjust the arguments
                modified_line = re.sub(r'change_nor_not\s+(\w+)\(\.A\((\w+)\),\s*\.Y\((\w+)\)\);', 
                                       rf'{best_nor}           \1(.A(\2), .B(\2), .Y(\3));', 
                                       line)
                file.write(modified_line)
            elif line.strip().startswith('change_and_buf'):
                # Replace 'change_nor_not' with 'nor_5' and adjust the arguments
                modified_line = re.sub(r'change_and_buf\s+(\w+)\(\.A\((\w+)\),\s*\.Y\((\w+)\)\);', 
                                       rf'{best_and}           \1(.A(\2), .B(1), .Y(\3));', 
                                       line)
                file.write(modified_line)
            else:
                # Write the line as it is
                file.write(line)

# Example usage
# modify_verilog_file('test_new_gen.v', f'new_test_new_gen.v')

