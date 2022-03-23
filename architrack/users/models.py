from pyexpat import model
from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.

class Location(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True)
    responsible = models.TextField(max_length=200, blank=True, null=True)
    position_responsible = models.TextField(max_length=500, blank=True, null=True)
    address = models.TextField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return str(self.name)

class Modality(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.name)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    agremiado_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="Numero de Agremiado")
    name = models.CharField(max_length=200, blank=True, null=True, verbose_name="Nombre")
    email = models.EmailField(max_length=500, blank=True, null=True, verbose_name="Correo Electronico")
    username = models.CharField(max_length=200, blank=True, null=True, verbose_name="Usuario")
    phone = models.CharField(max_length=200, blank=True, null=True, verbose_name="Telefono")
    mobile = models.CharField(max_length=200, blank=True, null=True, verbose_name="Celular")
    #location = models.CharField(max_length=200, blank=True, null=True)
    #location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    #location = models.ManyToManyField('Location', blank=True)
    #modality = models.ManyToManyField('Modality', blank=True)
    skill = models.ManyToManyField('Skill', blank=True, verbose_name="Especialidades")
    short_intro = models.CharField(max_length=200, blank=True, null=True, verbose_name="Descripcion corta")
    bio = models.TextField(blank=True, null=True, verbose_name="Biografia")
    profile_image = models.ImageField(null=True, blank=True, upload_to='profiles/', default='profiles/user-default.png', verbose_name="Foto")
    degree_card_number = models.CharField(max_length=50, blank=True, null=True, default="0000000", verbose_name="Numero de Cedula")
    request = models.BooleanField(blank=True, null=True, verbose_name="Solicitud")
    veracity_letter = models.BooleanField(blank=True, null=True, verbose_name="Carta de veracidad")
    degree = models.BooleanField(blank=True, null=True, verbose_name="Titulo")
    photo = models.BooleanField(blank=True, null=True, verbose_name="Foto")
    inscription = models.BooleanField(blank=True, null=True, verbose_name="Pago inscripcion")
    annuity = models.BooleanField(blank=True, null=True, verbose_name="Anualidad")
    degree_card = models.BooleanField(blank=True, null=True, verbose_name="Cedula Federal")
    speciallity_card = models.BooleanField(blank=True, null=True, verbose_name="Cedula Especialidad")
    rfc = models.BooleanField(blank=True, null=True)
    proof_of_address = models.BooleanField(blank=True, null=True, verbose_name="Comprobante de domicilio")
    ife = models.BooleanField(blank=True, null=True, verbose_name="Identificacion Oficial Vigente")
    curp = models.BooleanField(blank=True, null=True)
    resume = models.BooleanField(blank=True, null=True, verbose_name="Curriculum")
    sat_enrollment = models.BooleanField(blank=True, null=True, verbose_name="Alta de Hacienda")
    thesis = models.BooleanField(blank=True, null=True, verbose_name="Libro de arquitectura o Tesis")
    referral_cards = models.BooleanField(blank=True, null=True, verbose_name="Cartas de referencia")
    born_certificate = models.BooleanField(blank=True, null=True, verbose_name="Acta de nacimiento")
    municipality_licence = models.BooleanField(blank=True, null=True, verbose_name="Licencia giro municipal")
    state_card = models.BooleanField(blank=True, null=True, verbose_name="Cedula estatal")
    social_github = models.CharField(max_length=200, blank=True, null=True)
    social_facebook = models.CharField(max_length=200, blank=True, null=True)
    social_twitter = models.CharField(max_length=200, blank=True, null=True)
    social_linkedin = models.CharField(max_length=200, blank=True, null=True)
    social_youtube = models.CharField(max_length=200, blank=True, null=True)
    social_website = models.CharField(max_length=200, blank=True, null=True)
    courses = models.ManyToManyField('Course', blank=True, verbose_name="Cursos tomados")
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
    #owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True, unique=True)
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

class LettersHistory(models.Model):
    LETTER_TYPE = (
        ('dro','Carta DRO'),
        ('checklist','Carta Checklist'),
        ('veracidad','Carta de Veracidad'),
        ('compromiso','Carta Compromiso'),
    )
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    letterType = models.CharField(max_length=50, choices=LETTER_TYPE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    modality = models.ForeignKey(Modality, on_delete=models.CASCADE, null=True, blank=True)
    register = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.register if self.register else ''  

class DroRegister(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    modality = models.ForeignKey(Modality, on_delete=models.CASCADE, null=True, blank=True)
    register = models.CharField(max_length=200, blank=True, null=True)
    status = models.BooleanField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    #class Meta:
    #    unique_together = (('owner','location','modality','register'),)

    def __str__(self):
        return self.register if self.register else ''   




    