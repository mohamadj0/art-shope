# Generated by Django 4.1 on 2022-08-31 06:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_alter_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='is_sub',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='category',
            name='sub_caterory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='scategory', to='home.category'),
        ),
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ManyToManyField(related_name='products', to='home.category'),
        ),
    ]
