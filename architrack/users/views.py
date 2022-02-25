from django.contrib.auth import forms
from django.http import request
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile, Skill, Location, Modality
from .forms import CustomUserCreationForm, ProfileForm, SkillForm
from .utils import searchProfiles, paginateProfiles, sendDataDRO
from datetime import datetime
from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, cm
from django.templatetags.static import static
from django.conf import settings
from reportlab.platypus import (BaseDocTemplate, PageTemplate, 
NextPageTemplate, PageBreak, Frame, FrameBreak, Flowable, Paragraph, 
Image, Spacer, TableStyle)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus.tables import Table
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from reportlab.lib import colors
from django.core.files.storage import FileSystemStorage
import pandas as pd

#Diccionarios de días y meses
months = {
    1: "Enero",
    2: "Febrero",
    3: "Marzo",
    4: "Abril",
    5: "Mayo",
    6: "Junio",
    7: "Julio",
    8: "Agosto",
    9: "Septiembre",
    10: "Octubre",
    11: "Noviembre",
    12: "Diciembre",
}

days = {
    0: "Domingo",
    1: "Lunes",
    2: "Martes",
    3: "Miércoles",
    4: "Jueves",
    5: "Viernes",
    6: "Sábado",
}

# Create your views here.

def loginUser(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username=request.POST['username'].lower()
        password=request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        else:
            messages.error(request,'Username OR password is incorrect')

    return render(request, 'users/login_register.html')

def logoutUser(request):
    logout(request)
    messages.info(request, 'User was logged out')
    return redirect('login')

def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User account was created!')
            
            login(request, user)
            return redirect('edit-account')
        else:
            messages.success(request, 'An error has occurred during registration')


    context = {'page': page, 'form': form}
    return render(request, 'users/login_register.html', context)


def profiles(request):

    profiles, search_query = searchProfiles(request)

    custom_range, profiles = paginateProfiles(request, profiles, 3)

    context = {'profiles': profiles, 'search_query': search_query, 'custom_range': custom_range}
    return render(request, 'users/profiles.html', context)

def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)

    topSkills = profile.skill_set.exclude(description__exact="")
    otherSkills = profile.skill_set.filter(description="")
    yearsPaid = profile.years.all()
    courses = profile.courses.all()

    totalTrainingHours = 0

    for course in courses:
        if int(course.year) >= 2021:
            totalTrainingHours += course.hours

    context = {'profile':profile, 'topSkills': topSkills, 'otherSkills': otherSkills, 'yearsPaid':yearsPaid, 'courses': courses, 'totalTrainingHours': totalTrainingHours}
    return render(request, 'users/user-profile.html', context)

@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile

    skills = profile.skill_set.all()
    projects = profile.project_set.all()

    context = {'profile':profile, 'skills':skills, 'projects':projects} 
    return render(request, 'users/account.html', context)

@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    training_hours = 0
    year_flag = False
    
    courses = profile.courses.all()
    for course in courses:
        training_hours += course.hours
    profile.training_hours = training_hours
    years = profile.years.all()
    for year in years:
        if year == datetime.now().year:
            year_flag = True
    profile.status = year_flag

    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')

    context = {'form':form}
    return render(request, 'users/profile_form.html', context)

@login_required(login_url='login')
def editAccountByAdmin(request, pk):
    profile = Profile.objects.get(id=pk) 
    training_hours = 0
    year_flag = False
    
    courses = profile.courses.all()
    for course in courses:
        training_hours += course.hours
    profile.training_hours = training_hours
    years = profile.years.all()
    for year in years:
        if year == datetime.now().year:
            year_flag = True
    profile.status = year_flag

    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')

    context = {'form':form}
    return render(request, 'users/profile_form.html', context)

@login_required(login_url='login')
def droForm(request, pk):
    profile = Profile.objects.get(id=pk) 
    locations = Location.objects.all()
    modalities = Modality.objects.all()
    context = {'profile': profile, 'locations': locations, 'modalities': modalities}
    return render(request, 'users/dro_letter.html', context)

@login_required(login_url='login')
def commitmentForm(request, pk):
    profile = Profile.objects.get(id=pk)
    context = {'profile': profile}
    return render(request, 'users/commitment_letter.html', context)

@login_required(login_url='login')
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skills = Skill.objects.filter(owner=skill.owner).count()
            print(skills)
            if skills < 5:
                skill.save()
                form.save()
                messages.success(request, 'Skill was added successfully!')
            else:
                messages.error(request, 'Esta persona ya tiene 5 especialidades asignadas')
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/skill_form.html', context)

@login_required(login_url='login')
def createSkillAdmin(request, pk):
    profile = Profile.objects.get(id=pk)
    form = SkillForm()

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skills = Skill.objects.filter(owner=skill.owner).count()
            print(skills)
            if skills < 5:
                skill.save()
                form.save()
                messages.success(request, 'Skill was added successfully!')
            else:
                messages.error(request, 'Esta persona ya tiene 5 especialidades asignadas')
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/skill_form.html', context)

@login_required(login_url='login')
def updateSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill was updated successfully!')
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/skill_form.html', context)

