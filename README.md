# Die Super_duper_ki
## Was ist die super duper KI?
Die KI **clustert Reviews nach positiv & negativ**. Aktuelle **korrekte Zuordnung: ~81%**. Das ist schon ziemlich super duper.

## Benötigt wird:
* **Python 3.9** (beim Installieren **in PATH hinzufügen einhaken**. Am besten über Microsoft Store installieren.)
* **VaderSentiment**: `pip install vaderSentiment`
* **Language Tool Python**: `pip install language_tool_python`
* **Spacy**:
```python
pip install -U pip setuptools wheel
pip install -U spacy
python -m spacy download en_core_web_sm
```
* Weitere Packages:
```python
pip install --user -U nltk
pip install --user -U numpy
python -m nltk.downloader 'popular'
pip install -U pywsd
pip install -U wn==0.0.22
```
* Afinn: `pip install afinn` (**Optional**, da aktuell unbenutzt)

### Zum Generieren `python modular_arff_builder.py` ausführen (dann in WeKa öffnen)

(Falls `ModuleNotFoundError`: No module named 'language_tool_python' auftritt
in PyCharm über Settings -> Project -> Python Intepreter -> + Hinzufügen)