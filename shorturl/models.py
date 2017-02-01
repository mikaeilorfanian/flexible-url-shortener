from random import randint

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class ShortURLCombination(models.Model):
    combination = models.CharField(max_length=settings.SHORT_URL_LENGTH_BOUND[1])
    used = models.BooleanField(default=False)

    def __str__(self):
        return self.combination


class URL(models.Model):
    long_url = models.URLField(primary_key=True)
    converted_url = models.OneToOneField(ShortURLCombination)
    visit_count = models.IntegerField(default=0)
    submitter = models.ForeignKey(User)

    @staticmethod
    def get_or_create_short_url(long_url):
        url_obj = URL.objects.filter(long_url=long_url).first()
        if not url_obj:
            url_obj = URL(
                long_url=long_url,
                converted_url=ShortURLCombination.objects.filter(used=False).first(),
                submitter=User.objects.all()[randint(0, User.objects.count()-1)]
            )
            url_obj.converted_url.used = True
            url_obj.converted_url.save()
            url_obj.save()

        return url_obj

    def __str__(self):
        return '%s %s %s %s' % (
            self.long_url,
            self.converted_url.combination,
            self.count,
            self.submitter,
        )
