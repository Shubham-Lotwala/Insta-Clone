from django.db import models
import uuid
from users.models import User


# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=100,blank=False,null=False)
    image=models.URLField(max_length=1000)
    body = models.TextField(max_length=100)
    url=models.URLField(max_length=1000,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    id=models.CharField(max_length=100,default=uuid.uuid4,unique=True,primary_key=True,editable=False)
    likes = models.ManyToManyField(User, related_name='liked_posts',through="LikedPost")
    author = models.ForeignKey(User, on_delete=models.SET_NULL,null=True,related_name='posts',blank=True)


    def __str__(self):
        return str(self.title)
    class Meta:
        ordering = ['-created_at']


class LikedPost(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    created=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.user.username} liked {self.post.title}'


class Comment(models.Model):
    author=models.ForeignKey(User, on_delete=models.SET_NULL,null=True,related_name='comments')
    parent_post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    body=models.CharField(max_length=200)
    likes = models.ManyToManyField(User, related_name='liked_comments',through="LikedComment")
    created=models.DateTimeField(auto_now_add=True)
    id=models.CharField(max_length=100,default=uuid.uuid4,unique=True,primary_key=True,editable=False)


    def __str__(self):
        try:
            return f'{self.author.username}'
        except:
            return f'No Author'
        

    class Meta:
        ordering = ['-created']


class LikedComment(models.Model):
    comment=models.ForeignKey(Comment,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    created=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.user.username} liked {self.comment}'





class Reply(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='replies')
    parent_comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    body = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_replies',through="LikedReplies")
    id = models.CharField(max_length=100, default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        try:
            return f'{self.author.username}'
        except:
            return f'No Author'

    class Meta:
        ordering = ['-created']


class LikedReplies(models.Model):
    reply=models.ForeignKey(Reply,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    created=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.user.username} liked {self.reply}'






    