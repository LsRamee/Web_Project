from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    power = models.CharField(max_length=10)  # 권한

    def __str__(self):
        return self.username

class Post(models.Model):
    postname = models.CharField(max_length=50) #글제목
    contents = models.TextField() #글내용
    writer = models.CharField(max_length=100)
    # 게시글의 제목(postname)이 Post object 대신
    def __str__(self):
        return self.postname

