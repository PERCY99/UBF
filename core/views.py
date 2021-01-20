from django.shortcuts import render, get_object_or_404, get_list_or_404
from . import models, serializers
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.decorators import api_view, schema

from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
from quiz import models as quizmodels
class Subscriptions():
    def __init__(self, pdfs, mcqs, summaries, sessions, tests):
        self.pdfs = pdfs
        self.mcqs = mcqs
        self.summaries = summaries
        self.sessions = sessions
        self.tests = tests


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()


class TeamMemberViewSet(viewsets.ModelViewSet):
    queryset = models.TeamMember.objects.all()
    serializer_class = serializers.TeamMemberSerializer

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

class TeamFormViewSet(viewsets.ModelViewSet):
    queryset = models.TeamForm.objects.all()
    serializer_class = serializers.TeamFormSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

class ContactUsViewSet(viewsets.ModelViewSet):
    queryset = models.ContactUs.objects.all()
    serializer_class = serializers.ContactUsSerializer

    # def get_permissions(self):
    #     if self.action == 'create':
    #         permission_classes = [permissions.AllowAny]
    #     else:
    #         permission_classes = [permissions.IsAdminUser]
    #     return [permission() for permission in permission_classes]

class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = models.Feedback.objects.all()
    serializer_class = serializers.FeedbackSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

class FAQViewSet(viewsets.ModelViewSet):
    queryset = models.FAQ.objects.all()
    serializer_class = serializers.FAQSerializer

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = models.Article.objects.all()
    serializer_class = serializers.ArticleSerializer

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

class NewsViewSet(viewsets.ModelViewSet):
    queryset = models.News.objects.all()
    serializer_class = serializers.NewsSerializer

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]


class NewsletterViewSet(viewsets.ModelViewSet):
    queryset = models.Newsletter.objects.all()
    serializer_class = serializers.NewsletterSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = models.SubCategory.objects.all()
    serializer_class = serializers.SubCategorySerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

class PDFSerializer(viewsets.ModelViewSet):
    queryset = models.PDF.objects.all()
    serializer_class = serializers.PDFListSerializer

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [permissions.AllowAny]
        elif self.action == 'retrieve':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = models.PDF.objects.all()

        subcategory = self.request.query_params.get('subcategory', None)
        if subcategory is not None:
            queryset = queryset.filter(sub_category__name__iexact =subcategory)

        price = self.request.query_params.get('price', None)
        if price is not None:
            queryset = queryset.filter(price__exact = int(price))

        search = self.request.query_params.get('search', None)
        if search is not None:
            queryset = queryset.filter(name__icontains = search)
        return queryset

    def retrieve(self, request, pk=None, *args, **kwargs):
        serializer_context = {
            'request': request,
        }
        queryset = models.PDF.objects.all()
        pdf = get_object_or_404(queryset, pk=pk)
        serializer = serializers.PDFSerializer(pdf, context=serializer_context)
        return Response(serializer.data)


class MCQSerializer(viewsets.ModelViewSet):
    queryset = models.MCQ.objects.all()
    serializer_class = serializers.MCQListSerializer

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [permissions.AllowAny]
        elif self.action == 'retrieve':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = models.MCQ.objects.all()

        subcategory = self.request.query_params.get('subcategory', None)
        if subcategory is not None:
            queryset = queryset.filter(sub_category__name__iexact =subcategory)

        price = self.request.query_params.get('price', None)
        if price is not None:
            queryset = queryset.filter(price__exact = int(price))

        search = self.request.query_params.get('search', None)
        if search is not None:
            queryset = queryset.filter(name__icontains = search)
        return queryset

    def retrieve(self, request, pk=None, *args, **kwargs):
        serializer_context = {
            'request': request,
        }
        queryset = models.MCQ.objects.all()
        mcq = get_object_or_404(queryset, pk=pk)
        subscribed = get_object_or_404(models.UserSubscriptions, user=request.user)
        if (mcq in subscribed.mcqs.all()) or mcq.price < 1:
            serializer = serializers.MCQSerializer(mcq, context=serializer_context)
            return Response(serializer.data)
        else:
            return Response({"message": "MCQ Not Purchased"}, status=HTTP_400_BAD_REQUEST)


