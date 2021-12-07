import language_tool_python

def fix_grammer():
    global tool

    if not "tool" in globals():
        tool = language_tool_python.LanguageTool('en-US')

    text = "navigation could be better  but there is n't really anything the zen xtra can 't do once you 've gotten comfortable with it ."
    print(text)
    text = tool.correct(text)
    text = text.replace(" 't", "'t")
    print(text)
    return text

if __name__ == "__main__":
    fix_grammer()