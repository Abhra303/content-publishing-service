# Generated by Django 4.1.5 on 2023-01-15 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Interaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.PositiveIntegerField()),
                ('content_id', models.PositiveIntegerField()),
                ('type', models.CharField(choices=[('R', 'Read'), ('L', 'Like')], max_length=2)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
