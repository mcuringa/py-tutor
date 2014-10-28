__author__ = 'mxc'

from tutor import Question

t = []

def parse_prompt(text):
    prompt = text.replace("\\:",":")
    return prompt.strip()

def parse_result(s):
    return eval(s)

def parse_question(text):
    parts = text.split(":")
    if len(parts) % 2 != 0:
        raise Exception("Every key must have a value")

    q = Question()

    for i in range(1,len(parts),2):
        key = parts[i-1].trim()
        value = parts[i]


        if key == "result":
            q.result = parse_result(value)
        elif key == "prompt":
            q.prompt = parse_prompt(value)

    return q





Question("""
Write a function "always_true" which takes no parameters
and always returns the boolean value True.""", True),

Question("""
Write a function `plus_10(n)` which returns a number equal to n + 10""", True),
Question("""
Write a function "always_true" which takes no parameters
and always returns the boolean value True.""", True),
