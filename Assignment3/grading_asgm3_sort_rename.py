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

#? Running this function more than once can produce unexpected results.
#? If a students submission is zipped, this functin can unzip it and bring its contents up a directory... 
#? Don't run this multiple times on the same directory
def rename_submissions():
    print('Renaming submissions...')   

    #Read through all directories and rename the students files
    for entry in os.listdir():
        #Ignore .vscode/.git folder and only look at directories
        if entry.startswith('.') or not os.path.isdir(entry) or 'test_cases' in entry:
            continue

        #Enter the directory
        os.chdir('./' + entry)

        #Loop through files in directory and rename
        for file in os.listdir():
            #If the file is a zip file, extract it
            if file.endswith('.zip'):
                with zipfile.ZipFile(file, 'r') as zip_ref:
                    zip_ref.extractall('./')
                    os.remove(file)

            #If the file is a C, C++, or just plain .java
            if file.endswith('.c') or file.endswith('.cpp') or file.endswith('.java'):
                os.rename(file, file.split('_')[len(file.split('_')) - 1])

        #Go back a directory
        os.chdir('..')

    # Perform a second pass, moving the files inside unzipped folders out
    for entry in os.listdir():
        #Ignore .vscode/.git folder and only look at directories
        if entry.startswith('.') or not os.path.isdir(entry):
            continue

        #Enter the directory
        os.chdir('./' + entry)

        #Loop through files in directory and rename
        for file in os.listdir():
            #If the file is a directory, move its contents out...
            if os.path.isdir(file):

                os.chdir('./' + file)
                for item in os.listdir():
                    #Ignoring errors
                    try:
                        shutil.move(item, '../' + item)
                    except Exception:
                        pass

                os.chdir('..')

                #Remove the directory
                os.rmdir(file)
        os.chdir('..')

# Do the thing!
sort_submissions()
rename_submissions()