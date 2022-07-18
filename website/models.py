from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse

class User(AbstractUser):
    watchlist = models.ManyToManyField("List", related_name="watchers")

class Podcast(models.Model):
    podcast_id = models.AutoField(primary_key=True, default=None)
    title = models.TextField(default=None)
    image = models.TextField(default=None)
    creator = models.TextField()
    information = models.TextField()

    def __str__(self):
        return self.title

class Episode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    episode_id = models.AutoField(primary_key=True, default=None, blank=True)
    title = models.TextField(default=None)
    information = models.TextField(default=None)
    date = models.DateField(default=None)
    image = models.TextField(default=None)
    podcast = models.ForeignKey(Podcast, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class List(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    list_id = models.AutoField(primary_key=True, default=None)
    title = models.TextField(default=None)
    description = models.TextField(default=None)
    is_private = models.BooleanField(default=False)
    image = models.TextField(default=None)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("detail", kwargs={"id": self.id})

class ListContent(models.Model):
    custom_list = models.ForeignKey(List, on_delete=models.CASCADE, blank=True, null=True)
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE, blank=True, null=True)
    podcast = models.ForeignKey(Podcast, on_delete=models.CASCADE, blank=True, null=True)

class Review(models.Model):
    review_id = models.AutoField(primary_key=True, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    content = models.TextField()
    episode = models.ForeignKey(Episode, on_delete=models.SET_NULL, blank=True, null=True)
    podcast = models.ForeignKey(Podcast, on_delete=models.SET_NULL, blank=True, null=True)
    score = models.IntegerField(default=0,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0)
        ]
    )

    def __str__(self):
        return str(self.pk)


class Follow(models.Model):
    following = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name="is_following")
    follower = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name="followed_by")
    