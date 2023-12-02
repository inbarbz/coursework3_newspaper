from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# Create your models here.

#create custom user model with the fields date_of_birth, email, profile_image
class CustomUser(AbstractUser):
    date_of_birth = models.DateField(default=None, blank=True, null=True)
    profile_image = models.ImageField(upload_to='images/', blank=True, null=True)
    # add categories field which is a many to many field with the Category model
    categories = models.ManyToManyField('Category', default=None, blank=True, null=True)

    def __str__(self):
        return f"<User: {self.username} : {self.email} : {self.date_of_birth} : {self.categories}>"

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"<Category: {self.name}>"

class Article(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=100)
    content = models.TextField()
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"<Article: {self.title} : {self.category}>"

class Comment(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"<Comment: {self.author} : {self.article.title} : {self.content[:20]}>"
    



       