@login_required(login_url='login')
def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill was deleted successfully!')
        return redirect('account')
    context = {'object': skill}
    return render(request, 'delete_template.html', context)


def letterDRO(request, pk):
    profile = Profile.objects.get(id=pk)

    context = {'profile':profile}
    return render(request, 'users/dro_letter.html', context)

def checkList(request, pk):
    profile = Profile.objects.get(id=pk)

    skills =  profile.skill_set.all()
    yearsPaid = profile.years.all()
    courses = profile.courses.all()

    context = {'profile':profile, 'skills': skills, 'yearsPaid':yearsPaid, 'courses': courses}
    return render(request, 'users/checklist.html', context)

#------------------------------------------------imports from excel----------------------------------------------#
@login_required(login_url='login')
def import_csv(request):              
    try:
        if request.method == 'POST' and request.FILES['myfile']:
          
            myfile = request.FILES['myfile']
            print(myfile)        
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            excel_file = uploaded_file_url
            print(excel_file) 
            excel_url = str(settings.BASE_DIR) + static(excel_file)
            print(excel_url) 
            #empexceldata = pd.read_csv(excel_url,encoding='utf-8')
            empexceldata = pd.read_csv(excel_url, header=0, names=['num_agremiado', 'nombre', 'email', 'username', 'telefono','celular'],encoding='latin-1')
            dbframe = empexceldata
            print(dbframe)
            for dbframe in dbframe.itertuples():
                
                #obj = Profile.objects.create(agremiado_number=dbframe.num_agremiado, name=dbframe.nombre, email=dbframe.email, username=dbframe.username, phone=dbframe.telefono, mobile=dbframe.celular)
                obj = User.objects.create(username=dbframe.username, first_name=dbframe.nombre, email=dbframe.email, password="testuser1234", is_staff=False)
                print(obj)
                obj.save()

                profile = Profile.objects.get(username=obj.username)
                profile.agremiado_number = dbframe.num_agremiado
                profile.save()
    
            return render(request, 'users/importexcel.html', {
                'uploaded_file_url': uploaded_file_url
            })    
    except Exception as identifier:            
        print(identifier)
     
    return render(request, 'users/importexcel.html',{})

#-------------------------------------------------------------------------------------------#

