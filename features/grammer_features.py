import language_tool_python
import io
import contractions


# Yes Thorge really just misspelled the word "grammar" without intention. So we'll keep it like this lol
def fix_grammer(inputtext):
    global tool

    if not "tool" in globals():
        tool = language_tool_python.LanguageTool('en-US')


    text = inputtext

    write = text + "\n"

    text = tool.correct(text).lower()

    text = text.replace(" 't", "'t")

    expanded_words = []

    for word in text.split():
        expanded_words.append(contractions.fix(word))

    text = ' '.join(expanded_words)
    write += text + "\n\n"

    return text, write


def bad_grammer(inputtext):
    global tool

    if not "tool" in globals():
        tool = language_tool_python.LanguageTool('en-US')

    text = inputtext
    matches = tool.check(text)
    matches = [rule for rule in matches if not is_bad_rule(rule)]
    return_dict = {
        'values': [ len(text)/(len(matches) + 1) ],
        'heads': ['@Attribute bad_grammer_ratio REAL']}
    return return_dict


def is_bad_rule(rule):
    if rule.ruleId == "UPPERCASE_SENTENCE_START":
        return True

    if rule.ruleId == "I_LOWERCASE":
        return True

    return False