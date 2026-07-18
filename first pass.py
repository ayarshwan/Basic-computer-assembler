def firstpass(assembler_code):
    symbol_label = {}
    location_counter = 0 

    for line in assembler_code.split('\n'):
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

assembler_code = """
ORG 100
LDA SUB
CMA
INC
ADD MIN
STA DIF
HLT
MIN, DEC 83
SUB, DEC -23
DIF, HEX 0
END
"""
symbol_lable= firstpass(assembler_code)
print("symbol lable=",symbol_lable)



