from django.db import models
import re


class UserManager(models.Manager):
    def basic_validator(self, data):
        errors = {}
        EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")
        if len(data["first_name"]) < 2:
            errors["first_name"] = "First Name should be minimum 2 characters"
        if len(data["last_name"]) < 2:
            errors["last_name"] = "Last Name should be minimum 2 characters"
        if len(data["password"]) < 8:
            errors["password"] = "Password should be 8 characters minimum"
        if data["password"] != data["passconf"] and data["passconf"] != 0:
            errors["checkpassword"] = "Password should match!"
        if not EMAIL_REGEX.match(data["email"]):
            errors["email"] = "Invalid email address"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Message(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name="messages", on_delete=models.CASCADE)


class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    message = models.ForeignKey(Message, related_name="comments", on_delete=models.CASCADE)
