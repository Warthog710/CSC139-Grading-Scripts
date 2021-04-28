# CSC139-Grading-Scripts
The grading scripts I used to grade CSC139 (Operating Systems) for Dr. Shobaki at Sacramento State University

#### Assignment 1
Used ``grading_asgm1.py`` to sort, rename, and compile all submission. The shell script ``grade_test_cases.sh`` (written by a previous grader that I do not know) was modified and used to work with my test cases. The last test case was manually ran on each submission.

#### Assignment 2
Used ``grading_asgm2.py`` to sort, rename, check for plagirism (needs to be updated each semester), compile, and run all test cases. All errors were recorded. Each student's report was then tested against the output of their code to produce verify functionality.

#### Assignment 3
Used ``grading_asgm3_sort_rename.py``, ``grading_asgm3_compile_validate.py``, and ``grading_asgm3_test_check.py`` in that order. Note, for the script to work each students program must accept an *input.txt* file in the directory it is running as well as produce an *output.txt* in that same directory. Once the assignment is sorted, compiled, and tested, a line by line analyse is performed on the output and a summary file is placed in their directory highlighting potential problem areas. Some <u>known bugs</u> are listed below:
 - If the rename function is called multiple times on the same directory unexpected results can occur.
 - If the students program is overly complicated (includes multiple files with headers) or is stored in a multi-level directory structure it may fail to properly compile. In this case the program should mark such students folders as *"manual"*. Either test these manually or change the structure into something suitable for the script.
 - If a students program expects input from a file not named *input.txt* (in the same directory, with exact naming) or fails to produce an *output.txt* (in the same directory, with exact naming) the script will fail to test properly, and produce unexpected results. Recommendation go through each students work and verify they are accepting input and producing output in this manner.

#### Plagirism Detection
Plagirism detection is difficult to write. In light of this, it may be nice to use something already made. Unfortunately I do not have the time to research, and use such a library but perhaps something like this would work? Maybe someone in the future can play around with this:
<a href="https://github.com/manuel-freire/ac2">AC2 Project</a>
