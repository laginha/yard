from django.db import models
from datetime  import datetime, date
        
    
class Author( models.Model ):
    name = models.CharField( max_length=100 )
    gender = models.CharField( max_length=1, 
        choices=(('M', 'male'),('F','female')) )
    birthday = models.DateField( default=datetime.today )
    
    def gender_(self):
        return 'male' if self.gender=='M' else 'female'
    
    def age(self):
        return (date.today()-self.birthday).days / 365
    
    def __str__(self):
        return self.name


class Publishing(models.Model):
    name = models.CharField(unique=True, max_length=100)
    
    def __str__(self):
        return self.name


class Genre( models.Model ):
    name = models.CharField(unique=True, max_length=100)        

    def __str__(self):
        return self.name


class Book( models.Model ):
    author = models.ForeignKey( Author )
    publishing_house = models.ForeignKey( Publishing )
    title = models.CharField( max_length=100 )
    genres = models.ManyToManyField( Genre )
    publication_date = models.DateField( default=datetime.today )
    number_of_pages = models.PositiveIntegerField(blank=True, null=True)
    
    def genres_(self):
        return self.genres.all()
    
    def __str__(self):
        return self.title
