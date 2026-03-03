from django.db import models
from django.template.defaultfilters import slugify
# User model
from django.contrib.auth.models import User



class Userpage(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.owner.get_username())

        super(Userpage, self).save(*args, **kwargs)

    def __str__(self):
        return self.owner.get_username()

class Achievement(models.Model):
    MAX_NAME_LENGTH = 128

    name = models.CharField(max_length=MAX_NAME_LENGTH, unique=True)
    icon = models.ImageField() # TODO Set upload_to= directionary
    earners = models.ManyToManyField(User)

    def __str__(self):
        return self.name

class Book(models.Model):
    MAX_TITLE_LENGTH = 128
    MAX_AUTHOR_LENGTH = 128

    #TODO Figure out how to import the API
    isbn = models.IntegerField(unique=True)
    title = models.CharField(max_length=MAX_TITLE_LENGTH)
    #TODO How to do multivalued fields (more models perhaps)
    author = models.CharField(max_length=MAX_AUTHOR_LENGTH)#ArrayField(models.CharField(max_length=MAX_AUTHOR_LENGTH))
    pages = models.IntegerField()
    blurb = models.TextField()
    cover_image = models.ImageField()
    wishlisted_by = models.ManyToManyField(User, related_name='wishlisted_by')
    read_by = models.ManyToManyField(User, related_name='read_by')

    def __str__(self):
        return self.title

class ProgressRecord(models.Model):
    MAX_NAME_LENGTH = 128

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=MAX_NAME_LENGTH, unique=True)
    stage_final = models.IntegerField()
    stage_current = models.IntegerField()
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

class Details(models.Model):
    book = models.OneToOneField(Book, on_delete=models.CASCADE)
    favourites = models.IntegerField()
    reads = models.IntegerField()
    #ratings = models.ArrayField(models.IntegerField())
    #rating_average = models.IntegerField()
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.book)

        super(Details, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.book)
