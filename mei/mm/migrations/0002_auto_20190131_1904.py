# Generated by Django 2.0.10 on 2019-01-31 11:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mm', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='classify2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='classify_art2', to='mm.Classify'),
        ),
    ]