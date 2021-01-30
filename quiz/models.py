from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify


class Quiz(models.Model):
	name = models.CharField(max_length=100)
	description = models.CharField(max_length=70)
	image = models.ImageField()
	slug = models.SlugField(blank=True)
	timestamp = models.DateTimeField(auto_now_add=True)
	price = models.PositiveSmallIntegerField()
	duration = models.DurationField(null=True)
	live = models.BooleanField(default=False)
	roll_out = models.BooleanField(default=False)
	rollout_date=models.DateTimeField(blank=True,null=True)
	answerkey=models.FileField(blank=True,null=True)

	class Meta:
		ordering = ['timestamp',]
		verbose_name_plural = "Quizzes"

	def __str__(self):
		return self.name

class QuizSlot(models.Model):
	quiz = models.ForeignKey('quiz.Quiz', on_delete=models.CASCADE)
	start_datetime = models.DateTimeField()

	class Meta:
		verbose_name_plural = "Quiz Slots"

	def __str__(self):
		return self.quiz

class Question(models.Model):
	quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
	label = models.CharField(max_length=100)
	order = models.IntegerField(default=0)

	def __str__(self):
		return self.label


class Answer(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	label = models.CharField(max_length=100)
	is_correct = models.BooleanField(default=False)

	def __str__(self):
		return self.label


class QuizTaker(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
	score = models.IntegerField(default=0)
	completed = models.BooleanField(default=False)
	date_finished = models.DateTimeField(null=True, blank=True)
	timestamp = models.DateTimeField(auto_now_add=True)
	quiz_day_rank = models.PositiveIntegerField(null=True, blank=True)

	def __str__(self):
		return self.user.email


class UsersAnswer(models.Model):
	quiz_taker = models.ForeignKey(QuizTaker, on_delete=models.CASCADE)
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True)

	def __str__(self):
		return self.question.label


@receiver(pre_save, sender=Quiz)
def slugify_name(sender, instance, *args, **kwargs):
	instance.slug = slugify(instance.name)



class UserVerification(models.Model):
	quiz_taker = models.ForeignKey("quiz.QuizTaker", on_delete=models.CASCADE)
	datetime = models.DateTimeField(auto_now_add=True)
	image = models.ImageField()
	verified = models.BooleanField(default=False)

	def __str__(self):
		return str(self.quiz_taker)
		
