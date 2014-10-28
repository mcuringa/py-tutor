# tutor.py
# by: mxc
"""
Tutor is a simple, command-line, Computer Based Instruction for
teaching Python.
"""

__author__ = 'mxc'

levelMap = {}
# variables and functions
levelMap[1] = "function basics"
levelMap[1.1] = "variables"
levelMap[1.2] = "type"
levelMap[1.3] = "assignment"
levelMap[1.4] = "simple return"
levelMap[1.5] = "simple parameter"
levelMap[1.6] = "multiple parameters"
levelMap[1.7] = "math"
levelMap[1.8] = "mod"
levelMap[1.9] = "floor"

# conditions
levelMap[2.1] = "if"
levelMap[2.2] = "else"
levelMap[2.3] = "elif"
levelMap[2.4] = "multiple conditions"
levelMap[2.5] = "=="
levelMap[2.6] = ">"
levelMap[2.7] = "<"

# strings




class Question(object):

    success = "You are correct."
    fail = "Your answer did not match the expected response."
    idCount = 1

    def __init__(self, prompt, result, levels=(1,), params=(), hint=""):
        self.prompt = prompt
        self.result = result
        self.params = params
        self.hint = hint
        self.levels = levels
        self.id = Question.idCount
        Question.idCount += 1

    def check(self, response):
        f = eval(response)
        result = f(self.params)
        if result == self.result:
            return (True, Question.success)
        return (False, Question.fail)