def veracity_pdf(request, pk):
    now = datetime.now()
    response = HttpResponse(content_type='application/PDF')
    d = datetime.today().strftime('%Y-%m-%d')
    response['Content-Disposition'] = f'inline; filename="{d}.pdf"'

    w, h = letter

    buffer = BytesIO()


    p = canvas.Canvas(buffer, pagesize=letter)

    profile = Profile.objects.get(id=pk)

    context = {'profile':profile}


    p.setFillColorRGB(0.29296875, 0.453125, 0.609365)

    x= 0
    y= h - 80
    p.rect(x, y, 400, 60, fill=1)

    p.setFont("Helvetica", 12, leading=None)
    p.setFillColorRGB(0,0,0)
    p.drawString(250, h-110, "Carta de veracidad {}".format(now.year))
 
    logo = str(settings.BASE_DIR) + static("/images/LOGO_LETRAS_Blanco.png")

    p.drawImage(logo, x+290, h-70, 80, 40, mask='auto')

    text_president_name = "Arq. Laila Pérez Ochoa"
    style_president_name = getSampleStyleSheet()["Heading2"]
    style_president_name.alignment = TA_LEFT
    para = Paragraph(text_president_name, style_president_name)
    x, y = para.wrap(18*cm, 10*cm)
    y = h - 170
    para.drawOn(p, 1*cm, y)

    text_president_title = "Presidente Colegio de Arquitectos del estado de Jalisco, A.C. 2021-2024"
    style_president_title = getSampleStyleSheet()["Heading4"]
    style_president_title.alignment = TA_LEFT
    para = Paragraph(text_president_title, style_president_title)
    x, y = para.wrap(18*cm, 10*cm)
    y = h - 185
    para.drawOn(p, 1*cm, y)

    main_text = "El que suscribe la presente nombre_agremiado Identificándome con número de cedula Estatal "\
    "profesional cedula_profesional Manifiesto bajo protesta de decir la verdad que los documentos que envió "\
    "vía correo electrónico al responsable del área de agremiados del Colegio de Arquitectos del "\
    "Estado de Jalisco A. C., son fidedignos y copia fiel de los originales que en este momento "\
    "presento para su cotejo, mismos que solicito sean integrados a mi expediente personal."
    style = getSampleStyleSheet()["Normal"]
    style.alignment = TA_JUSTIFY
    style.leading = 20
    

    main_text = main_text.replace("\n", "<br />")
    main_text = main_text.replace("nombre_agremiado", profile.name)
    if profile.degree_card_number:
        main_text = main_text.replace("cedula_profesional", profile.degree_card_number)
    para = Paragraph(main_text, style)
    x, y = para.wrap(18*cm, 10*cm)
    y = h - 300
    para.drawOn(p, 1*cm, y)

    
    month_number = now.month
    day_number = int(now.strftime("%w"))

    day = days.get(day_number)
    month = months.get(month_number)


    location_text = """Atentamente: 
        Guadalajara, Jalisco A: current_date"""
    location_style = getSampleStyleSheet()["Normal"]
    location_style.alignment = TA_CENTER
    location_style.leading = 15
    location_text = location_text.replace("\n", "<br />")
    location_text = location_text.replace("current_date", "{}, {} de {} del {}".format(day, now.day, month, now.year))
    
    para = Paragraph(location_text, location_style)
    x, y = para.wrap(18*cm, 10*cm)
    y = h - 400
    para.drawOn(p, 1*cm, y)


    name_text = profile.name
    name_style = getSampleStyleSheet()["Title"]
    name_style.alignment = TA_CENTER
    name_style.fontSize = 12
    
    para = Paragraph(name_text, name_style)
    x, y = para.wrap(18*cm, 10*cm)
    y = h - 530
    para.drawOn(p, 1*cm, y)


    note_text = """<b>Nota:</b> colocar arriba de su nombre su firma autógrafa tal cual aparece en sus documentos de 
    identificación oficial"""
    note_style = getSampleStyleSheet()["Normal"]
    note_style.alignment = TA_LEFT
    note_style.leading = 15
    
    
    para = Paragraph(note_text, note_style)
    x, y = para.wrap(18*cm, 10*cm)
    y = h - 550
    para.drawOn(p, 1.5*cm, y)


    privacity_text = "AVISO DE PRIVACIDAD"
    privacity_style = getSampleStyleSheet()["Title"]
    privacity_style.alignment = TA_CENTER
    privacity_style.fontSize = 8
    
    para = Paragraph(privacity_text, privacity_style)
    x, y = para.wrap(18*cm, 10*cm)
    y = h - 650
    para.drawOn(p, 1*cm, y)

    privacity_style2 = getSampleStyleSheet()["Normal"]
    privacity_style2.alignment = TA_JUSTIFY
    privacity_style2.leading = 10
    privacity_style2.bulletFontName = 'Times-Roman'
    privacity_style2.fontSize = 6
    privacity_style2.bulletFontSize = 8
    privacity_style2.bulletIndent = 25
    privacity_text2 = """Colegio del Arquitectos del Estado de Jalisco A.C., con domicilio en calle Pedro Moreno 1612, colonia americana, ciudad 
    Guadalajara, municipio o delegacion Guadalajara, c.p. 44140, en la entidad de Jalisco, país México, utilizará sus datos personales
    recabados para:"""
    para = Paragraph(privacity_text2, privacity_style2)
    x, y = para.wrap(12*cm, 10*cm)
    y = h - 680
    para.drawOn(p, 4.5*cm, y)

    privacity_text3 = """<bullet>&bull</bullet>Emisión de Carta de Director Responsable"""
    para = Paragraph(privacity_text3, privacity_style2)
    x, y = para.wrap(12*cm, 10*cm)
    y = h - 690
    para.drawOn(p, 4.5*cm, y)

    privacity_text4 = """<bullet>&bull</bullet>Generación de Expedientes de Agremiados"""
    para = Paragraph(privacity_text4, privacity_style2)
    x, y = para.wrap(12*cm, 10*cm)
    y = h - 700
    para.drawOn(p, 4.5*cm, y)
    
    privacity_text5 = """Para más información acerca del tratamiento y de los derechos que puede hacer valer, usted puede acceder al aviso de
    privacidad integral a través de: En las instalaciones del Colegio de Arquitectos del Estado de Jalisco A.C. o por medio de correo
    electrónico"""
    para = Paragraph(privacity_text5, privacity_style2)
    x, y = para.wrap(12*cm, 10*cm)
    y = h - 730
    para.drawOn(p, 4.5*cm, y)

    x = 120
    y = h - 735
    p.rect(x, y, 355, 90, fill=0)

    p.setTitle(f'Report on {d}')
    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response

