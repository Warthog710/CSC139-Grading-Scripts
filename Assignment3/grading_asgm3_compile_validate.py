import os
import subprocess

#? Due to the nature of this assignment, it is very unlikely that this will compile all students' work.
#? Manually compile such cases :(
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

            #? C programs
            if file.endswith('.c'):
                fileName = file.split('.')[0]
                fileName = f'./{fileName}_errors.txt'
                error_file = open(fileName, 'w')
                subprocess.run(['gcc', '-w', f'./{file}'], stderr=error_file)
                error_file.close()

                if os.stat(fileName).st_size == 0:
                    os.remove(fileName)

            #? C++ programs
            if file.endswith('.cpp'):
                fileName = file.split('.')[0]
                fileName = f'./{fileName}_errors.txt'
                error_file = open(fileName, 'w')
                subprocess.run(['g++', '-w', f'./{file}'], stderr=error_file)
                error_file.close()

                if os.stat(fileName).st_size == 0:
                    os.remove(fileName)

            #? Java programs
            if file.endswith('.java'):
                fileName = file.split('.')[0]
                fileName = f'./{fileName}_errors.txt'
                error_file = open(fileName, 'w')
                subprocess.run(['javac', f'./{file}'], stderr=error_file)
                error_file.close()

                if os.stat(fileName).st_size == 0:
                    os.remove(fileName)           

        #Go back a directory
        os.chdir('..')

# This function reads through the directory structure and determines if test cases can be ran automatically
def validate_submissions():
    print('Validating submissions...')

    for entry in os.listdir():
        # Ignore .vscode/.git folder and only look at directories
        if entry.startswith('.') or not os.path.isdir(entry):
            continue

        # If MANUAL is in the name... skip it
        if 'MANUAL' in entry:
            continue

        #Enter the directory
        os.chdir('./' + entry)

        # Loop through the files in the directory, if it contains another directory or errors mark it as untestable
        for file in os.listdir():
            if os.path.isdir(file):
                os.rename('../' + entry, '../' + entry + ' MANUAL')
                break
            elif 'errors' in file:
                os.rename('../' + entry, '../' + entry + ' MANUAL')
                break

        os.chdir('..')

# Do the thing!
compile_submissions()
validate_submissions()