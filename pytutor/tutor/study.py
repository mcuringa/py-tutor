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
    return sorted(levels, key=itemgetter(1), reverse=True)


def current_level(student, cutoff=.75):
    levels = correct_at_levels(student)
    print("============= levels =============")
    print(len(levels))
    if len(levels) < 5:
        print("not enough data yet")
        return 1

    total = sum([count for level, count in levels])
    for level, count in levels:
        pct = count/total
        if pct >=cutoff:
            return level + 1
    return 1

def random_level(level):
    c = random.randint(1, 5)
    if c < 4:
        return level
    if c == 4:
        return max(level - 1, 1)
    
    max_level = len(Question.levels)
    return min(level + 1, max_level)


def next_question(student, tag=""):
    level = current_level(student)
    last2 = Response.objects.filter(user=student).order_by("-submitted").values_list("question").distinct()[:2]
    pool = Question.objects.filter(status=Question.ACTIVE)
    if len(tag) > 0:
        pool = pool.filter(tags__icontains=tag)
    lastids = [q[0] for q in last2]
    pool = pool.exclude(id__in=lastids)
    print("level is:", level)
    level_choice = random_level(level)
    print("level_choice is:", level_choice)
    level_count = pool.filter(level=level_choice).count()
    if level_count > 0:
        pool = pool.filter(level=level_choice)


    # pool = Question.objects.filter(level=level, status=Question.ACTIVE).exclude(id__in=lastids)
    return random.choice(pool)