def commitment_pdf(request, pk):
    now = datetime.now()
    response = HttpResponse(content_type='application/PDF')
    d = datetime.today().strftime('%Y-%m-%d')
    response['Content-Disposition'] = f'inline; filename="{d}.pdf"'

    w, h = letter

    buffer = BytesIO()


    p = canvas.Canvas(buffer, pagesize=letter)

    profile = Profile.objects.get(id=pk)

    profile.compromiso = True
    profile.compromiso_date = datetime(now.year, now.month, now.day, now.hour, now.minute)
    profile.save()

    p.setFillColorRGB(0.29296875, 0.453125, 0.609365)

    x= 0
    y= h - 80
    p.rect(x, y, 400, 60, fill=1)

    p.setFont("Helvetica", 12, leading=None)
    p.setFillColorRGB(0,0,0)
    p.drawString(170, h-110, "Carta Compromiso de Actualización Profesional {}".format(now.year))
 
    logo = str(settings.BASE_DIR) + static("/images/LOGO_LETRAS_Blanco.png")

    p.drawImage(logo, x+290, h-70, 80, 40, mask='auto')

    text_president_name = "Arq. Laila Pérez Ochoa"
    style_president_name = getSampleStyleSheet()["Heading2"]
    style_president_name.alignment = TA_LEFT
    para = Paragraph(text_president_name, style_president_name)
    x, y = para.wrap(18*cm, 10*cm)
    y = h - 170
    para.drawOn(p, 1*cm, y)

    text_president_title = "Presidente Colegio de Arquitectos del estado de Jalisco, A.C. 2021-2024"
    style_president_title = getSampleStyleSheet()["Heading4"]
    style_president_title.alignment = TA_LEFT
    para = Paragraph(text_president_title, style_president_title)
    x, y = para.wrap(18*cm, 10*cm)
    y = h - 185
    para.drawOn(p, 1*cm, y)

    main_text = "El que suscribe la presente. nombre_agremiado Identificándome Con número de cedula Estatal Expreso mi"\
    "compromiso para acreditar ante el Colegio de Arquitectos del Estado de Jalisco A.C. un total de <b>150</b> "\
    "horas de Capacitación para garantizar la <b>Actualización Profesional</b>."
    style = getSampleStyleSheet()["Normal"]
    style.alignment = TA_JUSTIFY
    style.leading = 20
    

    main_text = main_text.replace("\n", "<br />")
    main_text = main_text.replace("nombre_agremiado", profile.name)
    if profile.degree_card_number:
        main_text = main_text.replace("cedula_profesional", profile.degree_card_number)
    para = Paragraph(main_text, style)
    x, y = para.wrap(18*cm, 10*cm)
    y = h - 300
    para.drawOn(p, 1*cm, y)

    second_text = "Asimismo, con fundamento en lo dispuesto en artículo 37 fracciones III, V, XI Así como XXII de la"\
    "misma Ley para el Ejercicio de las Actividades Profesionales del Estado de Jalisco me comprmeto a "\
    "entregar constancia de las anteriores horas de capacitación al Colegio de Arquitectos del Estado de "\
    "Jalisco A.C. en plazo no mayor a tres meses posteriores a la fecha en que concluye este "\
    "compromiso, asumiendo íntegramente cualquier sanción que tenga a bien establecer el Colegio de "\
    "Arquitectos del Estado de Jalisco A.C. "\
    "La actualización Profesional a que hace referencia el articulo 61 de la Ley para el ejercicio de las "\
    "actividades profesionales del Estado de Jalisco debe estar cubierta <b>Antes del 31 de Diciembre del anio_actual</b>."    
    style = getSampleStyleSheet()["Normal"]
    style.alignment = TA_JUSTIFY
    style.leading = 20
    

    second_text = second_text.replace("\n", "<br />")
    second_text = second_text.replace("anio_actual", str(now.year))
    para = Paragraph(second_text, style)
    x, y = para.wrap(18*cm, 10*cm)
    y = h - 450
    para.drawOn(p, 1*cm, y)

    
    month_number = now.month
    day_number = int(now.strftime("%w"))

    day = days.get(day_number)
    month = months.get(month_number)


    location_text = """Atentamente: 
        Guadalajara, Jalisco A: current_date"""
    location_style = getSampleStyleSheet()["Normal"]
    location_style.alignment = TA_CENTER
    location_style.leading = 15
    location_text = location_text.replace("\n", "<br />")
    location_text = location_text.replace("current_date", "{}, {} de {} del {}".format(day, now.day, month, now.year))
    
    para = Paragraph(location_text, location_style)
    x, y = para.wrap(18*cm, 10*cm)
    y = h - 500
    para.drawOn(p, 1*cm, y)


    name_text = profile.name
    name_style = getSampleStyleSheet()["Title"]
    name_style.alignment = TA_CENTER
    name_style.fontSize = 12
    
    para = Paragraph(name_text, name_style)
    x, y = para.wrap(18*cm, 10*cm)
    y = h - 630
    para.drawOn(p, 1*cm, y)


    note_text = """<b>_______________________________________________________</b>"""
    note_style = getSampleStyleSheet()["Normal"]
    note_style.alignment = TA_LEFT
    note_style.leading = 15
    
    
    para = Paragraph(note_text, note_style)
    x, y = para.wrap(18*cm, 10*cm)
    y = h - 720
    para.drawOn(p, 5*cm, y)


    note_text = """<b>Firme aquí</b>"""
    note_style = getSampleStyleSheet()["Normal"]
    note_style.alignment = TA_LEFT
    note_style.leading = 15
    
    
    para = Paragraph(note_text, note_style)
    x, y = para.wrap(18*cm, 10*cm)
    y = h - 750
    para.drawOn(p, 9.1*cm, y)

    p.setTitle(f'Report on {d}')
    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response

