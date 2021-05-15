import os
import subprocess

#? Due to the nature of this assignment, it is very unlikely that this will compile all students' work.
#? Manually compile such cases :(
def compile_submissions():
    print('Compiling submissions...')
    makeSubmissions = []

    #Perform a pass and search for makefiles
    for entry in os.listdir():
        #Ignore .vscode/.git folder and only look at directories
        if entry.startswith('.') or not os.path.isdir(entry):
            continue

        #Enter the directory
        os.chdir('./' + entry)

        #Loop through files in directory and compile saving errors
        for file in os.listdir(): 
            if 'makefile' in file or 'Makefile' in file:
                makeSubmissions.append(entry)
                error_file = open('make_errors.txt', 'w')
                subprocess.run(['make'], stderr=error_file, stdout=subprocess.DEVNULL)
                error_file.close()

                if os.stat('./make_errors.txt').st_size == 0:
                    os.remove('./make_errors.txt')

        os.chdir('..')

    print(f'Verify the following submissions contain a.out: {makeSubmissions}') 

    #Read through all directories and compile the students files
    for entry in os.listdir():
        #Ignore .vscode/.git folder and only look at directories and makefile submissions
        if entry.startswith('.') or not os.path.isdir(entry) or entry in makeSubmissions:
            continue

        #Enter the directory
        os.chdir('./' + entry)

        #Loop through files in directory and compile saving errors
        for file in os.listdir(): 

            #? C Programs
            if file.endswith('.c'):
                fileName = file.split('.')[0]
                fileName = f'./{fileName}_errors.txt'
                error_file = open(fileName, 'w')
                subprocess.run(['gcc', '-w', f'./{file}'], stderr=error_file)
                error_file.close()

                if os.stat(fileName).st_size == 0:
                    os.remove(fileName)

            #? C++ Programs
            if file.endswith('.cpp'):
                fileName = file.split('.')[0]
                fileName = f'./{fileName}_errors.txt'
                error_file = open(fileName, 'w')
                subprocess.run(['g++', '-w', f'./{file}'], stderr=error_file)
                error_file.close()

                if os.stat(fileName).st_size == 0:
                    os.remove(fileName)

            #? Java Programs
            if file.endswith('.java'):
                fileName = file.split('.')[0]
                fileName = f'./{fileName}_errors.txt'
                error_file = open(fileName, 'w')
                subprocess.run(['javac', '-Xlint:unchecked', f'./{file}'], stderr=error_file)
                error_file.close()

                if os.stat(fileName).st_size == 0:
                    os.remove(fileName)

        
        #Go back to previous directory
        os.chdir('..')   

#? Marks a students folder with 'MANUAL' if compiliation failed or some other error occured (folders in their directory)
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

compile_submissions()
validate_submissions()
