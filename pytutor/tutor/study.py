import random
import json
from operator import itemgetter

from tutor.templatetags.tutor_extras import syn
from tutor.models import *

def correct_at_levels(student, last=20):

    correct = Response.objects.filter(user=student, is_correct=True)[:last]
    levels = [0 for i in range(len(Question.levels))]
    for r in correct:
        i = r.question.level -1
        levels[i] += 1
    levels = [(count, i) for count, i in enumerate(levels, start=1)]

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
    total = sum([count for level, count in levels])
    level = levels[0][0]

    level_up = sum([c for l, c in levels if l >= level])
    if level_up > total /2:
        return min(level + 1, len(Question.levels))
    return level

def next_tag_question(level, pool, tag):
    pool = pool.filter(tags__icontains=tag)
    level_choice = random_level(level)
    
    if pool.filter(level=level_choice) > 0:
        return random.choice(pool.filter(level=level_choice))
    
    if pool.filter(level=level) > 0:
        return random.choice(pool.filter(level=level))

    if pool.filter(level=level-1) > 0:
        return random.choice(pool.filter(level=level-1))

    if pool.filter(level=level+1) > 0:
        return random.choice(pool.filter(level=level+1))

    return random.choice(pool)


def next_question(student, tag=""):
    level = current_level(student)
    last2 = Response.objects.filter(user=student).order_by("-submitted").values_list("question").distinct()[:2]
    pool = Question.objects.filter(status=Question.ACTIVE)
    lastids = [q[0] for q in last2]
    pool = pool.exclude(id__in=lastids)

    if len(tag) > 0:
        return next_tag_question(pool, tag)

    level_choice = random_level(level)
    questions = pool.filter(level=level_choice)

    return random.choice(questions)

