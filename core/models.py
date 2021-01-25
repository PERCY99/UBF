from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

class User(AbstractUser):
    mobile = models.CharField(max_length = 16, blank=True, null=True)
    profile_pic = models.ImageField(blank=True, null=True)
    base64 = models.TextField(blank=True, null=True)

class TeamMember(models.Model):
    image = models.ImageField()
    name = models.CharField(max_length = 256)
    designation = models.CharField(max_length = 256)

class TeamForm(models.Model):
    full_name = models.CharField(max_length = 256)
    email = models.EmailField()
    mobile = models.CharField(max_length = 16)
    cv = models.FileField()
    image = models.ImageField(blank = True, null=True)
    other_document = models.FileField(blank = True, null=True)

    class Meta:
        verbose_name_plural = 'Team Form'

class ContactUs(models.Model):
    full_name = models.CharField(max_length=256)
    email = models.EmailField()
    mobile = models.CharField(max_length=16)
    message = models.TextField()

    class Meta:
        verbose_name_plural = 'Contact Us'

feedback_experience_choices = (
    ('Happy', 'Happy'),
    ('Sad', 'Sad'),
    ('Neutral', 'Neutral'),
)
class Feedback(models.Model):
    experience = models.CharField(max_length = 8)
    message = models.TextField()
    is_bug = models.BooleanField(default = False)

    class Meta:
        verbose_name_plural = 'Feedbacks'

class FAQ(models.Model):
    question = models.CharField(max_length = 512)
    answer = models.TextField()

    class Meta:
        verbose_name_plural = 'FAQs'

class Article(models.Model):
    title = models.CharField(max_length = 512)
    image = models.ImageField()
    date = models.DateField()
    content = models.TextField()

    class Meta:
        verbose_name_plural = 'Articles'

class News(models.Model):
    title = models.CharField(max_length = 512)
    image = models.ImageField()
    date = models.DateField()
    content = models.TextField()

    class Meta:
        verbose_name_plural = 'NEWS'

class Newsletter(models.Model):
    email = models.EmailField()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = 'Newsletters'


class Category(models.Model):
    name = models.CharField(max_length = 64)

    class Meta:
        verbose_name_plural = 'Categories'

class SubCategory(models.Model):
    category = models.ForeignKey('core.Category', on_delete=models.PROTECT)
    name = models.CharField(max_length = 64)

    class Meta:
        verbose_name_plural = 'Sub-Categories'

class PDF(models.Model):
    sub_category = models.ForeignKey('core.SubCategory', on_delete=models.PROTECT)
    name = models.CharField(max_length=256)
    file = models.FileField()
    price = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name_plural = 'PDFs'

class MCQ(models.Model):
    sub_category = models.ForeignKey('core.SubCategory', on_delete=models.PROTECT)
    name = models.CharField(max_length=256)
    file = models.FileField()
    image = models.ImageField()
    preview_file = models.FileField()
    description = models.TextField(blank=True, null=True)
    price = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name_plural = 'MCQs'

class Summary(models.Model):
    sub_category = models.ForeignKey('core.SubCategory', on_delete=models.PROTECT)
    name = models.CharField(max_length=256)
    description = models.TextField()
    file = models.FileField()
    image = models.ImageField()
    preview_file = models.FileField()
    price = models.PositiveSmallIntegerField(default=0)
    mcq = models.ManyToManyField('core.MCQ', null=True)

    class Meta:
        verbose_name_plural = 'Summaries'

class Session(models.Model):
    image = models.ImageField()
    name = models.CharField(max_length = 128)
    date = models.DateField()
    demo = models.FileField(blank=True, null=True)
    video = models.FileField(blank = True, null = True)
    youtube_link = models.CharField(max_length = 512, blank = True, null = True)
    price = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name_plural = 'Sessions'

class UserSubscriptions(models.Model):
    user = models.OneToOneField('core.User', on_delete=models.PROTECT)
    pdfs = models.ManyToManyField('core.PDF', blank=True)
    mcqs = models.ManyToManyField('core.MCQ', blank=True)
    summaries = models.ManyToManyField('core.Summary', blank=True)
    sessions = models.ManyToManyField('core.Session', blank=True)
    tests = models.ManyToManyField('quiz.Quiz', blank=True)
    class Meta:
        verbose_name_plural = 'User Subscriptions'




@receiver(post_save, sender=User)
def my_callback(sender, instance, *args, **kwargs):
    user_subscription = UserSubscriptions.objects.get_or_create(user=instance)




