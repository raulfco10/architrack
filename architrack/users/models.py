from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.

class Location(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    responsible = models.TextField(max_length=200, blank=True, null=True)
    position_responsible = models.TextField(max_length=500, blank=True, null=True)
    address = models.TextField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return str(self.name)

class Modality(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.name)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    agremiado_number = models.BigIntegerField(blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=500, blank=True, null=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=200, blank=True, null=True)
    mobile = models.CharField(max_length=200, blank=True, null=True)
    #location = models.CharField(max_length=200, blank=True, null=True)
    #location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    #location = models.ManyToManyField('Location', blank=True)
    #modality = models.ManyToManyField('Modality', blank=True)
    short_intro = models.CharField(max_length=200, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to='profiles/', default='profiles/user-default.png')
    degree_card_number = models.CharField(max_length=50, blank=True, null=True, default="0000000")
    request = models.BooleanField(blank=True, null=True)
    veracity_letter = models.BooleanField(blank=True, null=True)
    degree = models.BooleanField(blank=True, null=True)
    photo = models.BooleanField(blank=True, null=True)
    inscription = models.BooleanField(blank=True, null=True)
    annuity = models.BooleanField(blank=True, null=True)
    degree_card = models.BooleanField(blank=True, null=True)
    speciallity_card = models.BooleanField(blank=True, null=True)
    rfc = models.BooleanField(blank=True, null=True)
    proof_of_address = models.BooleanField(blank=True, null=True)
    ife = models.BooleanField(blank=True, null=True)
    curp = models.BooleanField(blank=True, null=True)
    resume = models.BooleanField(blank=True, null=True)
    sat_enrollment = models.BooleanField(blank=True, null=True)
    thesis = models.BooleanField(blank=True, null=True)
    referral_cards = models.BooleanField(blank=True, null=True)
    born_certificate = models.BooleanField(blank=True, null=True)
    municipality_licence = models.BooleanField(blank=True, null=True)
    state_card = models.BooleanField(blank=True, null=True)
    social_github = models.CharField(max_length=200, blank=True, null=True)
    social_facebook = models.CharField(max_length=200, blank=True, null=True)
    social_twitter = models.CharField(max_length=200, blank=True, null=True)
    social_linkedin = models.CharField(max_length=200, blank=True, null=True)
    social_youtube = models.CharField(max_length=200, blank=True, null=True)
    social_website = models.CharField(max_length=200, blank=True, null=True)
    courses = models.ManyToManyField('Course', blank=True)
    training_hours = models.IntegerField(blank=True, null=True)
    years = models.ManyToManyField('Year', blank=True)
    status = models.BooleanField(blank=True, null=True)
    compromiso = models.BooleanField(blank=True, null=True)
    compromiso_date = models.DateTimeField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return str(self.username)

    class Meta:
        ordering = ['created']
    
    @property
    def imageURL(self):
        try:
            url = self.profile_image.url
        except:
            url = ''
        return url



class Skill(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return str(self.name)

class Year(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)


    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    institution = models.CharField(max_length=200, blank=False, null=True)
    hours = models.IntegerField(blank=True, null=True)
    year = models.CharField(max_length=4, blank=True, null=True)
    price = models.FloatField(blank=False, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)


    def __str__(self):
        return self.name


    