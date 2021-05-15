import os
import shutil
import zipfile

def sort_submissions():
    print('Sorting submissions...')

    for entry in os.listdir():
        #Ignore directories and .py files
        if os.path.isdir(entry) or entry.endswith('.py'):
            continue

        #Get the student name
        student_name = entry.split('_')[0]

        if 'LATE' in entry:
            student_name += ' (LATE)'

        #Make the directory if not alread created
        if not os.path.exists('./' + student_name):
            os.mkdir('./' + student_name)

        #Move the file into the students directory
        shutil.move('./' + entry, './' + student_name)

def rename_submissions():
    print('Renaming submissions...')

    for entry in os.listdir():
        #Ignore .vscode/.git folder and only look at directories
        if entry.startswith('.') or not os.path.isdir(entry) or 'test_cases' in entry:
            continue

        #Enter the directory
        os.chdir('./' + entry)

        #Loop through files in directory extract files
        for file in os.listdir():
            #If the file is a zip file, extract it
            if file.endswith('.zip'):
                with zipfile.ZipFile(file, 'r') as zip_ref:
                    zip_ref.extractall('./')
                    os.remove(file)

                    #Find the recently extracted directory and move everything up a level
                    for file in os.listdir():
                        if os.path.isdir(file):
                            os.chdir('./' + file)

                            #Move the files up
                            for item in os.listdir():
                                try:
                                    shutil.move(item, '../' + item)
                                except Exception:
                                    pass

                            os.chdir('..')
                            os.rmdir(file)
        
        os.chdir('..')

        #Loop through the files again and rename
        for entry in os.listdir():
            #Ignore .vscode/.git folder and only look at directories
            if entry.startswith('.') or not os.path.isdir(entry) or 'test_cases' in entry:
                continue

            #Enter the directory
            os.chdir('./' + entry)

            for file in os.listdir():
                student = entry.replace('(LATE)', '').strip()

                #If the file contains the directory name, rename it
                if student in file:
                    #If the file is a C, C++, or just plain .java
                    if file.endswith('.c') or file.endswith('.cpp') or file.endswith('.java'):
                        os.rename(file, file.split('_')[len(file.split('_')) - 1])

            #Return to previous directory
            os.chdir('..')

        #Go through and read the java files, rename to their class name to prevent errors
        for entry in os.listdir():
            #Ignore .vscode/.git folder and only look at directories
            if entry.startswith('.') or not os.path.isdir(entry) or 'test_cases' in entry:
                continue

            #Enter the directory
            os.chdir('./' + entry)

            for file in os.listdir():
                if file.endswith('.java'):
                    codeFile = open(file, 'r')
                    
                    for line in codeFile:
                        if 'public class' in line:
                            newName = line.split(' ')[2].replace('{', '').strip()
                            break
                        elif 'public abstract class' in line:
                            newName = line.split(' ')[3].replace('{', '').strip()
                            break

                    #Close the file
                    codeFile.close()

                    #Rename the file
                    os.rename(file, newName + '.java')

            #Go back to previous directory
            os.chdir('..')

sort_submissions()
rename_submissions()
