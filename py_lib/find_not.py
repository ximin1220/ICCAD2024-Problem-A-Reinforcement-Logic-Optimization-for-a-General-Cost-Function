import subprocess
import os

def find_min_cost_module_not(base, library_file, output_file, module_names):
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
 {module_name} (a, o);
 endmodule
        """
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
            else:
                print(f"Output file '{output_file}' not found.")
        except subprocess.CalledProcessError as e:
            print(f"Error executing command for {verilog_filename}: {e}")

    # 返回最大cost值对应的模块名
    return best_module_name

# 示例调用函数
#base_command = "cost_estimator_3"
#library_file = "lib1.json"
#output_file = "cf3_ex2.out"
#module_names = ['and_6', 'and_2', 'and_3', 'and_4', 'and_5', 'and_1', 'and_7', 'and_8']
#best_module = find_max_cost_module(base_command, library_file, output_file, module_names)
#print(f"最大的cost值对应的模块名是 {best_module}")

def find_min_cost_module_not2(base, library_file, output_file, module_names):
    # 模块名列表
    
    output_option = "-output"
    # 最大的cost值和对应的模块名
    min_cost = float('inf')
    best_module_name = ""
    for i in range(1, 7):
        base_command = f'./cost_estimator_{i}'
        for module_name in module_names:
            # 构建.verilog文件的内容
            verilog_content = f"""module top_1598227639_809568180_776209382_1234615 (a, o);
    input a;
    output o;
    {module_name} (a, o);
    endmodule
            """
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
                else:
                    print(f"Output file '{output_file}' not found.")
            except subprocess.CalledProcessError as e:
                print(f"Error executing command for {verilog_filename}: {e}")

    # 返回最大cost值对应的模块名
    return best_module_name