def dro_pdf(request, pk):
    now = datetime.now()
    response = HttpResponse(content_type='application/PDF')
    d = datetime.today().strftime('%Y-%m-%d')
    response['Content-Disposition'] = f'inline; filename="{d}.pdf"'

    w, h = letter

    buffer = BytesIO()


    p = canvas.Canvas(buffer, pagesize=letter)

    #profile = Profile.objects.get(id=pk)

    profile, location, modality = sendDataDRO(request, pk)

    context = {'profile':profile, 'location': location, 'modality': modality}


    p.setFillColorRGB(0.29296875, 0.453125, 0.609365)

    x= 0
    y= h - 80
    p.rect(x, y, 400, 60, fill=1)

    p.setFont("Helvetica", 12, leading=None)
    p.setFillColorRGB(0,0,0)

    logo = str(settings.BASE_DIR) + static("/images/LOGO_LETRAS_Blanco.png")

    p.drawImage(logo, x+290, h-70, 80, 40, mask='auto')

    text_responsible_name = "<b>" + location.responsible + "</b>"
    style_responsible_name = getSampleStyleSheet()["Normal"]
    style_responsible_name.alignment = TA_LEFT
    para = Paragraph(text_responsible_name, style_responsible_name)
    x, y = para.wrap(18*cm, 10*cm)
    y = h - 150
    para.drawOn(p, 1*cm, y)

    text_responsible_title = "<b>" + location.position_responsible + "</b>"
    style_responsible_title = getSampleStyleSheet()["Normal"]
    style_responsible_title.alignment = TA_LEFT
    para = Paragraph(text_responsible_title, style_responsible_title)
    x, y = para.wrap(18*cm, 10*cm)
    y = h - 165
    para.drawOn(p, 1*cm, y)

    #text_responsible_title = "<b>De Obras Públicas de {}, Jalisco.</b>".format(location)
    #style_responsible_title = getSampleStyleSheet()["Normal"]
    #style_responsible_title.alignment = TA_LEFT
    #para = Paragraph(text_responsible_title, style_responsible_title)
    #x, y = para.wrap(18*cm, 10*cm)
    #y = h - 180
    #para.drawOn(p, 1*cm, y)

    text_presente = "Presente:"
    style_presente = getSampleStyleSheet()["Normal"]
    style_presente.alignment = TA_LEFT
    para = Paragraph(text_presente, style_presente)
    x, y = para.wrap(18*cm, 10*cm)
    y = h - 210
    para.drawOn(p, 1*cm, y)

    main_text = "El Colegio de Arquitectos del Estado de Jalisco, A.C con fundamento en los artículos 347, 348, 349, 350,351 "\
    "y 352 del Código Urbano del Estado de Jalisco y el artículo 37 de la Ley para el ejercicio de  las Actividades "\
    "Profesionales del Estado de Jalisco, así como el artículo 21 de los estatutos de este Colegio. Hace constar "\
    "que el/la:"
    style = getSampleStyleSheet()["Normal"]
    style.alignment = TA_JUSTIFY
    style.leading = 20
    
    main_text = main_text.replace("\n", "<br />")
    para = Paragraph(main_text, style)
    x, y = para.wrap(18*cm, 10*cm)
    y = h - 300
    para.drawOn(p, 1*cm, y)

    text_name = "<b>Arq. " + profile.name + "</b>"
    style_name = getSampleStyleSheet()["Normal"]
    style_name.alignment = TA_LEFT
    para = Paragraph(text_name, style_name)
    x, y = para.wrap(18*cm, 10*cm)
    y = h - 330
    para.drawOn(p, 1*cm, y)

    text_data = "No. Agremiado: <b>" + str(profile.agremiado_number) + "</b>"
    style_data = getSampleStyleSheet()["Normal"]
    style_data.alignment = TA_LEFT
    para = Paragraph(text_data, style_data)
    x, y = para.wrap(18*cm, 10*cm)
    y = h - 360
    para.drawOn(p, 1*cm, y)

    text_data = "Solicita su <b>Actualización / Refrendo </b>"
    style_data = getSampleStyleSheet()["Normal"]
    style_data.alignment = TA_LEFT
    para = Paragraph(text_data, style_data)
    x, y = para.wrap(18*cm, 10*cm)
    y = h - 390
    para.drawOn(p, 1*cm, y)

    text_data = "Registro: <b>drz-2108</b>"
    style_data = getSampleStyleSheet()["Normal"]
    style_data.alignment = TA_LEFT
    para = Paragraph(text_data, style_data)
    x, y = para.wrap(18*cm, 10*cm)
    y = h - 420
    para.drawOn(p, 1*cm, y)

    text_data = "Como director responsable en la modalidad en: <b>" + modality + "</b>"
    style_data = getSampleStyleSheet()["Normal"]
    style_data.alignment = TA_LEFT
    para = Paragraph(text_data, style_data)
    x, y = para.wrap(18*cm, 10*cm)
    y = h - 450
    para.drawOn(p, 1*cm, y)

    text_data = "Domicilio: <b>" + location.address + "</b>"
    style_data = getSampleStyleSheet()["Normal"]
    style_data.alignment = TA_LEFT
    para = Paragraph(text_data, style_data)
    x, y = para.wrap(18*cm, 10*cm)
    y = h - 480
    para.drawOn(p, 1*cm, y)

    text_data = "Teléfono: <b>" + str(profile.phone) + "</b>"
    style_data = getSampleStyleSheet()["Normal"]
    style_data.alignment = TA_LEFT
    para = Paragraph(text_data, style_data)
    x, y = para.wrap(18*cm, 10*cm)
    y = h - 510
    para.drawOn(p, 1*cm, y)

    text_data = "Celular: <b>" + str(profile.mobile) + "</b>"
    style_data = getSampleStyleSheet()["Normal"]
    style_data.alignment = TA_LEFT
    para = Paragraph(text_data, style_data)
    x, y = para.wrap(18*cm, 10*cm)
    y = h - 540
    para.drawOn(p, 1*cm, y)

    text_data = "E-Mail: <b>" + profile.email + "</b>"
    style_data = getSampleStyleSheet()["Normal"]
    style_data.alignment = TA_LEFT
    para = Paragraph(text_data, style_data)
    x, y = para.wrap(18*cm, 10*cm)
    y = h - 570
    para.drawOn(p, 1*cm, y)

    #text_data = "Carta con vigencia del año en curso"
    #style_data = getSampleStyleSheet()["Normal"]
    #style_data.alignment = TA_LEFT
    #para = Paragraph(text_data, style_data)
    #x, y = para.wrap(18*cm, 10*cm)
    #y = h - 600
    #para.drawOn(p, 1*cm, y)

    slogan_text = '''ATENTAMENTE: 
        <b><i>"LOS ARQUITECTOS AL SERVICIO DE LA COLECTIVIDAD"</i></b>
        Casa Cristo de Luis Barragán, Monumento Artístico de la Nación'''
    slogan_style = getSampleStyleSheet()["Normal"]
    slogan_style.alignment = TA_CENTER
    slogan_style.leading = 15
    slogan_text = slogan_text.replace("\n", "<br />")
    
    
    para = Paragraph(slogan_text, slogan_style)
    x, y = para.wrap(18*cm, 10*cm)
    y = h - 660
    para.drawOn(p, 1*cm, y)


    president_text = '''<b>Arq. Laila Pérez Ochoa</b>
        <i>Presidente Consejo Directivo 2021-2024
        Colegio de Arquitectos del Estado de Jalisco, A.C.</i>'''
    president_style = getSampleStyleSheet()["Normal"]
    president_style.alignment = TA_CENTER
    president_style.leading = 15
    president_text = president_text.replace("\n", "<br />")
    
    
    para = Paragraph(president_text, president_style)
    x, y = para.wrap(18*cm, 10*cm)
    y = h - 720
    para.drawOn(p, 1*cm, y)

    text_data = "Carta con vigencia del año en curso: <i>Gualajara, Jalisco</i>. " + str(now.day) + "/" + str(now.month) + "/" + str(now.year)
    style_data = getSampleStyleSheet()["Normal"]
    style_data.alignment = TA_LEFT
    para = Paragraph(text_data, style_data)
    x, y = para.wrap(18*cm, 10*cm)
    y = h - 760
    para.drawOn(p, 1*cm, y)

    

    x= 165
    y= h - 400
    #logo = str(settings.BASE_DIR) + static(profile.profile_image.url)
    logo = profile.profile_image.url
    p.drawImage(logo, x+290, y, 80, 80, mask='auto')

    

    p.setTitle(f'Report on {d}')
    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response

