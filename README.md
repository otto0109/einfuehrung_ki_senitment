# AI sentiment analysis on reviews
## Sentimentanalyse ist heute das Thema!
The AI **classifies reviews by positive & negative**. Current **correct classification: ~86% in the training data** 
and **90% in the test data**. That's pretty nice.

## Installation (run.bat also installs needed packages on Windows):
* **Python 3.9** (**add to PATH** on installation. Works the best via Microsoft Store actually...)
*  [**C++ Build Tools**](https://visualstudio.microsoft.com/de/visual-cpp-build-tools/)
* **VaderSentiment**: `pip install vaderSentiment`
* **Language Tool Python**: `pip install language_tool_python`
* **Spacy**:
```python
pip install -U pip setuptools wheel
pip install -U spacy
python -m spacy download en_core_web_sm
```
* **More Packages**:
```python
pip install --user -U nltk
pip install --user -U numpy
python -m nltk.downloader popular
pip install -U pywsd
pip install -U wn==0.0.22
```
* **Contractions**: `pip install contractions`
* Afinn: `pip install afinn` (**Optional**, because not used currently)


##How to Run
### 1. Change the basePath in `modular_arff_builder.py` to the Path of your project. (Config files would be way to easy)
###2. Run `run.bat` on Windows.
(Models for training and testing will be generated and packages are being installed)
### 2. OR Run`python modular_arff_builder.py`
### 3. Then open the generated .arff file in Explorer in [Weka 3](https://www.cs.waikato.ac.nz/ml/weka/).


##Troubleshoot
### Cacheing
**When the data or preprocessing changes,** you should **delete `grammer_cache.txt` and `grammer_cache_test.txt`**
###ModuleNotFoundError: No module named 'language_tool_python'
Go to Settings -> Project -> Python Intepreter -> +

##More
### Check out our [video](http://tiny.cc/sentiment_analysis) explaining every feature