@ECHO OFF
ECHO delete old data
rmdir /s /q generated

ECHO create directories
mkdir generated
cd generated
mkdir test
cd ..

:start
SET choice=
SET /p choice=Do you want to install all dependencies? [y,N]:
IF NOT '%choice%'=='' SET choice=%choice:~0,1%
IF '%choice%'=='Y' GOTO yes
IF '%choice%'=='y' GOTO yes
IF '%choice%'=='N' GOTO no
IF '%choice%'=='n' GOTO no
IF '%choice%'=='' GOTO no
ECHO "%choice%" is not valid
ECHO.
GOTO start


:yes
pip install vaderSentiment
pip install language_tool_python
pip install -U pip setuptools wheel
pip install -U spacy
python -m spacy download en_core_web_sm
pip install --user -U nltk
pip install --user -U numpy
pip install -U pywsd
pip install -U wn==0.0.22
pip install afinn
pip install contractions
python -m nltk.downloader popular
GOTO no

:no
python ./modular_arff_builder.py

