import os
import re
import string
import shutil
import subprocess

TEST_CASES_PATH = '/home/roemerq/CSC139_Grading/Assignment4/master/test_cases/'
TEST_CASE_NUM = 10
EXTRA_TEST_CASE_START = 6

def run_test_cases():
    print('Running test cases...')

    for entry in os.listdir():
        # Ignore certain items and non directories
        if entry.startswith('.') or not os.path.isdir(entry):
            continue

        # If the entry contains MANUAL skip it
        if 'MANUAL' in entry:
            continue

        os.chdir('./' + entry)

        # If this file exits, we will go ahead and run our test cases
        #? This is for C or C++ programs
        if os.path.exists('./a.out'):
            print(f'Runnig cases for {entry}')

            if not os.path.exists('./results'):
                os.mkdir('results')
            
            for x in range(1, TEST_CASE_NUM + 1):
                shutil.copy(TEST_CASES_PATH + f'input{x}.txt', './input.txt')

                #Run the test
                error_file = open(f'error_file_{x}.txt', 'w')
                process = subprocess.Popen(['./a.out', 'input.txt', 'output.txt'], stderr=error_file, stdout=subprocess.DEVNULL)

                #Give the process 2 seconds to complete, if not kill it
                try:
                    process.wait(2)
                except:
                    process.kill()
                    error_file.write(f'Timed out on input {x}.\n')

                #Move the results to the results folder and del input.txt
                try:
                    os.rename('output.txt', f'output{x}.txt')
                    shutil.move(f'output{x}.txt', f'./results/output{x}.txt')
                    os.remove('./input.txt')
                except Exception:
                    error_file.write(f'Failed to produce output for test {x}.\n')

                #Close the error file
                if not error_file.closed:
                    error_file.close()

                #Remove the input file if it exists
                if os.path.exists('./input.txt'):
                    os.remove('./input.txt')

                #If the errror file is zero remove it
                if os.stat(f'./error_file_{x}.txt').st_size == 0:
                    os.remove(f'./error_file_{x}.txt')

        #? For Java files
        else:
            filename = None
            print(f'Running cases for {entry}')

            if not os.path.exists('./results'):
                os.mkdir('results')

            #Iterate through java files to find that one that contains main
            for file in os.listdir():
                if file.endswith('.java'):
                    codeFile = open(file)
                    if 'public static void main' in codeFile.read():
                        filename = file.split('.')[0]

            #Try to close the file and verify we caught a name
            try:
                codeFile.close()
            except UnboundLocalError:
                pass

            if filename == None:
                continue

            #Run the tests
            for x in range(1, TEST_CASE_NUM + 1):
                shutil.copy(TEST_CASES_PATH + f'input{x}.txt', './input.txt')

                #Run the test
                error_file = open(f'error_file_{x}.txt', 'w')
                process = subprocess.Popen(['java', filename, 'input.txt', 'output.txt'], stderr=error_file, stdout=subprocess.DEVNULL)

                #Give the process 2 seconds to complete, if not kill it
                try:
                    process.wait(2)
                except:
                    process.kill()
                    error_file.write(f'Timed out on input {x}.\n')

                #Move the results to the results folder and del input.txt
                try:
                    os.rename('output.txt', f'output{x}.txt')
                    shutil.move(f'output{x}.txt', f'./results/output{x}.txt')
                    os.remove('./input.txt')
                except Exception:
                    error_file.write(f'Failed to produce output for test {x}.\n')

                #Close the error file
                if not error_file.closed:
                    error_file.close()

                #Remove the input file if it exists
                if os.path.exists('./input.txt'):
                    os.remove('./input.txt')

                #If the errror file is zero remove it
                if os.stat(f'./error_file_{x}.txt').st_size == 0:
                    os.remove(f'./error_file_{x}.txt')

        os.chdir('..')

