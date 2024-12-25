#!/usr/bin/python3

import re
import time
import sys

# Check if a file name is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: ./interpreter <filename>")
    sys.exit(1)

# Get the file name from the command line argument
file_name = sys.argv[1]

# Open the file
InstructionLines = []
try:
    file = open(file_name,"r")
    for line in file:
        InstructionLines.append(line.strip())
    file.close()
except FileNotFoundError:
    print(f"Error: The file '{file_name}' was not found.")
    sys.exit(1)

registers = {
    "r0": 0, "r1": 0,
    "r2": 0, "r3": 0,
    "r4": 0, "r5": 0,
    "r6": 0, "r7": 0,
    "r8": 0, "r9": 0
}


strings = {}  # Dictionary to store string variables

cmdTypes = ["add", "sub", "mult", "div", "put", "jmpe", "jmpu", "prn", "halt"]

numOfLines = len(InstructionLines)
i = 0

while i < numOfLines:
    curInstruction = re.split(r"[ ,]+", InstructionLines[i])

    if len(curInstruction) == 0 or curInstruction[0] not in cmdTypes:
        print(f"Skipping invalid instruction at line {i}: {InstructionLines[i]}")
        i += 1
        continue

    if curInstruction[0] == "add":
        result = registers[curInstruction[1]] + registers[curInstruction[2]]
        registers[curInstruction[2]] = result
        print("Sum:", result)

    elif curInstruction[0] == "sub":
        result = registers[curInstruction[1]] - registers[curInstruction[2]]
        registers[curInstruction[2]] = result
        print("Difference:", result)

    elif curInstruction[0] == "mult":
        result = registers[curInstruction[1]] * registers[curInstruction[2]]
        registers[curInstruction[2]] = result
        print("Result:", result)

    elif curInstruction[0] == "div":
        result = registers[curInstruction[1]] / registers[curInstruction[2]]
        registers[curInstruction[2]] = result
        print("Quotient:", result)

    elif curInstruction[0] == "put":
        # Check if the value is a string
        if curInstruction[1].startswith('"') and curInstruction[1].endswith('"'):
            # It's a string assignment
            strings[curInstruction[2]] = curInstruction[1][1:-1]  # Remove the quotes
            print(f"Assigned string to {curInstruction[2]}:", strings[curInstruction[2]])
        else:
            # It's an integer assignment
            registers[curInstruction[2]] = int(curInstruction[1].strip())
            print("Assigned:", curInstruction[2].strip(), registers[curInstruction[2]])

    elif curInstruction[0] == "jmpe":
        if registers[curInstruction[1].strip()] == registers[curInstruction[2].strip()]:
            i = int(curInstruction[3])  # Jump to line specified by jmpe
            continue

    elif curInstruction[0] == "jmpu":
        i = int(curInstruction[1])  
        continue

    elif curInstruction[0] == "prn":
        # Print either register value or string value
        if curInstruction[1] in registers:
            print(registers[curInstruction[1]])
        elif curInstruction[1] in strings:
            print(strings[curInstruction[1]])

    elif curInstruction[0] == "halt":
        print("Program halted\n")
        break

    i += 1
    time.sleep(0.1)  # Slowing down each iteration to show each step as it gets executed
