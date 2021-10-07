# Generated by Django 3.2.8 on 2021-10-07 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("questions", "0002_question_tags"),
    ]

    operations = [
        migrations.AddField(
            model_name="answer",
            name="num_vote_down",
            field=models.PositiveIntegerField(db_index=True, default=0),
        ),
        migrations.AddField(
            model_name="answer",
            name="num_vote_up",
            field=models.PositiveIntegerField(db_index=True, default=0),
        ),
        migrations.AddField(
            model_name="answer",
            name="vote_score",
            field=models.IntegerField(db_index=True, default=0),
        ),
        migrations.AddField(
            model_name="comment",
            name="num_vote_down",
            field=models.PositiveIntegerField(db_index=True, default=0),
        ),
        migrations.AddField(
            model_name="comment",
            name="num_vote_up",
            field=models.PositiveIntegerField(db_index=True, default=0),
        ),
        migrations.AddField(
            model_name="comment",
            name="vote_score",
            field=models.IntegerField(db_index=True, default=0),
        ),
        migrations.AddField(
            model_name="question",
            name="num_vote_down",
            field=models.PositiveIntegerField(db_index=True, default=0),
        ),
        migrations.AddField(
            model_name="question",
            name="num_vote_up",
            field=models.PositiveIntegerField(db_index=True, default=0),
        ),
        migrations.AddField(
            model_name="question",
            name="vote_score",
            field=models.IntegerField(db_index=True, default=0),
        ),
    ]
