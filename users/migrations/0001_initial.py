

from django.db import migrations, models
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('text', models.CharField(max_length=250)),
                ('image', sorl.thumbnail.fields.ImageField(upload_to='')),
            ],
        ),
    ]
