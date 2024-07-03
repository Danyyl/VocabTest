# VocabTest

Desktop application on PyQt5 for VocabTest

# Structure of the project

*.py files - files with code
requirements.txt - file to install all requirements
data - folder with data
    in this folder files with languages and words.
    name of the file {name_of_language}.csv
    and words inside
    if you want to add new language 
    just add file with a new language
result - folder with a results, that create in app working process
    every folder inside with a name {name}-{datetime.now().isoformat()}
    and folder with images, that generated from the file with words
    and result file data.csv with columns
    hash,stimuli,correct_answer,real_answer,language


# Run a program

install all requirements
create virtual environment on your computer with python (10+)
install all requirements like pip install -r requirements.txt
to run app - "python app.py" in root folder

Also you can configure number of test steps.
You should change const NUM_OF_WORDS in main.py file
