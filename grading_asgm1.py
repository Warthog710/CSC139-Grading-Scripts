import os
import subprocess
import shutil
import time

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
        #Ignore directories and files that don't end with .c
        if os.path.isdir(entry) or not entry.endswith('.c'):
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
            #If file contains producer and ends with .c rename it
            if 'producer' in file and file.endswith('.c'):
                os.rename(file, 'producer.c')

            #Else if file contains consumer and ends with .c rename it
            elif 'consumer' in file and file.endswith('.c'):
                os.rename(file, 'consumer.c')

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
            if 'producer.c' in file:
                error_file = open('./producer_compiler_errors.txt', 'w')
                subprocess.run(['gcc', './producer.c', '-lrt', '-w', '-o', 'producer'], stderr=error_file)
                error_file.close()

                #If the error file is size == 0, remove it as no errors occured
                if os.stat('./producer_compiler_errors.txt').st_size == 0:
                    os.remove('./producer_compiler_errors.txt')

            #Compile the consumer, ignoring warnings, saving any errors (if any)
            elif 'consumer.c' in file:
                error_file = open('./consumer_compiler_errors.txt', 'w')
                subprocess.run(['gcc', './consumer.c', '-lrt', '-w', '-o', 'consumer'], stderr=error_file)
                error_file.close()

                #If the error file is size == 0, remove it as no errors occured
                if os.stat('./consumer_compiler_errors.txt').st_size == 0:
                    os.remove('./consumer_compiler_errors.txt')

        #Go back a directory
        os.chdir('..')

#? Function needs a lot more work before it ready, just using this script to organize and compile submissions.
def run_test_cases(test_cases):
    print('Running test cases...')

    #Read through all directories and run the test cases on the students files
    for entry in os.listdir():
        #Ignore .vscode/.git folder and only look at directories
        if entry.startswith('.') or not os.path.isdir(entry):
            continue

        #Enter the directory
        os.chdir('./' + entry)

        #Only run if the file exists
        if os.path.exists('./producer'):
            #Run all the test cases
            count = 1
            summary = ''

            #Move test case 1 script in and run
            shutil.move('../grade_case1.sh', './')
            time.sleep(1)
            testPipe = subprocess.Popen('./grade_case1.sh', shell=True)
            shutil.move('./grade_case1.sh', '../grade_case1.sh')
            #print(testPipe.communicate())             

        #Go back a directory
        os.chdir('..')    
        time.sleep(1)      


#test_cases = read_test_cases()
#print(test_cases)
sort_submissions()
rename_submissions()
compile_submissions()