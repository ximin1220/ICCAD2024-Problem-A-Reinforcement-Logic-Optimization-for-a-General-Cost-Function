# Reinforcement Logic Optimization for a General Cost Function

**2024 CAD Contest - Logic Optimization**
**Achievement:** 🏆 Honorable Mention (Domestic / 國內賽佳作)
**Final Score:** 4074.506

## 📖 Overview

This project was developed for the **Reinforcement Logic Optimization for a General Cost Function** contest. The objective is to perform logic synthesis and optimization on a digital design netlist to minimize a cost defined by a "black-box" estimator .

Unlike traditional flows that optimize for PPA (Power, Performance, Area), this challenge requires the algorithm to interact with an unknown cost function executable, learning its preferences through trial and error to generate the optimal netlist .

## 🚀 Methodology

We implemented a framework combining **Simulated Annealing (SA)** with the **ABC Logic Synthesis System** (UC Berkeley) to explore the solution space and minimize the cost.

### 1. Optimization Engine: Simulated Annealing

The core of our solver uses Simulated Annealing to escape local optima and converge on a global minimum.

* **State:** The current netlist structure.
* **Action:** A random sequence of ABC optimization commands (e.g., `rewrite`, `balance`, `refactor`).
* **Cost:** Feedback provided by the external cost function estimator.
* **Acceptance Probability:** Metropolis criterion .

**Algorithm Pseudo-code:**

```cpp
// Initialization
s := initial netlist configuration
e := evaluate_cost(s, cost_estimator)
temp := initial_temp

while k < kmax and e > emin:
    // Generate neighbor by applying random ABC commands
    sn := random_neighbour(s, actions)
    en := evaluate_cost(sn, cost_estimator)

    // Metropolis Criterion
    if en < e or random() < exp((e - en) / temp):
        s := sn
        e := en
        if en < best_cost:
            best_s := sn
            best_cost := en

    // Cooling
    temp := max(temp * cooling_rate, min_temp)

```

### 2. Heuristics & Special Case Handling

Through analysis of the black-box estimator's behavior, we identified specific structural penalties and implemented targeted heuristics:

* **Redundancy Removal (`satclp`):**
* **Target:** Estimators 1, 4, 7, 8 (specifically Design 4).
* **Observation:** Standard commands failed to lower costs. The design contained redundant Boolean operations (chains of NAND/NOR/XOR).
* **Solution:** Applied the `satclp` command (SAT-based logic simplification). To prevent timeouts, we limited the Sum of Products (SOP) size using `-C 200`.


* **High Fanout Penalty (Buffer Insertion):**
* **Target:** Estimator 6.
* **Observation:** The estimator heavily penalized high fanout structures.
* **Solution:** We implemented a post-processing step to insert buffers at the output of every gate (excluding Primary Outputs and existing buffers). This drastically reduced the cost for specific cases to ~1.



## 🛠 System Requirements


**OS:** Linux System.


* **Dependencies:**
* C++ Compiler (GCC/Clang)
* [ABC System](https://github.com/berkeley-abc/abc) (Logic Synthesis and Verification Group, UC Berkeley)



## 💻 Usage

The program accepts arguments strictly following the contest specification.


### Execution

The executable takes the netlist, cell library, and cost function estimator as inputs.

```bash
./cada0009_final -netlist <netlist_path/name.v> \
                 -library <lib_path/name.lib> \
                 -cost_function <cost_function_path/name> \
                 -output <output_path/name.v>

```


**-netlist**: The input flattened Verilog netlist.



**-library**: The cell library in JSON-like format.



**-cost_function**: The black-box executable for cost estimation.



**-output**: The path for the optimized output netlist.



### Limits


**Time Limit:** 3 hours per case.



**Parallelism:** Multi-threading is not allowed.



## 📊 Results

* **Domestic Contest Result:** Honorable Mention (佳作).
* **Performance:** Achieved significant optimization ratios (up to ~637%) on complex test cases.

**Final Score:** 4074.506 (Calculated based on the summation of points from all cases).



## 📂 File Structure

* `src/`: Source code for the main optimization loop.
* `lib/`: Interface for interacting with ABC.
* `scripts/`: Automation scripts for testing different parameters.
* `abc/`: Submodule containing the ABC logic synthesis tool.

---

*Based on the 2024 CAD Contest Specification: Reinforcement Logic Optimization for a General Cost Function.*

