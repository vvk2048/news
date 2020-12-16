import uuid

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from datetime import datetime, timezone
from taggit.managers import TaggableManager

class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, null=True)
    version = models.IntegerField(default=0)

    def __str__(self):
        return self.user.email

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

class Category(models.Model):

    name = models.CharField(max_length=31)
    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.name

class MyCategory(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    categorys = models.ManyToManyField(Category)

    def __str__(self):
        return self.user.email

class Topic(models.Model):

    name = models.CharField(max_length=31)
    image = models.ImageField(blank=True, null=True)
    priority = models.IntegerField(default=1)

    def __str__(self):
        return self.name

class Tag(models.Model):

    name = models.CharField(max_length=30)
    image = models.ImageField(blank=True, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class MyTag(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.user.username

class Quote(models.Model):

    author = models.CharField(max_length=31)
    body = models.CharField(max_length=127)
    period = models.CharField(max_length=31)

    visibility = models.BooleanField(default=False)

    def __str__(self):
        return "%s - %s" % (self.author, self.period)

class News(models.Model):

    headline = models.CharField(max_length=127)

    tags = models.ManyToManyField(Tag, blank=True)
    etags = TaggableManager()

    category = models.ManyToManyField(Category)

    time = models.DateTimeField()

    body = models.TextField()
    image = models.ImageField(null=True, blank=True)

    newsAgency = models.CharField(max_length=512, default='Independent')
    source = models.URLField(max_length=255)

    FILE_TYPE = [
        ('IMG', 'Image'),
        ('VID', 'Video')
    ]
    file_type = models.CharField(max_length=7, choices=FILE_TYPE, default='IMG')
    user = models.ForeignKey(User, null=True, blank=True, default=None, on_delete=models.CASCADE)

    pos = models.IntegerField(default=0)
    neg = models.IntegerField(default=0)

    clickable = models.BooleanField(default=True)
    visibility = models.BooleanField(default=False)
    independent = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.headline

class MyNews(models.Model):

    headline = models.CharField(max_length=127)
    body = models.TextField()
    source = models.URLField(max_length=255)
    location = models.CharField(max_length=255, blank=True, default=True)

    FILE_TYPE = [
        ('IMG', 'Image'),
        ('VID', 'Video')
    ]
    file_type = models.CharField(max_length=7, choices=FILE_TYPE, default='IMG')

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    news = models.ForeignKey(News, null=True, blank=True, default=None, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.headline

class Save(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    news = models.ForeignKey(
        'News',
        on_delete=models.CASCADE,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} : {}".format(
            self.user.username,
            self.news.headline
        )

    class Meta:
        unique_together = ['user', 'news']


class Vote(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    news = models.ForeignKey(
        'News',
        on_delete=models.CASCADE,
    )

    polarity = models.BooleanField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} : {}".format(
            self.user.username,
            self.news.headline
        )

    class Meta:
        unique_together = ['user', 'news']

    def save(self, *args, **kwargs):

        if self.pk:
            obj = Vote.objects.values('polarity').get(pk=self.pk)

            if obj["polarity"]: self.news.pos -= 1
            else: self.news.neg -= 1

        if self.polarity: self.news.pos += 1
        else: self.news.neg += 1

        self.news.save()

        super(Vote, self).save(*args, **kwargs)

    def delete(self):

        if self.polarity: self.news.pos -= 1
        else: self.news.neg -= 1

        self.news.save()

        super(Vote, self).delete()
