# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

#import sorl.thumbnail.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('added', models.DateTimeField(auto_now=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Deck',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Face',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField(default=b'', blank=True)),
                ('image', models.TextField(default=b'', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserCard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('priority', models.PositiveSmallIntegerField(default=1)),
                ('due', models.DateTimeField(blank=True)),
                ('rung', models.SmallIntegerField(default=-1)),
                ('ease', models.PositiveSmallIntegerField(default=5)),
                ('card', models.ForeignKey(to='leitner.Card', on_delete=models.CASCADE)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserCardTest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('correct', models.BooleanField(default=True)),
                ('old_rung', models.SmallIntegerField(default=0)),
                ('new_rung', models.SmallIntegerField(default=0)),
                ('usercard', models.ForeignKey(to='leitner.UserCard', on_delete=models.CASCADE)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='card',
            name='back',
            field=models.ForeignKey(related_name='back', to='leitner.Face', on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='deck',
            field=models.ForeignKey(to='leitner.Deck', on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='front',
            field=models.ForeignKey(related_name='front', to='leitner.Face', on_delete=models.CASCADE),
            preserve_default=True,
        ),
    ]
