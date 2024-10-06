from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static
# Create your models here.


class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='avatars/',null=True, blank=True)
    display_name = models.CharField(max_length=50, null=True, blank=True)  # renamed the field
    email=models.EmailField(max_length=100,unique=True,null=True)
    country=models.CharField(max_length=50,null=True, blank=True)
    created=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return str(self.user)
    
    @property
    def avatar(self):
        try:
            avatar = self.image.url
        except:
            avatar=static('images/avatar_default.svg')
        return avatar
    

    @property
    def name(self):
         return self.display_name 
       