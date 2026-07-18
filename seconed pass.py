def format2bin(num: str,format_bits:int) -> str: #convert decimal or hex operands to binary
    
    valid_first_char = "6789ABCDEFabcdef"

    num = str(num)
    
    if (num[0] in valid_first_char) and all(c in "0123456789abcdefABCDEF" for c in num[1:]): 
     number = int(num, 16)  # Convert from hex to decimal
    else:
        number = int(num)  # Convert from decimal string to integer

    # If the number is decimal,positive or zero
    if number >= 0:
        return '{:b}'.format(number).zfill(format_bits)
    else: # handeling negative decimal number
        binary = '{:b}'.format(abs(number))  # Get binary representation of the absolute value
        binary = binary.zfill(format_bits)  # add zeros to match format_bits

        # Invert the bits (1's complement)
        inverted = ''.join('1' if bit == '0' else '0' for bit in binary)

        # Add 1 to get two's complement
        twos_complement = bin(int(inverted, 2) + 1)[2:].zfill(format_bits)

        return twos_complement
    
def convert_to_12bit_binary(num):
    # Convert the number to a string to separate each digit
    digits = str(num)
    
    # Convert each digit to a 4-bit binary using built-in function:format
    binary_digits = [format(int(digit), '04b') for digit in digits]
    
    # Join the 4-bit binary representations of the digits
    combined_binary = ''.join(binary_digits)
    
    # Ensure the total length is 12 bits by adding leading zeros if needed
    total_binary = combined_binary.zfill(12)
    
    return total_binary
   


opcode_dict = {   # Define opcode dictionary for mri
    "AND": "000",  
    "ADD": "001",  
    "LDA": "010",  
    "STA": "011",  
    "BUN": "100",  
    "BSA": "101",  
    "ISZ": "110",  
}

MR_instruction = {
    "AND": ["0", "8"],
    "ADD": ["1", "9"],
    "LDA": ["2", "A"],
    "STA": ["3", "B"],
    "BUN": ["4", "C"],
    "BSA": ["5", "D"],
    "ISZ": ["6", "E"], 
}
register_instruction = {
    "CLA": "0111100000000000",
    "CLE": "0111010000000000",
    "CMA": "0111001000000000",
    "CME": "0111000100000000",
    "CIR": "0111000010000000",
    "CIL": "0111000001000000",
    "INC": "0111000000100000",
    "SPA": "0111000000010000",
    "SNA": "0111000000001000",
    "SZA": "0111000000000100",
    "SZE": "0111000000000010",
    "HLT": "0111000000000001",
}

In_Out_instruction = {
    "INP": "1111100000000000",
    "OUT": "1111010000000000",
    "SKI": "1111001000000000",
    "SKO": "1111000100000000",
    "ION": "1111000010000000",
    "IOF": "1111000001000000"
}

def firstpass(assembler_code):
    symbol_label = {}
    location_counter = 0 

    for line in assembler_code.split('\n'):
        line = line.split('/')[0].strip()
        tokens = line.split()
        
        if not tokens:
            continue

        if tokens[0].endswith(","):  
            symbol_label[tokens[0].strip(",")] = location_counter
            location_counter += 1
        else:
            if tokens[0] == "ORG":
                location_counter = int(tokens[1])

            elif tokens[0] == "END":
                print("First pass done")
                break  
            else:
                location_counter += 1

    return symbol_label

def second_pass(assembler_code):
    symbol_table = {}
    location_counter = 0  # Starting location
    machine_code = {}

    # Collect all labels and their corresponding addresses
    for line in assembler_code.split('\n'):
        tokens = line.split()

    # handeling emptylines
        if not tokens:
            continue
    # handeling pesudocode ORG
        if tokens[0] == "ORG":
            location_counter = int(tokens[1])

    # handeling pesudocode END
        if tokens[0] == "END":
            break
    # handeling DIRECT/INDIRECT MRI INSC
        if tokens[0] in MR_instruction.keys() and len(tokens)>1:
            if tokens[-1] in ["I"]:
                direction= 1
                code=tokens[0]
                opcode=opcode_dict.get(code)
                Ilocation_counter=symbol_lable.get(tokens[1])
                binary_address= direction+opcode+str(convert_to_12bit_binary(Ilocation_counter))
                machine_code[location_counter] = binary_address
                location_counter += 1

            else:
                direction= str(0)
                code=tokens[0]
                opcode=opcode_dict.get(code)
                Ilocation_counter=symbol_lable.get(tokens[1])
                binary_address= direction+opcode+str(convert_to_12bit_binary(Ilocation_counter))
                machine_code[location_counter] = binary_address
                location_counter += 1

        elif tokens[0] in MR_instruction.keys() and len(tokens)==1:
                direction= str(0)
                code=tokens[0]
                opcode=str(opcode_dict.get(code))
                binary_address= direction+opcode+str(convert_to_12bit_binary(location_counter))
                machine_code[location_counter] = binary_address
                location_counter += 1       
        
    # handeling RRI INSC
        if tokens[0] in register_instruction.keys() :
            code=tokens[0]
            binary_address=register_instruction.get(code)
            machine_code[location_counter] = binary_address
            location_counter += 1

    # handeling IOI INSC
        if tokens[0] in In_Out_instruction.keys() :
            code=tokens[0]
            binary_address=In_Out_instruction.get(code)
            machine_code[location_counter] = binary_address
            location_counter += 1

    # handeling LABELS
        if tokens[0].endswith(",") and len(tokens)>2 and tokens[1] in ["HEX", "DEC"]:
               label = tokens[0].strip(",")
               number = tokens[2]
               binary_address = format2bin(number,16)
               machine_code[location_counter] = binary_address
               location_counter += 1

    return machine_code


# Example assemply program
assembler_code = """
            ORG 100
            LDA SUB
            CMA  
            INC  
            ADD  MIN
            STA  DIF
            HLT
MIN,        DEC  83
SUB,        DEC  -23 I
DIF,        HEX  0
            END;
"""

# Run the first pass and print the machine code
symbol_lable= firstpass(assembler_code)
print("symbol lable=",symbol_lable)
print("First pass done, wait for second pass..")

#call second pass func and assagin assembler_code to it
machine_code = second_pass(assembler_code)

# Display the machine code in the requested format
print("Machine Code:")
for address, code in machine_code.items():
    print(f"{address}: {code}")

print("second pass done yoo!")
