# Generated by Django 5.0.6 on 2024-06-26 06:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TotalCost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('u21', models.CharField(blank=True, max_length=100, null=True)),
                ('ru21', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('u22', models.CharField(blank=True, max_length=100, null=True)),
                ('ru22', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('u23', models.CharField(blank=True, max_length=100, null=True)),
                ('ru23', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('u24', models.CharField(blank=True, max_length=100, null=True)),
                ('ru24', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('u25', models.CharField(blank=True, max_length=100, null=True)),
                ('ru25', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('u26', models.CharField(blank=True, max_length=100, null=True)),
                ('ru26', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('u31', models.CharField(blank=True, max_length=100, null=True)),
                ('ru31', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('u32', models.CharField(blank=True, max_length=100, null=True)),
                ('ru32', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('u33', models.CharField(blank=True, max_length=100, null=True)),
                ('ru33', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('u34', models.CharField(blank=True, max_length=100, null=True)),
                ('ru34', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('u35', models.CharField(blank=True, max_length=100, null=True)),
                ('ru35', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('u37', models.CharField(blank=True, max_length=100, null=True)),
                ('ru37', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('u41', models.CharField(blank=True, max_length=100, null=True)),
                ('ru41', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('u43', models.CharField(blank=True, max_length=100, null=True)),
                ('ru43', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('u44', models.CharField(blank=True, max_length=100, null=True)),
                ('ru44', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('u51', models.CharField(blank=True, max_length=100, null=True)),
                ('ru51', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('u52', models.CharField(blank=True, max_length=100, null=True)),
                ('ru52', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('u57', models.CharField(blank=True, max_length=100, null=True)),
                ('ru57', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('u58', models.CharField(blank=True, max_length=100, null=True)),
                ('ru58', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('u61', models.CharField(blank=True, max_length=100, null=True)),
                ('ru61', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('u63', models.CharField(blank=True, max_length=100, null=True)),
                ('ru63', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('u64', models.CharField(blank=True, max_length=100, null=True)),
                ('ru64', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('u65', models.CharField(blank=True, max_length=100, null=True)),
                ('ru65', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('u71', models.CharField(blank=True, max_length=100, null=True)),
                ('ru71', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('u72', models.CharField(blank=True, max_length=100, null=True)),
                ('ru72', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('u73', models.CharField(blank=True, max_length=100, null=True)),
                ('ru73', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('u74', models.CharField(blank=True, max_length=100, null=True)),
                ('ru74', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('u81', models.CharField(blank=True, max_length=100, null=True)),
                ('ru81', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('u82', models.CharField(blank=True, max_length=100, null=True)),
                ('ru82', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('u83', models.CharField(blank=True, max_length=100, null=True)),
                ('ru83', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('u84', models.CharField(blank=True, max_length=100, null=True)),
                ('ru84', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('u91', models.CharField(blank=True, max_length=100, null=True)),
                ('ru91', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('u92', models.CharField(blank=True, max_length=100, null=True)),
                ('ru92', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('u93', models.CharField(blank=True, max_length=100, null=True)),
                ('ru93', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('u94', models.CharField(blank=True, max_length=100, null=True)),
                ('ru94', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('u95', models.CharField(blank=True, max_length=100, null=True)),
                ('ru95', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('u96', models.CharField(blank=True, max_length=100, null=True)),
                ('ru96', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('u97', models.CharField(blank=True, max_length=100, null=True)),
                ('ru97', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('ru1a', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('ru1c', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('ru1d', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('ru1e', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('ru2a', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('ru2b', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('ru2d', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('ru2e', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('ru2f', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('ru3b', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('ru3c', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('ru3d', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('ru4a', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('ru4b', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=255)),
                ('login_time', models.DateTimeField(blank=True, null=True)),
                ('logout_time', models.DateTimeField(blank=True, null=True)),
                ('button_clicked', models.CharField(blank=True, max_length=255, null=True)),
                ('file_downloaded', models.FileField(blank=True, null=True, upload_to='downloads/')),
                ('file_details', models.TextField(blank=True, null=True)),
                ('timestamp', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
