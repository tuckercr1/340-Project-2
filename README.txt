Alex Laughlin
Chris Tucker
CSCI 340
Project 2

The program p2.py is a memory simulator that simulates a round robin scheduler. It takes 8 parameters that can be passed from the command line: 
1. computer memory size
2. page size
3. the number of jobs
4. the minimum job run time
5. the maximum job run time
6. the minimum job memory
7. the maximum job memory
8. a random seed


***How To Run***
This program was made with python version 3.8.2 and it is recommended to use this version to run.
To run the program from the linux terminal, open the file location in the terminal and type "python3 p2.py argv[1] argv[2] argv[3] argv[4] argv[5] argv[6] argv[7] argv[8]"

***Important Notes***
There are acaully 9 parameters passed. The 0th parameter is the name of the program and is not used.
Parameters 1 through 8 MUST BE integers.
The computer memory size MUST BE an even multiple of the page size.
The minumum job run time MUST BE smaller than the maximum job run time.
The minimum job memory MUST BE smaller than the maximum job memory.
If you do not pass the correct amount of arguments when calling the program, you will be asked to provide each parameter individually.

