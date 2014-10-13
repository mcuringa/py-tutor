import random
import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.contrib import messages

from tutor.models import *

@login_required
def study(request, try_again_id=0, study_tag=None):
    """Randomly choose the next question for the user to study.
       If no questions exist, prompt the user to create one."""


    if request.method == "POST":
        respond(request)
    
    questions = Question.objects.all()
    if not questions:
        context = {"questions" : False}
    else:
        if try_again_id > 0:
            question = Question.objects.get(pk=try_again_id)  # everything above and including this line, Matt did.
            response_form = ResponseForm.objects.get(study_tag = study_tag)
            # This was my attemt to accomplish #2 ^--

        elif study_tag is not None:
            print ('the study tag is:', study_tag)
            questions = Question.objects.get(study_tag= study_tag) # should we be saying questions or question for this variable?
            # Now I sort of think I should put a 'context' right here,
            # here I'm trying to say, questions = only questions that have the same tag
            # ^ is that the same as '#1 looking up a random question with the tag?' <-- I feel like I'm missing choice.random somewhere in here.

            # v v v then, serve from only these questions (stay in the same study_tag group.)
            # I'm trying to do #1 and

            # for tag in Tag.objects.all().fliter(study_tag= str(study_tag))
            # Example for #5??  6 ^-> for test in Test.objects.all().filter(question=pk):

            questions = serve_question(request.user)#.choice.random < or something?

#-------------List of Things I Need To Do -----------------------

            #1. look up a random question with the tag
            #2. change the form, so that when they go to the next question,  <---------- I think I don't know what 'change the form' means here.
                                                                                        # what is the response form / question form? the page that shows up with questions, and reponse listings?
            # if they're studying wihtin a tag, they stay in the tag
            #3. for try again, if they're studying with a tag, they need to stay within the tag.

            # v do these first v
            #4. make sure that the tags get saved and work 
            #5. filter (look up tag as a string saved with question)

        else:
            question = serve_question(request.user)
            

        response_form = ResponseForm()
        try:
            response = Response.objects.get(user=request.user, question=question)
            attempt = response.attempt + 1
        except: 
            attempt = 1
        context = {
            "question": question, 
            "response_form" : response_form, 
            "questions" : True,
            "attempt" : attempt
        }
    
    return render(request, 'tutor/respond.html', context)

@login_required
def no_questions(request):
    return render(request, 'tutor/no_questions.html')

@login_required
def respond(request):
    """Allow user to write a response to a question."""
    
    print("respond called")

    pk = int(request.POST["qpk"])
    user_code = request.POST.get('user_code', False);
    print(request.POST)
    print(user_code)
    # printing whatever was typed into the box as string

    #responses are linked to ArchiveQuestions, but we're given a Question key
    question = Question.objects.get(pk=pk)  
    
    try:
        attempts = Response.objects.all().filter(user=request.user, question=question)
    except: 
        attempts = []
    
    response = Response(attempt=len(attempts) + 1, user=request.user, question=question)
    response.code = user_code

    #evaluate user's code
    response.is_correct = True
    testResults = []
    for test in Test.objects.all().filter(question=pk):
        ex, success = test.evaluate(user_code)
        response.is_correct = success
        testResults.append((test, success))


        ## Answer the question, and keep refreshing to see if it's working.

    context = {"question" : question, 
               "response" : response, 
               "previous_attempt" : response.attempt - 1,
               "testResults" : testResults }
               ## Here, make it so it formats the user's code with the assert statements from the 
               ## Question (question.tests) --
               ## change the output here in context and in response_correct.html

    # response.is_correct = len(testResults) == 0
    response.save()
    
    return render(request, 'tutor/response_result.html', context)

def list(request):
    """List the questions in the database"""
    
    questions = Question.objects.all()
    context = {"questions": questions}

    
    return render(request, 'tutor/list.html', context)

@login_required
def question_form(request, pk=0):
    
    if pk == 0:
        form = QuestionForm()
        history = []
        test_results = []
    else:

        question = Question.objects.get(pk=pk)        
        form = QuestionForm(instance=question)
        #form.id_comment = "" #this doesn't actually clear the field
        history = ArchiveQuestion.objects.all().filter(parent_id=pk)
        tests = Test.objects.all().filter(question=question)
        test_results = {}
        if tests.count() == 0:
            messages.add_message(request, messages.INFO, 'This question has no unit tests. Without unit tests, a response to this question won\'t be properly evaluated. Create a unit test below!')
        else:
            for test in tests:
                print(test.to_code())
                r = test.evaluate()

                if r[1] == False:
                    messages.add_message(request, messages.INFO, 'Test ' + str(test.to_code()) + ' failed on Solution code. Check this test case and your solution code to fix the issue.')
                    result = "Test failed on 'Solution' code."
                    passed = False
                else:
                    result = "Test passed on 'Solution' code!"
                    passed = True
                test_results[test.pk] = (test.to_code(), result, passed)

    test_form = TestForm()

    context = { "question": form,
                "pk": pk,
                "history": history,
                "test_form": test_form,
                "tests": test_results
              }

    return render(request, 'tutor/question_form.html', context)

