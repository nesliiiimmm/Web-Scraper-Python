from django.db import models
from django.urls import reverse

# Create your models here.

class post(models.Model):
    title = models.CharField(max_length=120)
    content = models.TextField()
    publishing_date = models.DateField()

    def __str__(self): #objenin title ını göstermek için
        return self.title

    def get_absolute_url(self):
        return reverse('post:detail', kwargs={'id': self.id})
        #return "post/{}".format(self.id)

