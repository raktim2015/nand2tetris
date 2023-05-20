import sys

final_instruction = []
lno=-1
global st_variable
st_variable = 16
c_a = {
            "101010": ["0", ""],
            "111111": ["1", ""],
            "111010": ["-1" , ""],
            "001100": ["D", ""],
            "110000": ["A", "M"],
            "001101": ["!D"],
            "110001": ["!A", "!M"],
            "001111": ["-D"],
            "110011": ["-A", "-M"],
            "011111": ["D+1", ""],
            "110111": ["A+1", "M+1"],
            "001110": ["D-1"],
            "110010": ["A-1", "M-1"],
            "000010": ["D+A", "D+M"],
            "010011": ["D-A", "D-M"],
            "000111": ["A-D", "M-D"],
            "000000": ["D&A", "D&M"],
            "010101": ["D|A", "D|M"]
        }

dest_map = {
    "0": "000",
    "": "000",
    "M": "001",
    "D": "010",
    "DM": "011",
    "MD": "011",
    "A": "100",
    "AM": "101",
    "MA": "101",
    "AD": "110",
    "DA": "110",
    "ADM": "111",
    "AMD": "111",
    "MAD": "111",
    "MDA": "111",
    "DAM": "111",
    "DMA": "111"
}

jmp_map = {
    "": "000",
    "0": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
}

predefined_symbols = {
    "SP": "0000000000000000",
    "LCL": "0000000000000001",
    "ARG": "0000000000000010",
    "THIS": "0000000000000011",
    "THAT": "0000000000000100",
    "R0": "0000000000000000",
    "R1": "0000000000000001",
    "R2": "0000000000000010",
    "R3": "0000000000000011",
    "R4": "0000000000000100",
    "R5": "0000000000000101",
    "R6": "0000000000000110",
    "R7": "0000000000000111",
    "R8": "0000000000001000",
    "R9": "0000000000001001",
    "R10": "0000000000001010",
    "R11": "0000000000001011",
    "R12": "0000000000001100",
    "R13": "0000000000001101",
    "R14": "0000000000001110",
    "R15": "0000000000001111",
    "SCREEN": "0100000000000000",
    "KBD": "0110000000000000"
}

variables = {}
labels = {}

def convertAInstruction(tokens):
    global st_variable
    #print(tokens)
    tokens = tokens.strip()
    instruction = ""
    symbol = False
    for elem in tokens[1:]:
        #print(elem, ord(elem))
        if (ord(elem)>=48 and ord(elem)<=57):
            continue
        else:
            symbol=True
            break
    
    if not symbol:
        ins = int(tokens[1:])
        while ins>0:
            instruction = str(ins%2) + instruction
            ins = ins//2
        instruction = instruction.rjust(16, '0')

    else:
        a_symbol = tokens[1:].strip()
        if a_symbol in labels:
            instruction = labels[a_symbol]
        elif a_symbol in predefined_symbols:
            instruction = predefined_symbols[a_symbol]
        
        # new symbol
        elif a_symbol in variables:
            instruction = variables[a_symbol]
        else:
            curr = st_variable
            st_variable+=1
            while curr>0:
                instruction = str(curr%2) + instruction
                curr = curr//2
            instruction = instruction.rjust(16, '0')
            variables[a_symbol] = instruction
    
    #instruction = instruction.rjust(16,"0")
    final_instruction.append(instruction)
    #print(instruction)


def convertCInstruction(tokens):
    #print(tokens)
    tokens = tokens.strip()
    token = tokens
    instruction = "111"

    dest = ""
    comp = ""
    jmp = ""
    remaining = ""
    if ("=" in token) and (";" in token):
        dest = token.split("=")[0]
        remaining = token.split("=")[1]
        comp = remaining.split(";")[0]
        jmp = remaining.split(";")[1]
    elif ("=" in token):
        dest = token.split("=")[0]
        comp = token.split("=")[1]

    elif (";" in token):
        comp = token.split(";")[0]
        jmp = token.split(";")[1]
    

    flag = False
    print("elem ", c_a["110011"][1])
    for key in c_a:
        for index, elem in enumerate(c_a[key]):
            if elem == comp:
                if index==0:
                    instruction += "0"
                else:
                    instruction += "1"
                instruction += key
                flag=True
        if flag:
            break

    print("here dest = ", dest, " comp = ", comp, "jmp = ",jmp)
    instruction += dest_map[dest]
    instruction += jmp_map[jmp]
    #instruction = instruction.rjust(16,"0")
    final_instruction.append(instruction)


def markLabel(tokens, lno):
    tokens = tokens.strip()
    label = tokens[1:len(tokens)-1]
    instruction = ""
    ins = lno
    while ins > 0:
        instruction = str(ins%2) + instruction
        ins = ins//2
    instruction = instruction.rjust(16, '0')

    labels[label] = instruction


lines = []
with open(sys.argv[1], "r") as f:
    lines = f.readlines()


# remove comments
temp_lines = []
for line in lines:
    curr_line = line.strip()
    token = ""
    for elem in curr_line:
        if elem == '/':
            break
        if elem!=' ':
            token += elem
    if len(token)>0:
        temp_lines.append(token)
    
lines = temp_lines

# collect and remove all labels

lno = -1
for tokens in lines:
    lno+=1
    if tokens[0] == '(':
        markLabel(tokens, lno)
        lno-=1

print(labels)

for tokens in lines:
    
    print(tokens)
    if tokens[0]=='(':
        continue
    if tokens[0]=='@':
        convertAInstruction(tokens)
        continue
    else:
        convertCInstruction(tokens)
        continue


op_file = "Pong.hack"
with open(op_file, "w") as w:
    for ins in final_instruction:
        w.write(ins)
        w.write('\n')
        print(ins)