@login_required
def save_question(request):

    print('saving a question...')
    pk = int(request.POST["pk"])
    if pk > 0:
        q = Question.objects.get(pk=pk)
        form = QuestionForm(request.POST, instance=q)
        form.instance.version += 1
    else:
        form = QuestionForm(request.POST)
        form.instance.version = 1
        form.instance.creator = request.user

    form.instance.modifier = request.user
    try:
      question = form.save()
      archive(question)
      url = "/tutor/" + str(question.id) + "/edit"
    except:
        messages.add_message(request, messages.INFO, 'Please fill out all required fields.')
        url = "/tutor/new"


    return HttpResponseRedirect(url)

## I have no idea how to save the tags.  This is a guess.
@login_required
def save_tags(request):
    print('saving tags...')
    question = Question.objects.get(pk=pk)
    tags = Tags.objects.all().filter(question=question)
    print (tags)
    return HttpResponseRedirect(url)

#using this as how to save tag, use tag.
# @login_required
# def save_question(request):

#     print('saving a question...')
#     pk = int(request.POST["pk"])
#     if pk > 0:
#         q = Question.objects.get(pk=pk)
#         form = QuestionForm(request.POST, instance=q)
#         form.instance.version += 1
#     else:
#         form = QuestionForm(request.POST)
#         form.instance.version = 1
#         form.instance.creator = request.user

#     form.instance.modifier = request.user
#     try:
#       question = form.save()
#       archive(question)
#       url = "/tutor/" + str(question.id) + "/edit"
#     except:
#         messages.add_message(request, messages.INFO, 'Please fill out all required fields.')
#         url = "/tutor/new"


#     return HttpResponseRedirect(url)
@login_required
def delete_question(request, pk):
    """Deletes the selected question and all related ArchiveQuestions."""

    question = Question.objects.get(pk=pk)
    archives = ArchiveQuestion.objects.all().filter(parent_id=pk)
    for q in archives:
        q.delete()
    question.delete()
    return HttpResponseRedirect("/tutor/list")

def archive(question):
    aq = ArchiveQuestion()
    aq.archive(question)
    aq.modifier = question.modifier
    aq.save()

@login_required
def add_test(request):
    questionId = int(request.POST["question_id"])
    q = Question.objects.get(pk=questionId)
    form = TestForm(request.POST)
    form.instance.question = q
    try:
        test = form.save()
        success = True

    except:
        message = "Tests require arguments, expected results, and a fail message."
        success = False
        passed = False
        list_append = ""

    if success:
        message = ""
        user_function = test.question.solution
        result = test.evaluate(user_function)
        if result[1]:
            #this test passed
            passed = True
            list_append = "<li class=\"bg-success\">" + test.to_code() + "<br>Result: Test passed on 'Solution' code!<br>" + "<a href=\"/tutor/test/" + str(test.id) + "/del\" alt=\"Delete this test\">x</li>"
        else:
            #this test didn't
            passed = False
            list_append = "<li class=\"bg-danger\">" + test.to_code() + "<br>Result: Test failed on 'Solution' code.<br>" + "<a href=\"/tutor/test/" + str(test.id) + "/del\" alt=\"Delete this test\">x</li>"
    data = {
        "success": success,
        "message": message,
        "list_append": list_append,
        "passed": passed,
        "assert_code": test.to_code()
    }
    # json = serializers.serialize("json", [test])
    # # return a sustring because djano only works with
    # # iterables, but we just want a single json object
    # data = json[1:-1]

    return HttpResponse(json.dumps(data), content_type="application/json")

@login_required
def del_test(request, pk):
    test = Test.objects.get(pk=pk)
    question = test.question
    test.delete()
    messages.add_message(request, messages.INFO, "Test successfully deleted.")
    url = "/tutor/" + str(question.id) + "/edit"
    return HttpResponseRedirect(url)

def serve_question(user):
    """Serves a user the next applicable question."""
    #get history of user's correct and incorrect responses
    # correct_responses = Response.objects.all().filter(user=user, is_correct=True)
    # incorrect_responses = Response.objects.all().filter(user=user, is_correct=False)

    questions = Question.objects.all().filter()
    next_q = random.choice(questions)
    return next_q