def checklist_pdf(request, pk):
    now = datetime.now()
    response = HttpResponse(content_type='application/PDF')
    d = datetime.today().strftime('%Y-%m-%d')
    response['Content-Disposition'] = f'inline; filename="{d}.pdf"'

    w, h = letter

    buffer = BytesIO()


    p = canvas.Canvas(buffer, pagesize=letter)

    profile = Profile.objects.get(id=pk)

    skills = profile.skill_set.all()

    yearsPaid = profile.years.all()

    p.setFillColorRGB(0.29296875, 0.453125, 0.609365)

    x= 25
    y= h - 80
    p.rect(x, y, 550, 40, fill=1)

    p.setFont("Helvetica", 12, leading=None)
    p.setFillColorRGB(0,0,0)

    logo = str(settings.BASE_DIR) + static("/images/LOGO_LETRAS_Blanco.png")

    p.drawImage(logo, x+480, h-75, 60, 30, mask='auto')

    x= 25
    y= h - 160
    #logo = str(settings.BASE_DIR) + static(profile.profile_image.url)
    logo = profile.profile_image.url
    p.drawImage(logo, x, y, 80, 80, mask='auto')

    p.setFillColorRGB(0.501, 0.505, 0.494)

    x= 105
    y= h - 120
    p.rect(x, y, 117, 40, fill=1)

    x= 105
    y= h - 160
    p.rect(x, y, 117, 40, fill=1)

    p.setFillColorRGB(0.882, 0.878, 0.878)

    x= 105
    y= h - 120
    p.rect(x + 117, y, 158, 40, fill=1)

    x= 105
    y= h - 160
    p.rect(x + 117, y, 118, 40, fill=1)

    #––––––––––––––––––––––––––––––––––––––––––––––––––––––

    p.setFillColorRGB(0.501, 0.505, 0.494)

    x= 105
    y= h - 120
    p.rect(x + 275, y, 117, 40, fill=1)

    x= 105
    y= h - 160
    p.rect(x + 200, y, 117, 40, fill=1)

    p.setFillColorRGB(0.882, 0.878, 0.878)

    x= 105
    y= h - 120
    p.rect(x + 352, y, 118, 40, fill=1)

    x= 105
    y= h - 160
    p.rect(x + 317, y, 153, 40, fill=1)

    text_name = "<b>Nombre:</b>"
    style_name = getSampleStyleSheet()["Normal"]
    style_name.alignment = TA_LEFT
    para = Paragraph(text_name, style_name)
    x, y = para.wrap(18*cm, 4*cm)
    y = h - 105
    para.drawOn(p, 4.8*cm, y)

    text_name = profile.name
    style_name = getSampleStyleSheet()["Normal"]
    style_name.alignment = TA_LEFT
    para = Paragraph(text_name, style_name)
    x, y = para.wrap(18*cm, 4*cm)
    y = h - 105
    para.drawOn(p, 8*cm, y)

    text_fecha = "<b>Fecha:</b>"
    style_fecha = getSampleStyleSheet()["Normal"]
    style_fecha.alignment = TA_LEFT
    para = Paragraph(text_fecha, style_fecha)
    x, y = para.wrap(18*cm, 4*cm)
    y = h - 105
    para.drawOn(p, 14.2*cm, y)

    text_fecha = str(now.day) + "/" + str(now.month) + "/" + str(now.year)
    style_fecha = getSampleStyleSheet()["Normal"]
    style_fecha.alignment = TA_LEFT
    para = Paragraph(text_fecha, style_fecha)
    x, y = para.wrap(18*cm, 4*cm)
    y = h - 105
    para.drawOn(p, 17.5*cm, y)

    text_agremiado = "<b>Num. Agremiado:</b>"
    style_agremiado = getSampleStyleSheet()["Normal"]
    style_agremiado.alignment = TA_LEFT
    para = Paragraph(text_agremiado, style_agremiado)
    x, y = para.wrap(18*cm, 10*cm)
    y = h - 145
    para.drawOn(p, 4.3*cm, y)

    text_agremiado = ""
    if profile.agremiado_number :
        text_agremiado = str(profile.agremiado_number)
    style_agremiado = getSampleStyleSheet()["Normal"]
    style_agremiado.alignment = TA_LEFT
    para = Paragraph(text_agremiado, style_agremiado)
    x, y = para.wrap(18*cm, 4*cm)
    y = h - 145
    para.drawOn(p, 8*cm, y)

    text_anualidades = "<b>Anualidades:</b>"
    style_anualidades = getSampleStyleSheet()["Normal"]
    style_anualidades.alignment = TA_LEFT
    para = Paragraph(text_anualidades, style_anualidades)
    x, y = para.wrap(18*cm, 4*cm)
    y = h - 145
    para.drawOn(p, 11.7*cm, y)

    text_anualidades = ""
    for year in yearsPaid:
        if text_anualidades == "":
            text_anualidades = str(year)
        else:
            text_anualidades = text_anualidades + "-" + str(year)
    style_anualidades = getSampleStyleSheet()["Normal"]
    style_anualidades.alignment = TA_LEFT
    para = Paragraph(text_anualidades, style_anualidades)
    x, y = para.wrap(18*cm, 4*cm)
    y = h - 145
    para.drawOn(p, 15.2*cm, y)

    styles = getSampleStyleSheet()
    style = styles["BodyText"]

    header = Paragraph("<bold><font size=15>Documentación</font></bold>", style)
    rowSolicitud = ['1', 'Solicitud', profile.request]
    rowVeracity = ['2', 'carta de veracidad', profile.veracity_letter]
    rowDegree = ['3','Titulo', profile.degree]
    rowPhoto = ['4','Foto digital', profile.photo]
    rowInscription = ['5','Pago inscripcion', profile.inscription]
    rowAnnuity = ['6','Pago Anualidad', profile.annuity]
    rowDegreeCard = ['7','Cedula Federal', profile.degree_card]
    rowSpecialty = ['8','Cedula Especialidad', profile.speciallity_card]
    rowRFC = ['9','RFC', profile.rfc]
    rowProofOfAddress = ['10','comprobante Domicilio', profile.proof_of_address]
    rowIFE = ['11','Identificacion Oficial Vigente', profile.ife]
    rowCURP = ['12','Curp', profile.curp]
    rowResume = ['13','Curriculum', profile.resume]
    rowSAT = ['14','Alta de Hacienda', profile.sat_enrollment]
    rowThesis = ['15','Libro de arquitectura / Tesis', profile.thesis]
    rowReferralCards = ['16','2 cartas de refencia', profile.referral_cards]
    rowBornCertificate = ['17','Acta de nacimiento', profile.born_certificate]
    rowMunicipalityLicence = ['18','Licencia de Giro Municipal', profile.municipality_licence]
    rowStateCard = ['19','Cedula estatal', profile.state_card]


    data = []
    data.append(convertBoolean(rowSolicitud))
    data.append(convertBoolean(rowVeracity))
    data.append(convertBoolean(rowDegree))
    data.append(convertBoolean(rowPhoto))
    data.append(convertBoolean(rowInscription))
    data.append(convertBoolean(rowAnnuity))
    data.append(convertBoolean(rowDegreeCard))
    data.append(convertBoolean(rowSpecialty))
    data.append(convertBoolean(rowRFC))
    data.append(convertBoolean(rowProofOfAddress))
    data.append(convertBoolean(rowIFE))
    data.append(convertBoolean(rowCURP))
    data.append(convertBoolean(rowResume))
    data.append(convertBoolean(rowSAT))
    data.append(convertBoolean(rowThesis))
    data.append(convertBoolean(rowReferralCards))
    data.append(convertBoolean(rowBornCertificate))
    data.append(convertBoolean(rowMunicipalityLicence))
    data.append(convertBoolean(rowStateCard))

    t = Table(data)
    t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.25, colors.black),
                        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black)]))
    data_len = len(data)

    for each in range(data_len):
        if each % 2 == 0:
            bg_color = colors.whitesmoke
        else:
            bg_color = colors.lightgrey

        t.setStyle(TableStyle([('BACKGROUND', (0, each), (-1, each), bg_color)]))

    aW = 40
    aH = 620

    w, h = header.wrap(18*cm, 4*cm)
    header.drawOn(p, .9*cm, aH)
    aH = aH - h
    w, h = t.wrap(aW, aH)
    t.drawOn(p, .9*cm, aH-h)

    #x, y = para.wrap(18*cm, 4*cm)
    #y = h - 145
    #para.drawOn(p, 15.2*cm, y)

    courses = profile.courses.all()
    header = Paragraph("<bold><font size=12>Cursos</font></bold>", style)
    dataTraining = [['No','Hrs','Año','Concepto','Institución']]
    totalhour = 0
    for idx, obj in enumerate(courses):
        row = []
        totalhour += obj.hours
        row.append(idx+1)
        row.append(obj.hours)
        row.append(obj.year)
        row.append(obj.description)
        row.append(obj.institution)
        dataTraining.append(row) 

    row = ['Total', totalhour, 'Horas']
    dataTraining.append(row)

    t = Table(dataTraining)
    t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.25, colors.black),
                        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black)]))
    data_len_train = len(dataTraining)

    for each in range(data_len_train):
        if each % 2 == 0:
            bg_color = colors.whitesmoke
        else:
            bg_color = colors.lightgrey

        t.setStyle(TableStyle([('BACKGROUND', (0, each), (-1, each), bg_color)]))

    aW = 40
    aH = 620

    w, h = header.wrap(18*cm, 4*cm)
    header.drawOn(p, 8*cm, 615)
    aH = aH - h
    w, h = t.wrap(aW, aH)
    t.drawOn(p, 8*cm, aH-h)

    header = Paragraph("<bold><font size=12>ESPECIALIDADES</font></bold>", style)
    dataSpecialty = []
    for idx, obj in enumerate(skills):
        row = []
        row.append(idx+1)
        row.append(obj.name)
        dataSpecialty.append(row) 

    if len(dataSpecialty) > 0:
        t = Table(dataSpecialty)
        t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.25, colors.black),
                            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black)]))
        data_len = len(dataSpecialty)

        for each in range(data_len):
            if each % 2 == 0:
                bg_color = colors.whitesmoke
            else:
                bg_color = colors.lightgrey

            t.setStyle(TableStyle([('BACKGROUND', (0, each), (-1, each), bg_color)]))

        aW = 40
        aH = 620 - (data_len_train * 30)

        w, h = header.wrap(18*cm, 4*cm)
        header.drawOn(p, 8*cm, 615 - (data_len_train * 30))
        aH = aH - h
        w, h = t.wrap(aW, aH)
        t.drawOn(p, 8*cm, aH-h)

