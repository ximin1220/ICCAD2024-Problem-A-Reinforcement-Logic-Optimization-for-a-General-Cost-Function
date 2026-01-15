import subprocess
import os

def find_min_cost_module_1input(base, library_file, output_file, module_names, genlib_file, gate):
    # 模块名列表
    base_command = f'./{base}'
    output_option = "-output"
    # 最大的cost值和对应的模块名
    min_cost = float('inf')
    best_module_name = ""

    for module_name in module_names:
        # 构建.verilog文件的内容
        verilog_content = f"""module top_1598227639_809568180_776209382_1234615 (a, o);
 input a;
 output o;
 {module_name} g1(a, o);
 endmodule
        """
    #     verilog_content = f"""module top_1598227639_809568180_776209382_1234615 (a, o);
    #  input a;
    #  output o;
    #  wire a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, o1, o2, o3, o4, o5, o6, o7, o8, o9, o10;
    #  {module_name} (a1, o1);
    #  {module_name} (a2, o2);
    #  {module_name} (a3, o3);
    #  {module_name} (a4, o4);
    #  {module_name} (a5, o5);
    #  {module_name} (a6, o6);
    #  {module_name} (a7, o7);
    #  {module_name} (a8, o8);
    #  {module_name} (a9, o9);
    #  {module_name} (a10, o10);
    #  endmodule
    #         """
        # 将内容写入文件
        verilog_filename = f"gates/{module_name}.v"
        with open(verilog_filename, 'w') as f:
            f.write(verilog_content)
        
        # 构建完整的命令
        command = [base_command, "-library", library_file, "-netlist", verilog_filename, "-output", output_file]
        # print(command)

        # 执行命令并捕获输出
        try:
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            # 检查输出文件是否存在
            if os.path.exists(output_file):
                # 解析输出文件中的cost值
                with open(output_file, 'r') as f:
                    output_data = f.read().strip()
                    if output_data.startswith("cost = "):
                        cost_value = float(output_data.split("=")[1].strip())
                        # 比较并更新最大的cost值和对应的模块名
                        if cost_value < min_cost:
                            min_cost = cost_value
                            best_module_name = module_name
                with open(genlib_file, 'a') as f:
                    if gate == 'buf':
                        # content = ''
                        content = f"GATE {module_name}    {cost_value}  Y=A;                         PIN * NONINV 1 999 1 0 1 0\n"
                    elif gate == 'not':
                        content = f"GATE {module_name}    {cost_value}  Y=!A;                        PIN * NONINV 1 999 1 0 1 0\n"
                    f.write(content)

            else:
                print(f"Output file '{output_file}' not found.")
        except subprocess.CalledProcessError as e:
            print(f"Error executing command for {verilog_filename}: {e}")

    # 返回最大cost值对应的模块名
    return best_module_name, min_cost

