import json


def get_gate(lib_file):
    with open(lib_file, 'r') as file:
        data = json.load(file)

    and_names = []
    nor_names = []
    not_names = []
    nand_names = []
    buf_names = []
    xor_names = []
    xnor_names = []
    or_names = []

    # (and, not, nor, nand, buf, xor, xnor, or)
    for cell in data['cells']:
        if cell['cell_type'] in ['and']:
            and_names.append(cell['cell_name'])
        if cell['cell_type'] in ['nor']:
            nor_names.append(cell['cell_name'])
        if cell['cell_type'] in ['not']:
            not_names.append(cell['cell_name'])
        if cell['cell_type'] in ['nand']:
            nand_names.append(cell['cell_name'])
        if cell['cell_type'] in ['buf']:
            buf_names.append(cell['cell_name'])
        if cell['cell_type'] in ['xor']:
            xor_names.append(cell['cell_name'])
        if cell['cell_type'] in ['xnor']:
            xnor_names.append(cell['cell_name'])
        if cell['cell_type'] in ['or']:
            or_names.append(cell['cell_name'])
    
    return and_names, not_names, nor_names, nand_names, buf_names, xor_names, xnor_names, or_names


