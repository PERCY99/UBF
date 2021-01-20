# Create your tasks here

from celery import shared_task
from demoapp.models import Widget
from quiz import models
from datetime import datetime
from django.db.models import Q, Count


# from celery.task.schedules import crontab
# from celery.decorators import periodic_task
#
#
# @periodic_task(run_every=(crontab(minute='*/15')), name="some_task", ignore_result=True)
# def some_task():
    # do something


@shared_task
def EndQuiz(quiz):
    # datetimes = models.QuizSlot.objects.filter(quiz = quiz, start_datetime__gte = datetime.now())
    # for start_datetime in datetimes:

    quiztakers = models.QuizTaker.objects.filter(quiz = quiz, completed=False)
    quiztakers.update(completed=True, date_finished = datetime.now())
    for quiztaker in quiztakers:
        correct_answers = 0

        for users_answer in models.UsersAnswer.objects.filter(quiz_taker=quiztaker):
            answer = models.Answer.objects.get(question=users_answer.question, is_correct=True)
            if users_answer.answer == answer:
                correct_answers += 1

        quiztaker.score = int(correct_answers / quiztaker.quiz.question_set.count() * 100)

        aggregate = models.QuizTaker.objects.filter(score__lt=quiztaker.score).aggregate(ranking=Count('score'))
        quiztaker.quiz_day_rank = int(aggregate['ranking'] + 1)

        quiztaker.save()

    return True

