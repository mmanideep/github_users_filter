import requests
import datetime

from django.contrib.auth.models import User
from django.contrib.auth.models import models
from django.utils.safestring import mark_safe

from settings import GIT_TOKEN


class BaseModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class GithubUser(User, BaseModel):

    name = models.TextField()
    avatar_url = models.URLField(null=True, blank=True)
    company = models.TextField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    followers = models.IntegerField()
    public_repos = models.IntegerField()
    location = models.TextField(null=True, blank=True)

    def image_tag(self):
        avatar_url = "" if not self.avatar_url else self.avatar_url
        return mark_safe('<img src="%s" width="150" height="150" />' % avatar_url)

    image_tag.short_description = "Image"

    @classmethod
    def initialize_from_git_user_api(cls, git_api_url):
        response_json = requests.get(
            git_api_url,
            headers={"Authorization": "token {}".format(GIT_TOKEN)}
        ).json()
        user_dict = {
            "username": response_json["login"],
            "id": response_json["id"],
            "name": response_json["name"],
            "email": response_json["email"],
            "avatar_url": response_json["avatar_url"],
            "created_at": datetime.datetime.utcnow(),
            "company": response_json["company"],
            "bio": response_json["bio"],
            "followers": response_json["followers"],
            "public_repos": response_json["public_repos"],
            "location": response_json["location"]
        }
        user = cls(**user_dict)
        return user

    def __str__(self):
        return "<GithubUser {} {}>".format(self.username, self.email)


class SearchApiCallLog(BaseModel):
    for_date = models.DateField()
    count = models.IntegerField(default=0)
