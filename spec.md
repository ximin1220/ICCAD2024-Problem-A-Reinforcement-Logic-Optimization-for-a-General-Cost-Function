這是一份將提供的 PDF 規格書轉換為 Markdown 格式的文件。

Reinforcement Logic Optimization for a General Cost Function 

**Authors:** Chung-Han Chou, Kwangsoo-Han, Chih-Jen (Jacky) Hsu, Chi-An (Rocky) Wu, and Kuan-Hua Tu **Organization:** Cadence Design Systems, Inc. 

**Version History:**

* 2024.03.04: First Version 


* 2024.05.22: Update runtime limit, add a reference to json format and output file example 



---

1. Introduction 

Logic synthesis/optimization is a key step in digital design flow. Traditionally, in this stage, the optimization metrics PPA (power, performance, area) might be majorly determined. However, as the technology node shrinks and the design process becomes extremely complicated, the logic optimization tools might be invoked into some iterative optimization flow or called by some local re-synthesis for variant purposes.

In the meantime, the optimization metric would not be limited to PPA. It may also optimize for critical modules, placeability, routability, verification, testability, engineering change order, system redundancy, and more.

In this contest, we propose a reinforcement logic optimization problem. We will provide a cost function estimator (a black-box executable file). Contestants are tasked with developing a program that interacts with the estimator and learns to perform optimizations to minimize the cost.

**Optimization Framework:**
The expected optimization framework involves the given netlist and cell library as inputs, and the optimized netlist as output. In the framework, the developed algorithms and the cost function estimator continuously interact with each other. The algorithms perform optimizations based on the cost received from the estimator and output the optimized netlist to the estimator. The estimator receives the optimized netlist and outputs the cost to the algorithms again. The objective is for the algorithms to learn to minimize the cost.

(See Figure 1 in original document for the framework diagram) 

---

2. Background 

2.1 Logic optimization in local re-synthesis 

Local re-synthesis is widely used in modern design flow not only for PPA, but also for other reasons such as resolving congestion, supporting functional ECO, etc. In such complex scenarios, the objective is to correctly model the criticality and budget of resources (timing, power, P&R resource, ...) as non-linear functions in local re-synthesis.

In addition, there is a set of complicated constraints different from one block to the other. For example, in ECO, when spare cells are limited, the number of usable cells becomes a constraint. Similarly, considering routing resources during local resynthesis is important to avoid congestion and DRC violations. Considering all conditions, an optimization strategy for general cost function may greatly reduce human effort and time for design closure.

2.2 Reinforcement learning and logic optimization 

Traditional machine learning techniques typically rely on large amounts of hand-labeled training data, which is challenging to obtain for optimization problems. In contrast, reinforcement learning (RL) enables an AI-driven system to learn through trial and error, receiving feedback from its actions. This makes RL well-suited for problems requiring search and exploration of a vast solution space within a complex environment.

For this problem, contestants are expected to develop an intelligent methodology to explore the solution space rather than relying on a cost-function-based algorithm.

---

3. Problem Formulation and Input Output Format 

This section defines the input, output, and requirements of this contest. The submitted executable file should take three input files and output the optimized netlist.

**Inputs:**

1. A flattened Verilog netlist to be optimized.


2. A cell library describing the spec of each library cell.


3. A cost function estimator (an executable file).



**Objective:**
Generate a functionally equivalent netlist using the cells in the cell library and minimize the cost reported by the estimator.

3.1 Program requirement 

* 
**System:** Must run on a Linux system.


* 
**Time Limit:** 3 hours for each case.


* 
**Parallelism:** Parallel computation with multiple threads or processes is **not** allowed.


* 
**Arguments:** The program should accept four arguments:


* `-netlist <netlist_path/name.v>`
* `-library <lib_path/name.lib>`
* `-cost_function <cost_function_path/name>`
* `-output <output_path/name.v>`



**Execution Example:**

```bash
./cada0000_alpha -cost_function cost_function_1 -library low_vt.lib -netlist design.v -output design_optimized.v

```



3.2 Input file format 

3.2.1 Netlist 

The input netlist is a flattened netlist in Verilog format without hierarchy (one top module only). It is composed of:

1. Primitive gates: `and`, `or`, `nand`, `nor`, `not`, `buf`, `xor`, `xnor`.


2. Wires.


3. Constant values: `1'b1`, `1'b0`.



**Notes:**

* All primitive gates (except `buf` and `not`) have 2 inputs and 1 output.


* 
`buf` and `not` gates have 1 input and 1 output.


* All primary inputs and outputs are scalars (one-bit signals) .



3.2.2 Cell library 

