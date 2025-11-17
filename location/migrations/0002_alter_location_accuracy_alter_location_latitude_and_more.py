# Generated migration

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='accuracy',
            field=models.DecimalField(decimal_places=2, help_text='GPS accuracy in meters', max_digits=15),
        ),
        migrations.AlterField(
            model_name='location',
            name='latitude',
            field=models.DecimalField(decimal_places=7, help_text='Latitude coordinate (-90 to 90)', max_digits=10),
        ),
        migrations.AlterField(
            model_name='location',
            name='longitude',
            field=models.DecimalField(decimal_places=7, help_text='Longitude coordinate (-180 to 180)', max_digits=11),
        ),
    ]
