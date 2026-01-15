# Adjusting the function logic to ensure the new lines are inserted after the wire section and before the gate section
import re
import random
import string

# Generate a random string for buffer instance names
def generate_string():
    characters = string.ascii_letters + string.digits
    random_chars = ''.join(random.choices(characters, k=10))
    return 'g' + random_chars

def paradox_f(input_file, output_file, best_xnor, best_and):
    # Initialize variables
    input_wire_prefix = "input"
    wire_prefix = "wire"
    collecting_inputs = False
    input_wires = []
    inside_wire_declaration = False

    # Read the original Verilog file content
    with open(input_file, 'r') as file:
        verilog_code = file.readlines()

    # Collect all the input wires from multiple lines if necessary
    for line in verilog_code:
        if input_wire_prefix in line:
            collecting_inputs = True  # Start collecting input wires
            line = line.replace("input", "").replace(";", "").strip()
            input_wires.extend([wire.strip() for wire in line.split(",") if wire.strip()])
        elif collecting_inputs:
            if ";" in line:  # If the input section ends, stop collecting
                line = line.replace(";", "").strip()
                input_wires.extend([wire.strip() for wire in line.split(",") if wire.strip()])
                collecting_inputs = False
            else:
                input_wires.extend([wire.strip() for wire in line.split(",") if wire.strip()])

    # Now, create new wires with "_p" suffix for each input wire
    new_wire_declarations = ", ".join([f"{wire}_p" for wire in input_wires]) + ";"
    new_wire_declarations = "wire " + new_wire_declarations + "\n"

    # Build the lines that need to be inserted
    insertion_lines = f"""
    wire paradox_output, p1, p2, p3, p4, p5, p6;
    {best_xnor} {generate_string()}(.A({input_wires[0]}), .B({input_wires[0]}), .Y(p1));
    {best_and} {generate_string()}(.A(p1), .B(p1), .Y(p2));
    {best_and} {generate_string()}(.A(p2), .B(p2), .Y(p3));
    {best_and} {generate_string()}(.A(p3), .B(p3), .Y(p4));
    {best_and} {generate_string()}(.A(p4), .B(p4), .Y(p5));
    {best_and} {generate_string()}(.A(p5), .B(p5), .Y(p6));
    {best_and} {generate_string()}(.A(p6), .B(p6), .Y(paradox_output));

    {new_wire_declarations}
    """
    for pi in input_wires:
        new_line = f'{best_and} {generate_string()}(.A({pi}), .B(paradox_output), .Y({pi}_p));\n'
        insertion_lines += new_line

    # Prepare the output lines, modifying gates to replace primary input wires with their "_p" version
    output_lines = []
    inside_module = False
    wire_section_completed = False
    for line in verilog_code:
        modified_line = line
        if "module" in line:
            inside_module = True
        if inside_module and "input" in line:
            output_lines.append(line)  # Do not modify input declaration lines
            continue
        # After collecting the input wires, look for the wire section
        if inside_module and "wire" in line:
            output_lines.append(line)
            inside_wire_declaration = True
            continue
        if inside_wire_declaration and ";" in line:  # End of wire declaration section
            inside_wire_declaration = False
            output_lines.append(line)
            output_lines.append(insertion_lines)  # Insert the required lines after wire declarations
            continue
        for wire in input_wires:
            # Replace primary inputs in gates with their "_p" counterpart
            modified_line = modified_line.replace(f".A({wire})", f".A({wire}_p)")
            modified_line = modified_line.replace(f".B({wire})", f".B({wire}_p)")
            modified_line = modified_line.replace(f".C({wire})", f".C({wire}_p)")
            modified_line = modified_line.replace(f".D({wire})", f".D({wire}_p)")
        output_lines.append(modified_line)

    # Write the modified Verilog code to the output file
    with open(output_file, 'w') as file:
        file.writelines(output_lines)

# Apply the function to the newly uploaded file
#paradox_f('pp.v', 'test_paradox.v')


