# Generated by Django 3.2.2 on 2021-05-10 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('workID', models.IntegerField(unique=True)),
                ('name', models.CharField(max_length=10)),
                ('gender', models.IntegerField(choices=[(1, 'Male'), (2, 'Female')], default=None, null=True)),
                ('phoneNumber', models.BigIntegerField(default=None, null=True)),
                ('email', models.EmailField(default=None, max_length=254, null=True)),
                ('pwd', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='CourseComments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('courseID', models.IntegerField()),
                ('studentID', models.IntegerField()),
                ('content', models.TextField(max_length=300)),
                ('rate', models.IntegerField(choices=[(1, 'Onestar'), (2, 'Twostar'), (3, 'Threestar'), (4, 'Fourstar'), (5, 'Fivestar')])),
                ('createTime', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='CourseGrouping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('courseID', models.IntegerField()),
                ('groupID', models.IntegerField()),
                ('groupName', models.CharField(max_length=30)),
                ('groupCounts', models.IntegerField()),
                ('groupLimits', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='CourseInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('courseName', models.CharField(max_length=30)),
                ('courseDescription', models.TextField(max_length=200, null=True)),
                ('courseTime', models.CharField(max_length=20, null=True)),
                ('courseLocation', models.CharField(max_length=40, null=True)),
                ('creditAward', models.IntegerField(null=True)),
                ('courseStatus', models.IntegerField(choices=[(0, 'Not Available'), (1, 'Deleted'), (2, 'Open'), (3, 'Closed'), (4, 'Settled')], default=0)),
                ('teacherName', models.CharField(max_length=10)),
                ('teacherDescription', models.TextField(max_length=200, null=True)),
                ('teacherID', models.IntegerField()),
                ('openFrom', models.DateTimeField(null=True)),
                ('openUntil', models.DateTimeField(null=True)),
                ('extra', models.TextField(max_length=500)),
                ('createTime', models.DateTimeField(auto_now_add=True)),
                ('modifyTime', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='CourseTaking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('studentID', models.IntegerField()),
                ('courseID', models.IntegerField()),
                ('settled', models.BooleanField(default=False)),
                ('creditAward', models.IntegerField(null=True)),
                ('validFrom', models.DateTimeField(null=True)),
                ('validUntil', models.DateTimeField(null=True)),
                ('grade', models.FloatField(null=True)),
                ('gradeType', models.IntegerField(choices=[(0, 'Cardinal'), (1, 'Hundredmark'), (2, 'Hundredmarkfloat')], null=True)),
                ('extra', models.TextField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Discussion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issueID', models.IntegerField()),
                ('fromWhich', models.IntegerField()),
                ('fromWhat', models.IntegerField()),
                ('fromWho', models.CharField(max_length=10)),
                ('toWhich', models.IntegerField(null=True)),
                ('toWhat', models.IntegerField(null=True)),
                ('toWho', models.CharField(max_length=10, null=True)),
                ('content', models.TextField(max_length=300)),
                ('createTime', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Issues',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('courseID', models.IntegerField()),
                ('studentID', models.IntegerField()),
                ('studentName', models.CharField(max_length=10)),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=300)),
                ('status', models.IntegerField(choices=[(1, 'Closed'), (2, 'Open')])),
                ('createTime', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='PlanDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('courseID', models.IntegerField()),
                ('planID', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Requirement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('planName', models.CharField(max_length=30)),
                ('requirement', models.IntegerField()),
                ('deadline', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('workID', models.IntegerField(unique=True)),
                ('name', models.CharField(max_length=10)),
                ('gender', models.IntegerField(choices=[(1, 'Male'), (2, 'Female')], default=None, null=True)),
                ('phoneNumber', models.BigIntegerField(default=None, null=True)),
                ('email', models.EmailField(default=None, max_length=254, null=True)),
                ('pwd', models.CharField(max_length=40)),
                ('planID', models.IntegerField(null=True)),
                ('requirementID', models.IntegerField(null=True)),
                ('validCredit', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('workID', models.IntegerField(unique=True)),
                ('name', models.CharField(max_length=10)),
                ('gender', models.IntegerField(choices=[(1, 'Male'), (2, 'Female')], default=None, null=True)),
                ('phoneNumber', models.BigIntegerField(default=None, null=True)),
                ('email', models.EmailField(default=None, max_length=254, null=True)),
                ('pwd', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='TrainingPlans',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('planName', models.CharField(max_length=30)),
                ('description', models.TextField(max_length=300, null=True)),
                ('createTime', models.DateTimeField(auto_now_add=True)),
                ('modifyTime', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
