# Generated by Django 4.2.2 on 2023-07-02 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0007_lecture_quiz_alter_lecture_attachment_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecture',
            name='description',
            field=models.TextField(),
        ),
    ]
