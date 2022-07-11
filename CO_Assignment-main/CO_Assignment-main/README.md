# ASM ASSEMBLER SIMULATOR
Python script written to interpret and simulate asm code written using the OP Codes and Registers given in the Problem Statement

## Simple Assembler
Converts the given ASM script to binary

## Simple Simulator
Uses the converted ASM script to Binary to simulate what it was originally intented to by dumping the values of all registers after processing every command, futher it also provides a graph plotting memory accessed vs cycle count

## How to evaluate/Run
* Go to the `automatedTesting` directory and execute the `run` file with appropiate options passed as arguments.
* Options available for automated testing:
	1. `--verbose`: Prints verbose output
	2. `--no-asm`: Does not evaluate the assembler
	3. `--no-sim`: Does not evaluate the simulator