#---------------------------------------------------------------------------------------
    styles = getSampleStyleSheet()
    style = styles["BodyText"]

    header = Paragraph("<bold><font size=12>Carta Compromiso</font></bold>", style)

    rowCompromiso = ['1', 'Tiene Carta Compromiso', profile.compromiso] 
    #rowCompromisoDate = ['1', 'Tiene Carta Compromiso', profile.compromiso_date]    

    data = []
    data.append(convertBoolean(rowCompromiso))
    #data.append(rowCompromisoDate)

    t = Table(data)
    t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.25, colors.black),
                        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black)]))
    data_len = len(data)

    for each in range(data_len):
        if each % 2 == 0:
            bg_color = colors.whitesmoke
        else:
            bg_color = colors.lightgrey

        t.setStyle(TableStyle([('BACKGROUND', (0, each), (-1, each), bg_color)]))

    aW = 40
    aH = 620 - (data_len_train * 30)

    w, h = header.wrap(18*cm, 4*cm)
    header.drawOn(p, 13*cm, 615 - (data_len_train * 30))
    aH = aH - h
    w, h = t.wrap(aW, aH)
    t.drawOn(p, 13*cm, aH-h)

#---------------------------------------------------------------------------------------------------------------

    p.setTitle(f'Report on {d}')
    p.showPage()
    p.save()
    
    
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response

def convertBoolean(lista):
    #print(lista[2])
    if lista[2] == True:
        lista[2] = 'Si'
    else:
        lista[2] = 'No'
    return lista


