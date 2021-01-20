from quiz.models import Quiz, QuizTaker, Question, Answer, UsersAnswer
from rest_framework import serializers
from django.db.models import Count


class QuizListSerializer(serializers.ModelSerializer):
	questions_count = serializers.SerializerMethodField()
	type = serializers.SerializerMethodField()

	class Meta:
		model = Quiz
		fields = ["id", "name", "description", "image", "slug", "questions_count", "price", "type"]
		read_only_fields = ["questions_count", "type"]

	def get_questions_count(self, obj):
		return obj.question_set.all().count()

	def get_type(self, obj):
		return "test"


class AnswerSerializer(serializers.ModelSerializer):
	class Meta:
		model = Answer
		fields = ["id", "question", "label"]


class QuestionSerializer(serializers.ModelSerializer):
	answer_set = AnswerSerializer(many=True)

	class Meta:
		model = Question
		fields = "__all__"


class UsersAnswerSerializer(serializers.ModelSerializer):
	class Meta:
		model = UsersAnswer
		fields = "__all__"


class MyQuizListSerializer(serializers.ModelSerializer):
	completed = serializers.SerializerMethodField()
	progress = serializers.SerializerMethodField()
	questions_count = serializers.SerializerMethodField()
	score = serializers.SerializerMethodField()
	type = serializers.SerializerMethodField()

	class Meta:
		model = Quiz
		fields = ["id", "name", "description", "image", "slug", "questions_count", "completed", "score", "progress", "price", "type"]
		read_only_fields = ["questions_count", "completed", "progress", "type"]

	def get_completed(self, obj):
		try:
			quiztaker = QuizTaker.objects.get(user=self.context['request'].user, quiz=obj)
			return quiztaker.completed
		except QuizTaker.DoesNotExist:
			return None

	def get_progress(self, obj):
		try:
			quiztaker = QuizTaker.objects.get(user=self.context['request'].user, quiz=obj)
			if quiztaker.completed == False:
				questions_answered = UsersAnswer.objects.filter(quiz_taker=quiztaker, answer__isnull=False).count()
				total_questions = obj.question_set.all().count()
				return int(questions_answered / total_questions)
			return None
		except QuizTaker.DoesNotExist:
			return None

	def get_questions_count(self, obj):
		return obj.question_set.all().count()

	def get_score(self, obj):
		try:
			quiztaker = QuizTaker.objects.get(user=self.context['request'].user, quiz=obj)
			if quiztaker.completed == True:
				return quiztaker.score
			return None
		except QuizTaker.DoesNotExist:
			return None

	def get_type(self, obj):
		return "test"


class QuizTakerSerializer(serializers.ModelSerializer):
	usersanswer_set = UsersAnswerSerializer(many=True)
	rank = serializers.SerializerMethodField(read_only=True)
	correct_answers = serializers.SerializerMethodField(read_only=True)
	wrong_answers = serializers.SerializerMethodField(read_only=True)
	not_attempted = serializers.SerializerMethodField(read_only=True)
	time_spent = serializers.SerializerMethodField(read_only=True)

	class Meta:
		model = QuizTaker
		fields = "__all__"

	def get_rank(self, obj):
		aggregate = QuizTaker.objects.filter(score__lt=obj.score).aggregate(ranking=Count('score'))
		return aggregate['ranking'] + 1

	def get_correct_answers(self, obj):
		correct_answers = 0
		for users_answer in UsersAnswer.objects.filter(quiz_taker=obj):
			answer = Answer.objects.get(question=users_answer.question, is_correct=True)
			if users_answer.answer == answer:
				correct_answers += 1
		return correct_answers

	def get_wrong_answers(self, obj):
		wrong_answers = 0
		for users_answer in UsersAnswer.objects.filter(quiz_taker=obj, answer__isnull=False):
			answer = Answer.objects.get(question=users_answer.question, is_correct=True)
			if users_answer.answer != answer:
				wrong_answers += 1
		return wrong_answers

	def get_not_attempted(self, obj):
		not_attempted = UsersAnswer.objects.filter(quiz_taker=obj, answer__isnull=True).count()
		return not_attempted

	def get_time_spent(self, obj):
		if obj.completed:
			time = obj.date_finished - obj.timestamp
			return (time.seconds // 3600)
		else:
			return None

class QuizDetailSerializer(serializers.ModelSerializer):
	quiztakers_set = serializers.SerializerMethodField()
	question_set = QuestionSerializer(many=True)

	class Meta:
		model = Quiz
		fields = "__all__"

	def get_quiztakers_set(self, obj):
		try:
			quiz_taker = QuizTaker.objects.get(user=self.context['request'].user, quiz=obj)
			serializer = QuizTakerSerializer(quiz_taker)
			return serializer.data
		except QuizTaker.DoesNotExist:
			return None

class QuizLeaderBoardSerializer(serializers.ModelSerializer):
	quiztakers_set = serializers.SerializerMethodField()

	class Meta:
		model = Quiz
		fields = "__all__"

	def get_quiztakers_set(self, obj):
		try:
			quiz_taker = QuizTaker.objects.filter(quiz=obj)
			serializer = QuizTakerSerializer(quiz_taker, many=True)
			return serializer.data
		except QuizTaker.DoesNotExist:
			return None

class QuizResultSerializer(serializers.ModelSerializer):
	quiztaker_set = serializers.SerializerMethodField()
	question_set = QuestionSerializer(many=True)

	class Meta:
		model = Quiz
		fields = "__all__"

	def get_quiztaker_set(self, obj):
		try:
			quiztaker = QuizTaker.objects.get(user=self.context['request'].user, quiz=obj)
			serializer = QuizTakerSerializer(quiztaker)
			return serializer.data

		except QuizTaker.DoesNotExist:
			return None




