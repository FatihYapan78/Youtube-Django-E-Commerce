# Generated by Django 3.2 on 2024-02-19 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppEcommerce', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='brand_en',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='brand',
            name='brand_tr',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='caseshape',
            name='case_shape_en',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='caseshape',
            name='case_shape_tr',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='color',
            name='color_en',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='color',
            name='color_tr',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='gender',
            name='gender_en',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='gender',
            name='gender_tr',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='glassfeature',
            name='glass_feature_en',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='glassfeature',
            name='glass_feature_tr',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='mechanism',
            name='mechanism_en',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='mechanism',
            name='mechanism_tr',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='description_en',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='description_tr',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='model_en',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='model_tr',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='straptype',
            name='strap_type_en',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='straptype',
            name='strap_type_tr',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='style',
            name='style_en',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='style',
            name='style_tr',
            field=models.CharField(max_length=250, null=True),
        ),
    ]
