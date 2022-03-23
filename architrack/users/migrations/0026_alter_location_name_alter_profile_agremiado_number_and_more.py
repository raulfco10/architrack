# Generated by Django 4.0.3 on 2022-03-15 05:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0025_remove_skill_owner_profile_skill'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='agremiado_number',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Numero de Agremiado'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='annuity',
            field=models.BooleanField(blank=True, null=True, verbose_name='Anualidad'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.TextField(blank=True, null=True, verbose_name='Biografia'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='born_certificate',
            field=models.BooleanField(blank=True, null=True, verbose_name='Acta de nacimiento'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='degree',
            field=models.BooleanField(blank=True, null=True, verbose_name='Titulo'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='degree_card',
            field=models.BooleanField(blank=True, null=True, verbose_name='Cedula Federal'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='degree_card_number',
            field=models.CharField(blank=True, default='0000000', max_length=50, null=True, verbose_name='Numero de Cedula'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='email',
            field=models.EmailField(blank=True, max_length=500, null=True, verbose_name='Correo Electronico'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='ife',
            field=models.BooleanField(blank=True, null=True, verbose_name='Identificacion Oficial Vigente'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='inscription',
            field=models.BooleanField(blank=True, null=True, verbose_name='Pago inscripcion'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='mobile',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Celular'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='municipality_licence',
            field=models.BooleanField(blank=True, null=True, verbose_name='Licencia giro municipal'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='name',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Nombre'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Telefono'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.BooleanField(blank=True, null=True, verbose_name='Foto'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(blank=True, default='profiles/user-default.png', null=True, upload_to='profiles/', verbose_name='Foto'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='proof_of_address',
            field=models.BooleanField(blank=True, null=True, verbose_name='Comprobante de domicilio'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='referral_cards',
            field=models.BooleanField(blank=True, null=True, verbose_name='Cartas de referencia'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='request',
            field=models.BooleanField(blank=True, null=True, verbose_name='Solicitud'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='resume',
            field=models.BooleanField(blank=True, null=True, verbose_name='Curriculum'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='sat_enrollment',
            field=models.BooleanField(blank=True, null=True, verbose_name='Alta de Hacienda'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='short_intro',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Descripcion corta'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='skill',
            field=models.ManyToManyField(blank=True, to='users.skill', verbose_name='Especialidades'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='speciallity_card',
            field=models.BooleanField(blank=True, null=True, verbose_name='Cedula Especialidad'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='state_card',
            field=models.BooleanField(blank=True, null=True, verbose_name='Cedula estatal'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='thesis',
            field=models.BooleanField(blank=True, null=True, verbose_name='Libro de arquitectura o Tesis'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='username',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Usuario'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='veracity_letter',
            field=models.BooleanField(blank=True, null=True, verbose_name='Carta de veracidad'),
        ),
        migrations.CreateModel(
            name='LettersHistory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('letterType', models.CharField(choices=[('dro', 'Carta DRO'), ('checklist', 'Carta Checklist'), ('veracidad', 'Carta de Veracidad'), ('compromiso', 'Carta Compromiso')], max_length=50)),
                ('register', models.CharField(blank=True, max_length=200, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.location')),
                ('modality', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.modality')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.profile')),
            ],
        ),
    ]