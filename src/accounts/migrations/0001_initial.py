# Generated by Django 3.0.8 on 2020-07-11 12:43

import accounts.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('register_date', models.DateTimeField(auto_now_add=True)),
                ('country_code', models.CharField(default='+20', max_length=6, verbose_name='كود الدولة')),
                ('phone_number', models.CharField(max_length=13, unique=True, validators=[django.core.validators.RegexValidator(message='رقم الهاتف غير صحيح', regex='^[0][1][2?0?5?1]\\d{8}$')])),
                ('first_name', models.CharField(max_length=50, verbose_name='الاسم الاول')),
                ('last_name', models.CharField(max_length=50, verbose_name='اسم العائلة')),
                ('profile_img', models.ImageField(null=True, upload_to=accounts.models.user_folder_direction, validators=[django.core.validators.validate_image_file_extension], verbose_name='الصورة الشخصية')),
                ('graduate_date', models.DateField(blank=True, null=True, verbose_name='عام التخرج')),
                ('birth_date', models.DateField(blank=True, null=True, validators=[accounts.models.validate_birthdate], verbose_name='تاريخ الميلاد')),
                ('gender', models.CharField(blank=True, choices=[('ذكر', 'ذكر'), ('انثى', 'انثى')], max_length=20, null=True, verbose_name='الجنس')),
                ('office_add', models.CharField(blank=True, max_length=250, null=True, verbose_name='عنوان المكتب')),
                ('blocked_booking', models.BooleanField(default=False)),
                ('phone_verified', models.BooleanField(default=False)),
                ('authy_id', models.CharField(blank=True, max_length=20, null=True)),
                ('send_code', models.BooleanField(default=False)),
                ('is_banned', models.BooleanField(default=False)),
                ('in_review', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('onsite_book', models.BooleanField(default=False)),
                ('phone_book', models.BooleanField(default=False)),
                ('wallet', models.FloatField(blank=True, null=True, verbose_name='المحفظة')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='الدولة')),
                ('slug', models.SlugField(allow_unicode=True, verbose_name='الإسم المختصر')),
            ],
            options={
                'verbose_name': 'countries',
                'verbose_name_plural': 'countries',
            },
        ),
        migrations.CreateModel(
            name='Governorate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='المحافظة')),
                ('slug', models.SlugField(allow_unicode=True, verbose_name='الإسم المختصر')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Country')),
            ],
            options={
                'verbose_name': 'governorates',
                'verbose_name_plural': 'governorates',
            },
        ),
        migrations.CreateModel(
            name='LawyerDegrees',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='درجة القيد')),
                ('slug', models.SlugField(allow_unicode=True, verbose_name='الإسم المختصر')),
            ],
            options={
                'verbose_name': 'Lawyer Degree',
                'verbose_name_plural': 'Lawyer Degrees',
            },
        ),
        migrations.CreateModel(
            name='VerifyLastSentIn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('efforts', models.PositiveIntegerField()),
                ('last_sent', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='last_sent', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'verify code last sent in',
                'verbose_name_plural': 'verify code last sent in',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='المنطقة')),
                ('slug', models.SlugField(allow_unicode=True, verbose_name='الإسم المختصر')),
                ('governorate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Governorate')),
            ],
            options={
                'verbose_name': 'regions',
                'verbose_name_plural': 'regions',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.Country', verbose_name='الدولة'),
        ),
        migrations.AddField(
            model_name='user',
            name='governorate',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.Governorate', verbose_name='المحافظة'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='lawyer_degree',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.LawyerDegrees', verbose_name='درجة القيد'),
        ),
        migrations.AddField(
            model_name='user',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.Region', verbose_name='المقاطعة / المنطقة'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
