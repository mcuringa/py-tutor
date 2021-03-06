import random
import json
from operator import itemgetter

from tutor.templatetags.tutor_extras import syn
from tutor.models import *

def correct_at_levels(student, last=20):

    # all correct responses in last 20
    correct = Response.objects.filter(user=student, is_correct=True)[:last]
    
    # init an empty list to hold the count at each level
    levels = [0 for i in range(len(Question.levels))]
    
    #count up the levels
    for r in correct:
        i = r.question.level -1
        levels[i] += 1
    
    # convert our list to a list of tuples in format (<level>, <count>)
    levels = [(count, i) for count, i in enumerate(levels, start=1)]

    # sort it twice, so that lower levels are first, if tied by count
    level_sorted = sorted(levels) #ascending by level
    return sorted(levels, key=itemgetter(1), reverse=True) # descending by correct count

def random_level(level):
    c = random.randint(1, 5)
    if c < 4:
        return level
    if c == 4:
        return max(level - 1, 1)
    
    max_level = len(Question.levels)
    return min(level + 1, max_level)

def current_level(student):
    levels = correct_at_levels(student)
    total_correct = sum([count for level, count in levels])
    
    # current leve is first item in level list
    level = levels[0][0]

    #[(5,2),(6,2),(4,1),(3,1),(2,1),(1,0)...]
    # how many correct answers do they have at or above the current level?
    correct_at_or_above_current_level = sum([c for l, c in levels if l >= level])
    
    # if they got > 50% right at current level, bump them up
    if correct_at_or_above_current_level > total_correct /2:
        return min(level + 1, len(Question.levels))
    return level

def next_tag_question(level, pool, tag):
    pool = pool.filter(tags__icontains=tag)

    level_choice = random_level(level)
    
    if pool.filter(level=level_choice).count() > 0:
        return random.choice(pool.filter(level=level_choice))
    
    if pool.filter(level=level).count() > 0:
        return random.choice(pool.filter(level=level))


    if pool.filter(level=level-1).count() > 0:
        return random.choice(pool.filter(level=max(level-1,1)))


    if pool.filter(level=level+1).count() > 0:
        return random.choice(pool.filter(level=min(level+1,len(Question.levels)+1)))

    # reload the pool, with the excluded IDs, this is only the case if a pool has 2 or fewer questions
    if pool.count() == 0:
        pool = Question.objects.filter(status=Question.ACTIVE)
        pool = pool.filter(tags__icontains=tag)
        
        if pool.count() == 0:
            raise ValueError("No questions in tagged pool: " + tag); # this shouldn't happen except in very odd cases
    
    return random.choice(pool)


def next_question(student, tag=""):
    level = current_level(student)
    last2 = Response.objects.filter(user=student).order_by("-submitted").values_list("question").distinct()[:2]
    pool = Question.objects.filter(status=Question.ACTIVE)
    lastids = [q[0] for q in last2]
    if pool.count() > 2:
        pool = pool.exclude(id__in=lastids)

    if len(tag) > 0:
        nextq = next_tag_question(level, pool, tag)
        return nextq

    level_choice = random_level(level)
    questions = pool.filter(level=level_choice)
    try:
        q = random.choice(questions)
    except IndexError:
        raise IndexError('No question at {} for user {}'.format(level_choice, student.username))

    return q

