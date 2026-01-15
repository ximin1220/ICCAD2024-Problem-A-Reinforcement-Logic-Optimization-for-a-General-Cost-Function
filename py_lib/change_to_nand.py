import subprocess
import os

def change_to_nand(best_gate_dic, v_path, base, library_file):
    new_dic = best_gate_dic
    best_nand = best_gate_dic['nand'][0]
    base_command = f'./{base}'
    #not
    with open(f'{v_path}/nand_not.v', 'w') as f:
        verilog_content = f"""module top_1598227639_809568180_776209382_1234615 (a, o);
 input a;
 output o;
 {best_nand} (a, a, o);
 endmodule
        """
        f.write(verilog_content)


    try:    
            command = [base_command, "-library", library_file, "-netlist", f'{v_path}/nand_not.v', "-output", 'owo.out']
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            # 检查输出文件是否存在
            if os.path.exists('owo.out'):
                # 解析输出文件中的cost值
                with open('owo.out', 'r') as f:
                    output_data = f.read().strip()
                    if output_data.startswith("cost = "):
                        cost_value = float(output_data.split("=")[1].strip())
                        if cost_value < best_gate_dic['not'][1]:
                             new_dic['not'] = ('change_nand_not', cost_value)
            else:
                print(f"Output file '{'owo.out'}' not found.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing command for {f'{v_path}/nand_not.v'}: {e}")
    
    return new_dic