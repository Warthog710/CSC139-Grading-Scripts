import os
import subprocess
import shutil

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

def run_test_cases(test_cases):
    print('Running test cases...')


test_cases = read_test_cases()
print(test_cases)
sort_submissions()
rename_submissions()