import re

def remove_gate_names(input_file, output_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    with open(output_file, 'w') as file:
        for line in lines:
            # 使用正則表達式匹配 gate name 並將其去掉
            modified_line = re.sub(r'(\bnot\b|\band\b|\bor\b|\bxor\b|\bxnor\b|\bnor\b|\bnand\b||\bbuf\b)\s+\w+\s*\(', r'\1 (', line)
            file.write(modified_line)

