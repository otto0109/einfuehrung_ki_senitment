# Die Super_duper_ki
## Was ist die super duper KI?
Die KI **clustert Reviews nach positiv & negativ**. Aktuelle **korrekte Zuordnung: ~81%**. Das ist schon ziemlich super duper.

## Benötigt wird:
* **Python 3.9** (beim Installieren **in PATH hinzufügen einhaken**)
* **VaderSentiment**: `pip install vaderSentiment`
* **Language Tool Python¹** (um Grammatik zu fixen): `pip install language_tool_python` und `spacy download en_core_web_sm`
* Afinn: `pip install afinn` (**Optional**, da aktuell unbenutzt)

### Zum Generieren `py modular_arff_builder.py` ausführen (dann in WeKa öffnen)

(¹ Falls `ModuleNotFoundError: No module named 'language_tool_python' auftritt
in PyCharm über Settings -> Project -> Python Intepreter -> + Hinzufügen)