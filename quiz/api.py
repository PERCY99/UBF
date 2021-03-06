from django.db.models import Q, Count
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from quiz.models import Answer, Question, Quiz, QuizTaker, UsersAnswer, UserVerification
from quiz.serializers import MyQuizListSerializer, QuizDetailSerializer, QuizListSerializer, QuizResultSerializer, UsersAnswerSerializer, QuizLeaderBoardSerializer, UserVerificationSerializer
from core import models as coremodels
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
import datetime



class MyQuizListAPI(generics.ListAPIView):
	permission_classes = [
		permissions.IsAuthenticated
	]
	serializer_class = MyQuizListSerializer

	def get_queryset(self, *args, **kwargs):
		queryset = Quiz.objects.filter(quiztaker__user=self.request.user)
		query = self.request.GET.get("q")

		if query:
			queryset = queryset.filter(
				Q(name__icontains=query) |
				Q(description__icontains=query)
			).distinct()

		return queryset


class QuizListAPI(generics.ListAPIView):
	serializer_class = QuizListSerializer
	permission_classes = [
		permissions.AllowAny,
	]

	def get_queryset(self, *args, **kwargs):
		queryset = Quiz.objects.filter(roll_out=True)
		# .exclude(quiztaker__user=self.request.user)
		query = self.request.GET.get("q")

		if query:
			queryset = queryset.filter(
				Q(name__icontains=query) |
				Q(description__icontains=query)
			).distinct()

		return queryset

	def list(self,request,*args,**kwargs):
		qs = self.get_queryset()

		serializer = self.serializer_class(qs,many=True)
		live = request.GET.get("live")
		data=list()
		data2=list()
		if live:
			live=live.lower()
			for i in serializer.data:
				if i['islive']:
					data.append(i)
				else:
					data2.append(i)
		if live:
			if live == 'true':
				return Response(data)
			elif live == 'false':
				return Response(data2)
		else:
			return Response(serializer.data)

class QuizDetailAPI(generics.RetrieveAPIView):
	serializer_class = QuizDetailSerializer
	permission_classes = [
		permissions.IsAuthenticated
	]

	def get(self, *args, **kwargs):
		slug = self.kwargs["slug"]
		quiz = get_object_or_404(Quiz, slug=slug)

		subscribed = get_object_or_404(coremodels.UserSubscriptions, user=self.request.user)
		if (quiz not in subscribed.tests.all()) and (quiz.price > 1):
			return Response({"message": "Test Not Purchased"}, status=HTTP_400_BAD_REQUEST)

		last_question = None
		obj, created = QuizTaker.objects.get_or_create(user=self.request.user, quiz=quiz)
		if created:
			for question in Question.objects.filter(quiz=quiz):
				UsersAnswer.objects.create(quiz_taker=obj, question=question)
		else:
			last_question = UsersAnswer.objects.filter(quiz_taker=obj, answer__isnull=False)
			if last_question.count() > 0:
				last_question = last_question.last().question.id
			else:
				last_question = None

		return Response({'quiz': self.get_serializer(quiz, context={'request': self.request}).data, 'last_question_id': last_question})

class QuizLeaderBoardAPI(generics.RetrieveAPIView):
	serializer_class = QuizLeaderBoardSerializer
	permission_classes = [
		permissions.IsAuthenticated
	]

	def get(self, *args, **kwargs):
		slug = self.kwargs["slug"]
		quiz = get_object_or_404(Quiz, slug=slug)
		return Response(self.get_serializer(quiz, context={'request': self.request}).data)

class SaveUsersAnswer(generics.UpdateAPIView):
	serializer_class = UsersAnswerSerializer
	permission_classes = [
		permissions.IsAuthenticated
	]

	def patch(self, request, *args, **kwargs):
		quiztaker_id = request.data['quiztaker']
		question_id = request.data['question']
		answer_id = request.data['answer']

		quiztaker = get_object_or_404(QuizTaker, id=quiztaker_id)
		question = get_object_or_404(Question, id=question_id)
		answer = get_object_or_404(Answer, id=answer_id)

		if quiztaker.completed:
			return Response({
				"message": "This quiz is already complete. you can't answer any more questions"},
				status=status.HTTP_412_PRECONDITION_FAILED
			)

		obj = get_object_or_404(UsersAnswer, quiz_taker=quiztaker, question=question)
		obj.answer = answer
		obj.save()

		return Response(self.get_serializer(obj).data)

