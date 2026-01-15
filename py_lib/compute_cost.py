import subprocess
import os

def compute_cost(input_file, base, library_file):
    # 模块名列表
    output_file = 'qwq.out'
    base_command = f'./{base}'
    output_option = "-output"
    # 最大的cost值和对应的模块名
    min_cost = float('inf')
    cost_value = -1

    # 构建完整的命令
    command = [base_command, "-library", library_file, "-netlist", input_file, "-output", output_file]
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

        else:
            print(f"Output file '{output_file}' not found.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing command for {input_file}: {e}")

    return cost_value

# print(compute_cost('add_buffer.v', 'test2/cost_estimator_6', 'test2/lib1.json'))
