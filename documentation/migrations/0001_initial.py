# Generated by Django 3.1.3 on 2021-03-31 17:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='interface',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('implementing_class', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=10000)),
            ],
        ),
        migrations.CreateModel(
            name='project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='method',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('header', models.CharField(max_length=100)),
                ('returns', models.CharField(max_length=200)),
                ('updates', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=10000)),
                ('builder_handle', models.CharField(max_length=200)),
                ('isCodeWritten', models.BooleanField(default=False)),
                ('isCodeTested', models.BooleanField(default=False)),
                ('isCodeUsable', models.BooleanField(default=False)),
                ('interface', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='methods', to='documentation.interface')),
            ],
        ),
        migrations.AddField(
            model_name='interface',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='interfaces', to='documentation.project'),
        ),
    ]
