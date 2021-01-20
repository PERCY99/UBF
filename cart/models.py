from django.db import models

# Create your models here.
class UserCart(models.Model):
    user = models.ForeignKey('core.User', on_delete=models.PROTECT)
    pdfs = models.ManyToManyField('core.PDF', blank=True)
    mcqs = models.ManyToManyField('core.MCQ', blank=True)
    summaries = models.ManyToManyField('core.Summary', blank=True)
    sessions = models.ManyToManyField('core.Session', blank=True)
    tests = models.ManyToManyField('quiz.Quiz', blank=True)

    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(blank=True, null=True)
    ordered = models.BooleanField(default=False)
    order_id = models.CharField(max_length=64, unique=True)
    payment = models.ForeignKey('cart.Payment', on_delete=models.PROTECT, blank=True, null=True)

    single_product = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Carts'

class Bookmark(models.Model):
    user = models.OneToOneField('core.User', on_delete=models.PROTECT)
    pdfs = models.ManyToManyField('core.PDF', blank=True)
    mcqs = models.ManyToManyField('core.MCQ', blank=True)
    summaries = models.ManyToManyField('core.Summary', blank=True)
    sessions = models.ManyToManyField('core.Session', blank=True)
    tests = models.ManyToManyField('quiz.Quiz', blank=True)
    class Meta:
        verbose_name_plural = 'Bookmarks'

class SaveForLater(models.Model):
    user = models.OneToOneField('core.User', on_delete=models.PROTECT)
    pdfs = models.ManyToManyField('core.PDF', blank=True)
    mcqs = models.ManyToManyField('core.MCQ', blank=True)
    summaries = models.ManyToManyField('core.Summary', blank=True)
    sessions = models.ManyToManyField('core.Session', blank=True)
    tests = models.ManyToManyField('quiz.Quiz', blank=True)

    class Meta:
        verbose_name_plural = 'Saved For Later'

class Payment(models.Model):
    order_id = models.CharField(max_length=128)
    payment_id = models.CharField(max_length=128)
    date_time = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Payments'