class SummarySerializer(viewsets.ModelViewSet):
    queryset = models.Summary.objects.all()
    serializer_class = serializers.SummaryListSerializer

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [permissions.AllowAny]
        elif self.action == 'retrieve':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = models.Summary.objects.all()

        subcategory = self.request.query_params.get('subcategory', None)
        if subcategory is not None:
            queryset = queryset.filter(sub_category__name__iexact =subcategory)

        price = self.request.query_params.get('price', None)
        if price is not None:
            queryset = queryset.filter(price__exact = int(price))

        search = self.request.query_params.get('search', None)
        if search is not None:
            queryset = queryset.filter(name__icontains = search)
        return queryset

    def retrieve(self, request, pk=None, *args, **kwargs):
        serializer_context = {
            'request': request,
        }
        queryset = models.Summary.objects.all()
        summary = get_object_or_404(queryset, pk=pk)
        subscribed = get_object_or_404(models.UserSubscriptions, user = request.user)
        if (summary in subscribed.summaries.all()) or summary.price < 1:
            serializer = serializers.SummarySerializer(summary, context=serializer_context)
            return Response(serializer.data)
        else:
            return Response({"message": "Summary Not Purchased"}, status=HTTP_400_BAD_REQUEST)



class SessionSerializer(viewsets.ModelViewSet):
    queryset = models.Session.objects.all()
    serializer_class = serializers.SessionListSerializer

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [permissions.AllowAny]
        elif self.action == 'retrieve':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = models.Session.objects.all()

        price = self.request.query_params.get('price', None)
        if price is not None:
            queryset = queryset.filter(price__exact = int(price))

        search = self.request.query_params.get('search', None)
        if search is not None:
            queryset = queryset.filter(name__icontains = search)
        return queryset

    def retrieve(self, request, pk=None, *args, **kwargs):
        serializer_context = {
            'request': request,
        }
        queryset = models.Session.objects.all()
        session = get_object_or_404(queryset, pk=pk)

        subscribed = get_object_or_404(models.UserSubscriptions, user = request.user)
        if (session in subscribed.sessions.all()) or session.price < 1:
            serializer = serializers.SessionSerializer(session, context=serializer_context)
            return Response(serializer.data)
        else:
            return Response({"message": "Session Not Purchased"}, status=HTTP_400_BAD_REQUEST)

class UserSubscriptionsSerializer(viewsets.ModelViewSet):
    queryset = models.UserSubscriptions.objects.all()
    serializer_class = serializers.UserSubscriptionsSerializer

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        user = request.user
        serializer_context = {
            'request': request,
        }
        queryset = models.UserSubscriptions.objects.all()
        user_subscription = get_object_or_404(queryset, user=user)
        serializer = serializers.UserSubscriptionsSerializer(user_subscription, many=False, context=serializer_context)
        return Response(serializer.data)

class SearchSubscriptionsView(APIView):

    def get(self, request):
        pdfs = models.PDF.objects.all()
        mcqs = models.MCQ.objects.all()
        summaries = models.Summary.objects.all()
        sessions = models.Session.objects.all()
        tests = quizmodels.Quiz.objects.all()

        search = self.request.query_params.get('search', None)
        if search is not None:
            pdfs = pdfs.filter(name__icontains = search)
            mcqs = mcqs.filter(name__icontains = search, description__icontains = search)
            summaries = summaries.filter(name__icontains = search, description__icontains = search)
            sessions = sessions.filter(name__icontains = search)
            tests = tests.filter(name__icontains = search, description__icontains = search)

        subscriptions = Subscriptions(pdfs, mcqs, summaries, sessions, tests)

        data = serializers.SearchSerializer(subscriptions).data
        return Response(data)
