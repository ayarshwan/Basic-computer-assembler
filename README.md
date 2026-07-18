# Basic Computer Assembler 🖥️

A **two-pass assembler** written in Python that translates assembly language programs into binary machine code for **Mano's Basic Computer** architecture (from *Computer System Architecture*).

## ✨ Features
- **First Pass:** builds a symbol table by scanning labels and calculating memory addresses
- **Second Pass:** generates 16-bit binary machine code using the symbol table
- Supports all three instruction formats:
  - **MRI** (Memory Reference Instructions): `AND`, `ADD`, `LDA`, `STA`, `BUN`, `BSA`, `ISZ`
  - **RRI** (Register Reference Instructions): `CLA`, `CLE`, `CMA`, `CME`, `CIR`, `CIL`, `INC`, `SPA`, `SNA`, `SZA`, `SZE`, `HLT`
  - **I/O Instructions**: `INP`, `OUT`, `SKI`, `SKO`, `ION`, `IOF`
- Handles **direct and indirect addressing** (`I` suffix)
- Supports pseudo-instructions: `ORG`, `END`, `HEX`, `DEC`
- Converts decimal/hex operands to binary, including **two's complement** for negative numbers
- Ignores comments (`/`) and blank lines

## 🧠 How it works
1. **`firstpass()`** scans the source line by line, tracking a location counter and recording every label's address in a symbol table.
2. **`second_pass()`** re-scans the code, this time using the symbol table to resolve operand addresses, and encodes each instruction/data line into its correct binary format (opcode + addressing mode + 12-bit address, or fixed patterns for RRI/I-O instructions).

## ▶️ Usage
```bash
python assembler.py
```

Edit the `assembler_code` string with your own assembly program, following this format:
```asm
            ORG 100
            LDA SUB
            CMA
            INC
            ADD  MIN
            STA  DIF
            HLT
MIN,        DEC  83
SUB,        DEC  -23
DIF,        HEX  0
            END
```

## 📌 Example Output
symbol lable= {'MIN': 106, 'SUB': 107, 'DIF': 108}
First pass done, wait for second pass..

Machine Code:
100: 0010000001101011
101: 0111001000000000
102: 0111000000100000
103: 0001000001101010
...
second pass done yoo!


## 🛠️ Requirements
No external dependencies — pure Python 3 standard library.