def check_results():
    print('Checking results...')
    for entry in os.listdir():
        # Ignore certain items and non directories
        if entry.startswith('.') or not os.path.isdir(entry):
            continue

        # If the entry contains MANUAL skip it
        if 'MANUAL' in entry:
            continue

        # If the results directory is missing, the tests were not run
        if not os.path.exists(entry + '/results'):
            continue
        
        # Change to the results directory and create a summary file
        os.chdir(f'./{entry}/results')
        compareResults = open('../result_summary.txt', 'w')

        # Compare all the tests
        for x in range(1, TEST_CASE_NUM + 1):

            # If we are at the extra test cases, mark it
            if x == EXTRA_TEST_CASE_START:
                compareResults.write(f'\n\n-- START EXTRA TEST CASES --\n\n')

            #? 0 = FIFO, 1 = Optimal, 2 = LRU
            for algorithm in ['FIFO', 'Optimal', 'LRU']:
                # Open the master file for that test case
                correctFile = open(f'{TEST_CASES_PATH}output{x}.txt', 'r')

                # Try to open the students output
                try:
                    resultFile = open(f'./output{x}.txt', 'r')
                except:
                    compareResults.write(f'Test Case {x}: All Algorithms\n')
                    compareResults.write(f'\tStudent output not found...\n')
                    correctFile.close()
                    break

                if 'FIFO' in algorithm:
                    compareResults.write(f'Test Case {x}: {algorithm}\n')
                    #Read until the FIFO line
                    while True:
                        correctLine = correctFile.readline()

                        if 'FIFO' in correctLine:
                            break

                    #Read students file until FIFO is found
                    while True:
                        resultLine = resultFile.readline()

                        if 'FIFO' in resultLine.upper() or 'FIRST IN FIRST OUT' in resultLine.upper():
                            break

                        # If this triggers, we have reached the end of the file
                        elif '' == resultLine:
                            break

                elif 'Optimal' in algorithm:
                    compareResults.write(f'Test Case {x}: {algorithm}\n')
                    #Read until the optimal line
                    while True:
                        correctLine = correctFile.readline()

                        if 'Optimal' in correctLine:
                            break

                    #Read students file until optimal is found
                    while True:
                        resultLine = resultFile.readline()

                        if 'OPTIMAL' in resultLine.upper() or 'OPT' in resultLine.upper():
                            break

                        # If this triggers, we have reached the end of the file
                        elif '' == resultLine:
                            break

                else:
                    compareResults.write(f'Test Case {x}: {algorithm}\n')
                    #Read until the LRU line
                    while True:
                        correctLine = correctFile.readline()

                        if 'LRU' in correctLine:
                            break

                    #Read stduents file until LRU is found
                    while True:
                        resultLine = resultFile.readline()

                        if 'LRU' in resultLine.upper() or 'LEAST RECENTLY USED' in resultLine.upper():
                            break

                        # If this triggers, we have reached the end of the file
                        elif '' == resultLine:
                            break

                # This is a stupid but easy way to quit that particular algorithm for that test case
                if '' == resultLine:
                    compareResults.write(f'\tStudent output for {algorithm} not found...\n')
                    correctFile.close()
                    resultFile.close()
                    continue

                # Read and compare lines until we reach the page fault line in the master file
                lineCount = 1
                while True:
                    try:
                        #? Do the reading...
                        #Strip and lowercase everything
                        correctLine = correctFile.readline().strip().lower()
                        resultLine = resultFile.readline().strip().lower()

                        #Remove puncuation
                        regex = re.compile('[%s]' % re.escape(string.punctuation))
                        correctLine = regex.sub('', correctLine)
                        resultLine = regex.sub('', resultLine)

                        #Remove double spaces
                        correctLine = re.sub(' +', ' ', correctLine)
                        resultLine = re.sub(' +', ' ', resultLine)

                        #If the lines are not equal, record it
                        if correctLine != resultLine:
                            compareResults.write(f'\tLine Mismatch: {lineCount}\n')
                            compareResults.write(f'\t\tCorrect: {correctLine}\n')
                            compareResults.write(f'\t\tStudent: {resultLine}\n')

                        if 'page fault' in correctLine:
                            break

                        lineCount += 1

                    #An error occured... likely ran out of lines in students file? 
                    except Exception:
                        compareResults.write('\tAn unknown error occured...\n')
                        break

                correctFile.close()
                resultFile.close()

        compareResults.close()
        os.chdir('../..') 

run_test_cases()
check_results()
