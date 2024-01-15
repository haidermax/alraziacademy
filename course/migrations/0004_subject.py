# Generated by Django 4.2.2 on 2023-06-29 11:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('course', '0003_delete_subject'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=250)),
                ('paid', models.BooleanField(default=False)),
                ('price', models.DecimalField(decimal_places=0, max_digits=7)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('grade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.grade')),
                ('members', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mycourses', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
