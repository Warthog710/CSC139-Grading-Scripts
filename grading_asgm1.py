import os
import subprocess

def read_test_cases():
    print('Reading test cases...')
    test_cases = []
    #Open file and read
    test_cases_file = open('./test_cases.txt', 'r')

    for line in test_cases_file:
        #If the line starts with # or \n ignore it
        if line.startswith('#') or line.startswith('\n'):
            continue        
        test_cases.append(line.strip('\n'))

    #Close file and return the test cases read
    test_cases_file.close()
    return test_cases



def sort_submissions():
    print('Sorting submissions...')
    

def rename_submissions():
    print('Renaming submissions...')

def compile_submissions():
    print('Compiling submissions...')

def run_test_cases(test_cases):
    print('Running test cases...')


test_cases = read_test_cases()
print(test_cases)