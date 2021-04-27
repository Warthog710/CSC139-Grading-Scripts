import os
import re
import subprocess
import shutil

#? This is the path to the directory where your test cases are stored... along with their solutions
#? Test case 1 name: input1.txt & Solution 1 named: output1.txt and so forth...
TEST_CASES_PATH = '/home/roemerq/CSC139_Grading/Assignment3/master/test_cases/'

#? The number of test cases, along with where the extra test cases start (puts a flag in the summary)
TEST_CASE_NUM = 22
EXTRA_TEST_CASE_START = 17

# Runs test cases. This function places an input.txt into the student directory, runs it, and records its output.txt in a results folder
#? For this to work... A student program MUST read a file 'input.txt' from the same directory it is place. In addition, it must record 
#? an 'output.txt' in the same directory.
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
            print(f'Running cases for {entry}')

            if not os.path.exists('./results'):
                os.mkdir('results')

            for x in range(1, TEST_CASE_NUM + 1):
                shutil.copy(TEST_CASES_PATH + f'input{x}.txt', './input.txt')

                #Run the test...
                errorFile = open(f'./error_file_{x}.txt', 'w')
                process = subprocess.Popen(['./a.out', 'input.txt', 'output.txt'], stderr=errorFile, stdout=subprocess.DEVNULL)

                try:
                    process.wait(2)
                except:
                    process.kill()
                    errorFile.write(f'Timed out on input {x}.\n')

                #Move the result to the results folder and del input.txt
                try:
                    os.rename('output.txt', f'output{x}.txt')
                    shutil.move(f'output{x}.txt', f'./results/output{x}.txt')
                    os.remove('./input.txt')
                except Exception:
                    errorFile.write(f'Failed to produce output for test {x}.\n')

                #Close if not already closed
                if not errorFile.closed:
                    errorFile.close()

                #Remove the input file if it exists
                if os.path.exists('./input.txt'):
                    os.remove('./input.txt')                    

                # If the error file is 0 remove it
                if os.stat(f'./error_file_{x}.txt').st_size == 0:
                    os.remove(f'./error_file_{x}.txt')

        # Else, we must be dealing with a java file
        else:
            fileName = None

            print(f'Running cases for {entry}')

            if not os.path.exists('./results'):
                os.mkdir('results')

            # Iterate through java files and find the one that has main
            for file in os.listdir():
                if file.endswith('.java'):
                    codeFile = open(file)
                    if 'public static void main' in codeFile.read():
                        fileName = file.split('.')[0]

            # Close the file and verify we caught a name
            try:
                codeFile.close()
            except UnboundLocalError:
                pass

            if fileName == None:
                continue

            for x in range(1, TEST_CASE_NUM + 1):
                shutil.copy(TEST_CASES_PATH + f'input{x}.txt', './input.txt')
                errorFile = open(f'./error_file_{x}.txt', 'w')
                process = subprocess.Popen(['java', fileName, 'input.txt', 'output.txt'], stderr=errorFile, stdout=subprocess.DEVNULL)

                try:
                    process.wait(2)
                except:
                    process.kill()
                    errorFile.write(f'Timed out on input {x}.\n')

                #Move the result to the results folder and del input.txt
                try:
                    os.rename('output.txt', f'output{x}.txt')
                    shutil.move(f'output{x}.txt', f'./results/output{x}.txt')
                    os.remove('./input.txt')
                except Exception:
                    errorFile.write(f'Failed to produce output for test {x}.\n')

                #Close if not already closed
                if not errorFile.closed:
                    errorFile.close()

                #Remove the input file if it exists
                if os.path.exists('./input.txt'):
                    os.remove('./input.txt')                    

                # If the error file is 0 remove it
                if os.stat(f'./error_file_{x}.txt').st_size == 0:
                    os.remove(f'./error_file_{x}.txt')        

        os.chdir('..')

# Reads through the results of the tests and performs a line by line comparison.
# Stored in the student folder will be a summary file highlighting areas of potential issue
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

        # Change to results directory and create summary file
        os.chdir(f'./{entry}/results')
        compareResults = open('../result_summary.txt', 'w')

        # Compare all tests
        for x in range(1, TEST_CASE_NUM + 1):

            # If we are at the extra test cases, mark it in the summary file
            if x == EXTRA_TEST_CASE_START:
                compareResults.write(f'\n\n-- START EXTRA TEST CASES --\n\n')


            # Open the master file for that test case
            compareResults.write(f'Test Case #{x} - ')
            correctFile = open(f'/home/roemerq/CSC139_Grading/Assignment3/master/test_cases/output{x}.txt', 'r')

            # Try to open the result file, if we can't it must not exist... skip it
            try:
                resultFile = open(f'./output{x}.txt', 'r')
            except FileNotFoundError:
                # Record error
                correctLine = re.sub(r'[\n\t\s]*', '', correctFile.readline())
                compareResults.write(correctLine + '\n')
                compareResults.write('\tStudent output not found...\n')
                correctFile.close()
                continue
                
            # We will use this variable to track the line we are on... starting at 1
            lineCount = 1

            try:
                # For all the lines in the result file... attempt to compare them
                for result in resultFile:
                    # Strip all \n \t and whitespace
                    correctLine = re.sub(r'[\n\t\s]*', '', correctFile.readline())
                    resultLine = re.sub(r'[\n\t\s]*', '', result)

                    #If we are on the first line...
                    if lineCount == 1:
                        compareResults.write(correctLine + '\n')

                        # If they don't match, record an algorithm mismatch.
                        if correctLine != resultLine:
                            compareResults.write(f'\tAlgorithm mismatch: Correct={correctLine}, Student={resultLine}\n')

                    # Compare average waiting time
                    elif 'AVGWaitingTime:' in correctLine:
                        correctLine = correctLine.split(':')[1].strip()
                        resultLine = resultLine.split(':')[1].strip()

                        # If the times do not match, record it
                        if resultLine != correctLine:
                            compareResults.write(f'\tIncorrect waiting time: Correct={correctLine}, Student={resultLine}\n')

                    # If the id/time does not match record it
                    elif resultLine != correctLine:
                        compareResults.write(f'\tProcess Id mismatch on line {lineCount}: Correct={correctLine}, Student={resultLine}\n')

                    lineCount += 1

            # If at any time an error occurs, record it.
            #? Likely to be caused if the correct file has less lines than their output...
            except Exception:
                compareResults.write(f'\tAn unknown error occured on line {lineCount}...\n')

            # Close the files
            resultFile.close()
            correctFile.close()             

        #Close our comparison file and go back two directories
        compareResults.close()
        os.chdir('../..')

# Do the thing
run_test_cases()
check_results()