class SubmitQuizAPI(generics.GenericAPIView):
	serializer_class = QuizResultSerializer
	permission_classes = [
		permissions.IsAuthenticated
	]

	def post(self, request, *args, **kwargs):
		quiztaker_id = request.data['quiztaker']
		# question_id = request.data['question']
		# answer_id = request.data['answer']

		quiztaker = get_object_or_404(QuizTaker, id=quiztaker_id)
		# question = get_object_or_404(Question, id=question_id)

		quiz = Quiz.objects.get(slug=self.kwargs['slug'])

		if quiztaker.completed:
			return Response({
				"message": "This quiz is already complete. You can't submit again"},
				status=status.HTTP_412_PRECONDITION_FAILED
			)

		# if answer_id is not None:
		# 	answer = get_object_or_404(Answer, id=answer_id)
		# 	obj = get_object_or_404(UsersAnswer, quiz_taker=quiztaker, question=question)
		# 	obj.answer = answer
		# 	obj.save()

		quiztaker.completed = True
		quiztaker.date_finished = datetime.datetime.now()
		correct_answers = 0

		for users_answer in UsersAnswer.objects.filter(quiz_taker=quiztaker):
			answer = Answer.objects.get(question=users_answer.question, is_correct=True)
			if users_answer.answer == answer:
				correct_answers += 1

		quiztaker.score = int(correct_answers / quiztaker.quiz.question_set.count() * 100)

		aggregate = QuizTaker.objects.filter(score__lt=quiztaker.score).aggregate(ranking=Count('score'))
		quiztaker.quiz_day_rank = int(aggregate['ranking'] + 1)

		quiztaker.save()
		return Response(self.get_serializer(quiz).data)



class UserVerificationView(viewsets.ModelViewSet):
	queryset = UserVerification.objects.all()
	serializer_class = UserVerificationSerializer

	def create(self, request, *args, **kwargs):
		verification_serializer = self.get_serializer(data=request.data)
		verification_serializer.is_valid(raise_exception=True)
		self.perform_create(verification_serializer)
		headers =self.get_success_headers(verification_serializer.data)

		verification_id = verification_serializer.data['id']
		user_verification = UserVerification.objects.get(id=verification_id)
		print(user_verification.image)

		import cv2
		import quiz.verification.head_pose_estimation_new as HPEN
		import quiz.verification.eye_tracker_new as ETN
		#import face_spoofing_new as FSN
		import quiz.verification.mouth_opening_detector_new as MODN
		import quiz.verification.person_and_phone_new as PAPN

		path = user_verification.image.url[1:]
		img = cv2.imread(path)
		print("__________________________________________________________________")
		print(path)
		print("__________________________________________________________________")

		res1 = HPEN.head_pose_estimator(img)
		
		res2 = ETN.eye_track(img)

		#res3 = FSN.face_spoof(img)
		res4 = MODN.mouth_detect(img)
		res5 = PAPN.phone_detect(img)
		print('head_pose: ',res1)
		print('eye_pos: ',res2)
		#print('face_spoof: ',res3)
		print('mouth: ',res4)
		print('phone or multiple persons: ',res5)
		
		response = res1 + res2 + res4 + res5
			

		return Response(response, status=status.HTTP_200_OK, headers=headers)


def tes12t(request):
	user_verification = UserVerification.objects.get(id=2)
	print(user_verification.image)

	import cv2
	import quiz.verification.head_pose_estimation_new as HPEN
	import quiz.verification.eye_tracker_new as ETN
	#import face_spoofing_new as FSN
	import quiz.verification.mouth_opening_detector_new as MODN
	import quiz.verification.person_and_phone_new as PAPN

	path = user_verification.image.url[1:]
	img = cv2.imread(path)
	print("__________________________________________________________________")
	print(path)
	print("__________________________________________________________________")
	print(user_verification.image.url)
	print(img)
	res1 = HPEN.head_pose_estimator(img)
	
	res2 = ETN.eye_track(img)

	#res3 = FSN.face_spoof(img)
	res4 = MODN.mouth_detect(img)
	res5 = PAPN.phone_detect(img)
	print('head_pose: ',res1)
	print('eye_pos: ',res2)
	#print('face_spoof: ',res3)
	print('mouth: ',res4)
	print('phone or multiple persons: ',res5)

	if(res4 == 'Mouth open' and res1 != 'OK' ):
		response = 1
	elif(res1 != 'OK' and res2 != 'OK'):
		response = 1
	elif(res5 != 'OK'):
		response = 2
	else:
		response = 3
	return Response(response, status=status.HTTP_200_OK)