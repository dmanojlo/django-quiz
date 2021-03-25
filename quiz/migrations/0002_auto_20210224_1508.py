# Generated by Django 3.1.3 on 2021-02-24 14:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='quiz.question'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='text',
            field=models.CharField(max_length=255, verbose_name='Answer'),
        ),
        migrations.AlterField(
            model_name='question',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='quiz.quizname'),
        ),
        migrations.AlterField(
            model_name='quizname',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quiz', to=settings.AUTH_USER_MODEL),
        ),
    ]