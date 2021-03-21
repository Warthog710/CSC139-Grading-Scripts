import os
import subprocess
import shutil
import pathlib

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

    #Read through all files and put each students work in seperate folder
    for entry in os.listdir():
        #Ignore directories and .py files
        if os.path.isdir(entry) or entry.endswith('.py') or entry == 'test_cases.txt':
            continue

        #Get the student name
        student_name = entry.split('_')[0]

        if 'LATE' in entry:
            student_name += ' (LATE)'

        #Make the directory if not alread create
        if not os.path.exists('./' + student_name):
            os.mkdir('./' + student_name)

        #Move the file into the students directory
        shutil.move('./' + entry, './' + student_name)       


#This function is unique to assignment 1 as it relies on file names
def rename_submissions():
    print('Renaming submissions...')
    
    #Read through all directories and rename the students files
    for entry in os.listdir():
        #Ignore .vscode/.git folder and only look at directories
        if entry.startswith('.') or not os.path.isdir(entry):
            continue

        #Enter the directory
        os.chdir('./' + entry)

        #Loop through files in directory and rename
        for file in os.listdir():
            #If file ends with .c rename it
            if file.endswith('.c') or file.endswith('.C'):
                os.rename(file, 'MTFindProd.c')

            #Else it must be the report
            elif len(pathlib.Path(file).suffix) > 0:
                os.rename(file, 'report' + pathlib.Path(file).suffix)

        #Go back a directory
        os.chdir('..')

def compile_submissions():
    print('Compiling submissions...')

    #Read through all directories and compile the students files
    for entry in os.listdir():
        #Ignore .vscode/.git folder and only look at directories
        if entry.startswith('.') or not os.path.isdir(entry):
            continue

        #Enter the directory
        os.chdir('./' + entry)

        #Loop through files in directory and compile saving errors
        for file in os.listdir(): 
            #Compile the producer, ignoring warnings, saving any errors (if any)
            if 'MTFindProd.c' in file and not os.path.exists('./MTFindProd'):
                #Append #include <stdbool.h> to each file so they compile
                originalFile = open(file, 'r')
                data = originalFile.read()
                originalFile.close()
                newFile = open(file, 'w')
                newFile.write('#include <stdbool.h>\n' + data)
                newFile.close()

                #Create error file and compile
                error_file = open('./compiler_errors.txt', 'w')
                subprocess.run(['gcc', '-O3', './MTFindProd.c','-w', '-o', 'MTFindProd', '-lpthread'], stderr=error_file)
                error_file.close()

                #If the error file is size == 0, remove it as no errors occured
                if os.stat('./compiler_errors.txt').st_size == 0:
                    os.remove('./compiler_errors.txt')

        #Go back a directory
        os.chdir('..')

def detect_plagirism():
    print('Detecting plagirism...')
    for entry in os.listdir():
        if entry.startswith('.') or not os.path.isdir(entry):
            continue

        os.chdir('./' + entry)

        if os.path.exists('./MTFindProd.c'):
            outStr = ''
            codeFile = open('./MTFindProd.c', 'r')
            data = codeFile.read()

            #Start test
            if '#define MAX_SIZE 100000000' not in data:
                outStr += 'MAX_SIZE incorrect...\n'
            if '#define MAX_THREADS 16' not in data:
                outStr += 'MAX_THREADS incorrect...\n'
            if '#define RANDOM_SEED 6543' not in data:
                outStr += 'RANDOM_SEED incorrect...\n'
            if 'MAX_RANDOM_NUMBER 3000' not in data:
                outStr += 'RANDOM_NUMBER incorrect...\n'
            if '#define NUM_LIMIT 9973' not in data:
                outStr += 'NUM_LIMIT incorrect...\n'
            
            #Write to file if a case was tripped
            if len(outStr) > 0:
                plagirism = open('possible_plagirism.txt', 'w')
                plagirism.write(outStr)
                plagirism.close()           

        os.chdir('..')

def run_test_cases(test_cases):
    print('Running test cases...')
    for entry in os.listdir():
        if entry.startswith('.') or not os.path.isdir(entry):
            continue

        os.chdir('./' + entry)

        #If the compiled file exists run the test cases
        if os.path.exists('./MTFindProd'):
            outStr = ''     
            count = 1   
            for test in test_cases:
                print('Running test ' + test + ' on ' + entry + ' code...')
                errorFile = open('./error_file_' + str(count) + '.txt', 'w')
                outFile = open('./out_file_' + str(count) + '.txt', 'w')
                process = subprocess.Popen(test.split(' '), stderr=errorFile, stdout=outFile)

                #Try waiting for 5 seconds, if it expires kill the process and fail the test case
                try:
                    process.wait(5)
                except subprocess.TimeoutExpired:
                    process.kill()
                    errorFile.close()
                    outFile.close()
                    outStr += 'Test Case: ' + test + '\tTIMED OUT!!!\n'
                    os.remove('./out_file_' + str(count) + '.txt')
                    os.remove('./error_file_' + str(count) + '.txt')
                    count += 1
                    continue

                errorFile.close()
                outFile.close()

                #Determine if it passed or failed
                if os.stat('./out_file_' + str(count) + '.txt').st_size == 0:
                    os.remove('./out_file_' + str(count) + '.txt')
                    outStr += 'Test Case: ' + test + '\tNO OUTPUT!!!\n'
                elif os.stat('./error_file_' + str(count) + '.txt').st_size != 0:
                    outStr += 'Test Case: ' + test + '\tERROR!!!\n'
                else:
                    os.remove('./error_file_' + str(count) + '.txt')
                    outStr += 'Test Case: ' + test + '\tSuccess!!!\n'

                #Increment counter for file names
                count += 1


            #Write overall results
            resultFile = open('test_results.txt', 'w')
            resultFile.write(outStr)
            resultFile.close()

        os.chdir('..')

#DO THE THING!!!
test_cases = read_test_cases()
print('Test Cases: ' + str(test_cases))
sort_submissions()
rename_submissions()
detect_plagirism()
compile_submissions()
run_test_cases(test_cases)