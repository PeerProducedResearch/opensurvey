# Generated by Django 3.0.6 on 2020-05-18 10:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('openhumans', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SurveyAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('survey_token', models.BooleanField(blank=True)),
                ('member', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='openhumans.OpenHumansMember')),
            ],
        ),
    ]