* At least one cell exists for each primitive gate.


* **Pin Names:**
* For 2-input cells: Inputs are `A` and `B`, output is `Y`.


* For `not` and `buf`: Input is `A`, output is `Y`.




* 
**Format:** JSON-like format.


* **Information Section:**
* 
`cell_num`: Number of cells.


* 
`attribute_num`: Number of attributes per cell.


* `attributes`: Array of property names. At least `cell_name` and `cell_type` are given.




* 
**Cells Section:** JSON array of cells.


* Values for `cell_name` and `cell_type` are strings.


* Attributes ending in `_f` are floating numbers.


* Attributes ending in `_i` are integers.


* 
`cell_type` matches one of the primitive gates.







**Library Example (Figure 2):**

```json
{
  "information": {
    "cell_num": "8",
    "attribute_num": "6",
    "attributes" : [ "cell_name", "cell_type", "delay_f", "power_f", "attribute_1_i", "attribute_2_f" ]
  },
  "cells": [
    {
      "cell_name": "NAND2X1",
      "cell_type": "nand",
      "delay_f": "45.23",
      "power_f": "910.85",
      "attribute_1_i": "123",
      "attribute_2_f": "45.678"
    }
  ]
}

```



3.2.3 Cost function estimator 

An executable file that takes 2 input files (cell library and netlist) and generates 1 output file. All gates in the netlist must be specified by the cell library. The output file contains a floating number denoting the cost.

**Execution Example:**

```bash
./cost_function_1 -library low_vt.lib -netlist design_iter0008.v -output cost_0008.txt

```



3.3 Output file format and requirements 

* The output file must be a Verilog netlist.


* 
**DO NOT** change the name of the top module.


* 
**DO NOT** change the name and declaration for primary inputs and outputs.


* Only cells specified in the cell library are allowed.



**Output Netlist Example (Figure 3):**

```verilog
module top (a, b, c, d, e, f, g, h, o);
  input a, b, c, d, e, f, g, h;
  output o;
  and_1 g0(a,b,y1);
  and_1 g1(c,d,y2);
  and_1 g2(e,f,y3);
  and_1 g3(g,h,y4);
  and_1 g4(y1,y2,y5);
  and_1 g5(y3,y4,y6);
  and_1 g6(y5,y6,o);
endmodule

```



---

4. Evaluation Criteria 

1. **Correctness:** Necessary. If the generated netlist is not functionally equivalent to the given netlist, the contestants will get zero points for the case.


2. 
**Cost:** The cost reported by the cost function estimator on the finally outputted netlist.


3. **Points Calculation:**





4. 
**Final Score:** The sum of points of all cases. The team having the largest final_score wins.



---

5. Examples 

TBD. 

---

6. References 

* [1] Maestre, S., Gumera, A., Hora, J., & de Guzman, M. J. (2022, July). Improving Digital Design PPA (Performance, Power, Area) using iSpatial Physical Restructuring. In 2022 37th International Technical Conference on Circuits/Systems, Computers and Communications (ITC-CSCC) (pp. 647-651). IEEE. 


* [2] Pandini, D., Pileggi, L. T., & Strojwas, A. J. (2002, March). Congestion-aware logic synthesis. In Proceedings 2002 Design, Automation and Test in Europe Conference and Exhibition (pp. 664-671). IEEE. 


* [3] Ratkovic, I., Palomar, O., Stanic, M., Unsal, O., Cristal, A., & Valero, M. (2014, July). Physical vs. physically-aware estimation flow: case study of design space exploration of adders. In 2014 IEEE Computer Society Annual Symposium on VLSI (pp. 118-123). IEEE. 


* [4] Tatsuoka, M., Watanabe, R., Otsuka, T., Hasegawa, T., Zhu, Q., Okamura, R., ... & Takabatake, T. (2015, June). Physically aware high level synthesis design flow. In Proceedings of the 52nd Annual Design Automation Conference (pp. 1-6). 


* [5] What is reinforcement learning? [https://online.york.ac.uk/what-is-reinforcement-learning/](https://online.york.ac.uk/what-is-reinforcement-learning/) 


* [6] Mnih, V., Kavukcuoglu, K., Silver, D., Graves, A., Antonoglou, I., Wierstra, D., & Riedmiller, M. (2013). Playing atari with deep reinforcement learning. arXiv preprint arXiv:1312.5602. 


* [7] Shan-Hung Wu, "Reinforcement Learning," datalab.github.io/ml/slides/14 Reinforcement Learning.pdf 


* [8] JSON Introduction [https://www.w3schools.com/js/js_json_intro.asp](https://www.w3schools.com/js/js_json_intro.asp)