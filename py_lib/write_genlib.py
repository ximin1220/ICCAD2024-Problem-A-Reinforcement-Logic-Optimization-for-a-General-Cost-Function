def write_genlib(best_gates, genlib_path):
    gates = ('and', 'not', 'nor', 'nand', 'buf', 'xor', 'xnor', 'or')
    with open(genlib_path, 'w') as f:
        for gate in gates:
            if gate == 'and':
                content = ''
                content = f"GATE {best_gates[gate][0]}    {best_gates[gate][1]}  Y=A*B;                       PIN * NONINV 1 999 1 0 1 0\n"
            elif gate == 'or':
                content = ''
                content = f"GATE {best_gates[gate][0]}    {best_gates[gate][1]}  Y=A+B;                       PIN * NONINV 1 999 1 0 1 0\n"
            elif gate == 'xor':
                content = ''
                content = f"GATE {best_gates[gate][0]}    {best_gates[gate][1]}  Y=(A*!B)+(!A*B);                       PIN * NONINV 1 999 1 0 1 0\n"
            elif gate == 'nor':
                content = ''
                content = f"GATE {best_gates[gate][0]}    {best_gates[gate][1]}  Y=!(A+B);                       PIN * NONINV 1 999 1 0 1 0\n"
            elif gate == 'xnor':
                content = ''
                content = f"GATE {best_gates[gate][0]}    {best_gates[gate][1]}  Y=(A*B)+(!A*!B);                       PIN * NONINV 1 999 1 0 1 0\n"
            elif gate == "nand":
                content = ''
                content = f"GATE {best_gates[gate][0]}    {best_gates[gate][1]}  Y=!(A*B);                       PIN * NONINV 1 999 1 0 1 0\n"
            elif gate == 'buf':
                content = f"GATE {best_gates[gate][0]}    {best_gates[gate][1]}  Y=A;                         PIN * NONINV 1 999 1 0 1 0\n"
            elif gate == 'not':
                content = f"GATE {best_gates[gate][0]}    {best_gates[gate][1]}  Y=!A;                        PIN * NONINV 1 999 1 0 1 0\n"
            else:
                content = ''
            f.write(content)
    # with open(genlib_path, 'w') as f:
    #     for gate in gates:
    #         if gate == 'and':
    #             content = f"GATE {best_gates[gate][0]}    1  Y=A*B;                       PIN * NONINV 1 999 1 0 1 0\n"
    #         elif gate == 'or':
    #             content = ''
    #             content = f"GATE {best_gates[gate][0]}    1  Y=A+B;                       PIN * NONINV 1 999 1 0 1 0\n"
    #         elif gate == 'xor':
    #             content = f"GATE {best_gates[gate][0]}    1  Y=(A*!B)+(!A*B);                       PIN * NONINV 1 999 1 0 1 0\n"
    #         elif gate == 'nor':
    #             # content = ''
    #             content = f"GATE {best_gates[gate][0]}    1  Y=!(A+B);                       PIN * NONINV 1 999 1 0 1 0\n"
    #         elif gate == 'xnor':
    #             content = f"GATE {best_gates[gate][0]}    1  Y=(A*B)+(!A*!B);                       PIN * NONINV 1 999 1 0 1 0\n"
    #         elif gate == "nand":
    #             content = f"GATE {best_gates[gate][0]}    1  Y=!(A*B);                       PIN * NONINV 1 999 1 0 1 0\n"
    #         elif gate == 'buf':
    #             content = f"GATE {best_gates[gate][0]}    1  Y=A;                         PIN * NONINV 1 999 1 0 1 0\n"
    #         elif gate == 'not':
    #             content = f"GATE {best_gates[gate][0]}    1  Y=!A;                        PIN * NONINV 1 999 1 0 1 0\n"
    #         f.write(content)