# Generated by Django 2.0.10 on 2019-02-10 13:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mm', '0005_user_share'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lock_article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lock_article_id', to='mm.Article')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_lock_id', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
