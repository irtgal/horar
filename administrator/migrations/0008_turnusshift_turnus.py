# Generated by Django 3.1.2 on 2020-11-20 10:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0007_auto_20201120_1147'),
    ]

    operations = [
        migrations.AddField(
            model_name='turnusshift',
            name='turnus',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='administrator.turnus'),
        ),
    ]