# @login_required

# --> it looke like del_test is separate from the del_question function
# will my duplicate have to follow the same form?


# @login_required
# def delete_question(request, pk):
#     """Deletes the selected question and all related ArchiveQuestions."""

#     question = Question.objects.get(pk=pk)
#     archives = ArchiveQuestion.objects.all().filter(parent_id=pk)
#     for q in archives:
#         q.delete()
#     question.delete()
#     return HttpResponseRedirect("/tutor/list")
def dup(request, pk=0):
    new_q = Question.objects.get(pk=pk)
    tests = Test.objects.all().filter(question=new_q)
    new_q.pk = None
    new_q.creator = request.user
    new_q.modifier = request.user
    new_q.save()

    for t in tests:
        t.pk = None
        t.question = new_q
        t.save()



# look up all associated test qs
# set all test qs  - assign them into variable associated with question
# we need to reset "creator" manually to be the current user (or "modifier")


    messages.add_message(request, messages.INFO, "Test successfully duplicated.")
    url = "/tutor/" + str(new_q.id) + "/edit"

    return HttpResponseRedirect("/tutor/list")


# def dupTests(request, pk=0):
#     test = Test.objects.get(pk=pk)
#     question = test.question
#     test.save()

#     print (test)

#     test.pk = None
#     test.save()

#     dupTest = test
#     return HttpResponse(url)


# Now I want to make it so that the name changes to (function_name_duplicate1)

# printing (dup_q.test) gave an error, so I htink I have to make a new 
# function for tests.
# here's the modle I think I should follow for tests  (although maybe not, this could
    #just be the 'x' button on "existing tests boxes. ")


    ## Is question tied to test?

    ## do a print statement on source_q, and see if there's any tests in there.

    #     for source_test in source_q:
    #         dup_test.append(source_test)
    # duplicate_q = 


    # context = {"questions": questions}
    
    # return render(request, 'tutor/list.html', context)

    # django model copy / deep copy (<-- new copy for all archived *  nevermind)



    # change primary key to zero, then create archive qs and make them an empty list. 
    #aquestions = []
    # the look up all the tests that are part of source_q, for each one, 
    #create a new test, and add it to your duplicate q
    # create empty dup question, get the id, and then save all 
    #the test to the database as you go.


    #look up question we want to dup using pk

    #copy it? give it new id?

    #save the new object

    #copy all the tests, too

    #now redirect back to the list














    #get the questions associated with those responses
    # correct_questions = []
    # for response in correct_responses:
    #     correct_questions.extend(Question.objects.all().filter(id=response.question.parent_id).latest("created"))
    # incorrect_questions = []
    # for response in incorrect_responses:
    #     incorrect_questions.extend(Question.objects.all().filter(id=response.question.parent_id).latest("created"))
    
    #now find:
    #highest level at which user has correctly answered a question
    #highest level at which user has incorrectly answered a question
    #lowest level at which user has incorrectly answered a question
    # highest_correct_level = 1
    # for question in correct_questions.values:
    #     if question.level > highest_correct_level:
    #         highest_correct_level = question.level

    # highest_incorrect_level = 1
    # lowest_incorrect_level = 10
    # for question in incorrect_questions.values:
    #     if question.level > highest_incorrect_level:
    #         highest_incorrect_level = question.level
    #     if question.level < lowest_incorrect_level:
    #         lowest_incorrect_level = question.level

    #now calculate based on these numbers
    #main focus is current level (highest_correct_level.
    #count questions at highest current level
    #if count > 5 and level < 10, move the user to the next level
    #if count > 5 and level = 10, give the user a random question from level 5 - 10.

    #otherwise, pick a random floating point number from 0 to 1.
    #if highest and lowest incorrect levels are the same:
    #   if that number is not the current level:
    #       if num <= 0.6, give user a random unanswered or incorrect question from this level
    #       if 0.6 < num <= 0.9, give user a random unanswered or incorrect question from highest/lowest incorrect level
    #       if 0.9 < num <= 1.0, give user a random unanswered question w/level between current and the high/low level
    #   if that number is the current level
    #       if num <= 0.8, give user a random unanswered or incorrect question from this level
    #       if 0.8 < num <=  1.0, give user a random unanswered or incorrect question from
    #                            a level 1 or 2 less than the current one.

    #if highest and lowest incorrect levels are different:
    #   if num <= 0.6, give user a random unanswered or incorrect question from this level
    #   if 0.6 < num <= 1.0, give user a random unanswered or incorrect question from
    #                        a level less than this one, but not below the lowest incorrect level.


    #dummy for debugging
    questions = Question.objects.all()
    best_question = random.choice(questions)

    return best_question
