from allauth.account.adapter import get_adapter
from rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from . import models
from quiz.serializers import *
import datetime

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('email', 'username', 'password', 'mobile', 'profile_pic', 'first_name', 'last_name')


class CustomRegisterSerializer(RegisterSerializer):
    mobile = serializers.CharField(allow_blank = True, allow_null=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField(allow_blank = True, allow_null=True)
    email = serializers.EmailField(allow_blank = True, allow_null=True)
    profile_pic = serializers.ImageField(allow_null=True)

    class Meta:
        model = models.User
        fields = ('email', 'username', 'password', 'mobile', 'first_name', 'last_name', 'profile_pic')

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            'email': self.validated_data.get('email', ''),
            'mobile': self.validated_data.get('mobile', ''),
            'profile_pic': self.validated_data.get('profile_pic', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user.mobile = self.cleaned_data.get('mobile')
        user.profile_pic = self.cleaned_data.get('profile_pic')
        user.save()
        adapter.save_user(request, user, self)
        return user


class TokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = Token
        fields = ('key', 'user')

class TeamMemberSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name="team-members-detail")

    class Meta:
        model = models.TeamMember
        fields = ['id', 'image', 'name', 'designation']

class TeamFormSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name="team-form-detail")

    class Meta:
        model = models.TeamForm
        fields = ['id', 'full_name', 'email', 'mobile', 'cv', 'other_document']

class ContactUsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ContactUs
        fields = ['id', 'full_name', 'email', 'mobile', 'message']

class FeedbackSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name="feedback-detail")

    class Meta:
        model = models.Feedback
        fields = ['id', 'experience', 'message', 'is_bug']

class FAQSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name="faqs-detail")

    class Meta:
        model = models.FAQ
        fields = ['id', 'question', 'answer']

class ArticleSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name="articles-detail")

    class Meta:
        model = models.Article
        fields = ['id', 'title', 'image', 'date', 'content']

class NewsSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name="news-detail")

    class Meta:
        model = models.News
        fields = ['id', 'title', 'image', 'date', 'content']


class NewsletterSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name="newsletter-detail")

    class Meta:
        model = models.Newsletter
        fields = ['id', 'email']

class CategorySerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name="core:category-detail")

    class Meta:
        model = models.Category
        fields = ['id', 'name']

class SubCategorySerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name="core:sub-category-detail")

    class Meta:
        model = models.SubCategory
        fields = ['id', 'name']


class PDFSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name="core:pdf-detail")
    sub_category = SubCategorySerializer(many=False, read_only = True)
    type = serializers.SerializerMethodField(read_only = True)

    class Meta:
        model = models.PDF
        fields = [ 'id', 'name', 'file', 'price', 'sub_category', 'type']

    def get_type(self, obj):
        return "pdf"

class PDFListSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name="core:pdf-detail")
    sub_category = SubCategorySerializer(many=False, read_only = True)
    type = serializers.SerializerMethodField(read_only = True)

    class Meta:
        model = models.PDF
        fields = ['id', 'name', 'price', 'sub_category', 'file', 'type']

    def get_type(self, obj):
        return "pdf"

class MCQSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name="core:mcq-detail")
    sub_category = SubCategorySerializer(many=False, read_only = True)
    type = serializers.SerializerMethodField(read_only = True)

    class Meta:
        model = models.MCQ
        fields = ['id', 'name', 'file', 'price', 'sub_category', 'image', 'preview_file', 'description', 'type']

    def get_type(self, obj):
        return "mcq"

class MCQListSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name="core:mcq-detail")
    sub_category = SubCategorySerializer(many=False, read_only = True)
    type = serializers.SerializerMethodField(read_only = True)

    class Meta:
        model = models.MCQ
        fields = [ 'id', 'file', 'name', 'price', 'sub_category', 'image', 'preview_file', 'description', 'type' ]

    def get_type(self, obj):
        return "mcq"

class SummarySerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name="core:summary-detail")
    sub_category = SubCategorySerializer(many=False, read_only = True)
    mcq = MCQSerializer(many=True, read_only = True)
    type = serializers.SerializerMethodField(read_only = True)

    class Meta:
        model = models.Summary
        fields = ['id', 'name', 'file', 'price', 'sub_category', 'description','mcq', 'image', 'preview_file', 'type']

    def get_type(self, obj):
        return "summary"

class SummaryListSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name="core:summary-detail")
    sub_category = SubCategorySerializer(many=False, read_only = True)
    mcq = MCQListSerializer(many=True, read_only = True)
    type = serializers.SerializerMethodField(read_only = True)

    class Meta:
        model = models.Summary
        fields = ['id', 'name', 'price', 'sub_category', 'description','mcq',  'image', 'preview_file', 'type']

    def get_type(self, obj):
        return "summary"

class SessionSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name="core:session-detail")
    type = serializers.SerializerMethodField(read_only = True)
    upcoming = serializers.SerializerMethodField(read_only = True)

    class Meta:
        model = models.Session
        fields = ['id', 'name', 'image', 'price', 'date', 'video','youtube_link', 'type', 'upcoming', 'demo']

    def get_type(self, obj):
        return "session"

    def get_upcoming(self, obj):
        if obj.date > datetime.date.today():
            return True
        else:
            return False

class SessionListSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name="core:session-detail")
    type = serializers.SerializerMethodField(read_only = True)
    upcoming = serializers.SerializerMethodField(read_only = True)

    class Meta:
        model = models.Session
        fields = ['id', 'name', 'image', 'price', 'date','youtube_link', 'type', 'upcoming', 'demo']

    def get_type(self, obj):
        return "session"

    def get_upcoming(self, obj):
        if obj.date > datetime.date.today():
            return True
        else:
            return False

class UserSubscriptionsSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name="core:user-subscription-detail")
    user = UserSerializer(many=False, read_only = True)
    pdfs = PDFSerializer(many=True, read_only = True)
    mcqs = MCQSerializer(many=True, read_only = True)
    summaries = SummarySerializer(many=True, read_only = True)
    sessions = SessionSerializer(many=True, read_only = True)
    tests = QuizListSerializer(many=True, read_only = True)

    class Meta:
        model = models.UserSubscriptions
        fields = ['id', 'user', 'pdfs', 'mcqs', 'summaries', 'sessions', 'tests']

class SearchSerializer(serializers.Serializer):
    pdfs = PDFSerializer(many=True, read_only = True)
    mcqs = MCQSerializer(many=True, read_only = True)
    summaries = SummarySerializer(many=True, read_only = True)
    sessions = SessionSerializer(many=True, read_only = True)
    tests = QuizListSerializer(many=True, read_only = True)


















