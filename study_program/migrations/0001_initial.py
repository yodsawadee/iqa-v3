# Generated by Django 2.0 on 2019-02-26 05:28

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AssessmentResult',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=200)),
                ('year', models.IntegerField(choices=[(1980, 1980), (1981, 1981), (1982, 1982), (1983, 1983), (1984, 1984), (1985, 1985), (1986, 1986), (1987, 1987), (1988, 1988), (1989, 1989), (1990, 1990), (1991, 1991), (1992, 1992), (1993, 1993), (1994, 1994), (1995, 1995), (1996, 1996), (1997, 1997), (1998, 1998), (1999, 1999), (2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019)], default=2019, verbose_name='year')),
                ('curriculum_status', models.TextField(choices=[('New', 'New'), ('Modify', 'Modify')], max_length=400)),
                ('curriculum_status_year', models.IntegerField(choices=[(1980, 1980), (1981, 1981), (1982, 1982), (1983, 1983), (1984, 1984), (1985, 1985), (1986, 1986), (1987, 1987), (1988, 1988), (1989, 1989), (1990, 1990), (1991, 1991), (1992, 1992), (1993, 1993), (1994, 1994), (1995, 1995), (1996, 1996), (1997, 1997), (1998, 1998), (1999, 1999), (2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019)], default=2019, verbose_name='หลักสูตรปี')),
                ('curriculum_standard', models.IntegerField(choices=[(1980, 1980), (1981, 1981), (1982, 1982), (1983, 1983), (1984, 1984), (1985, 1985), (1986, 1986), (1987, 1987), (1988, 1988), (1989, 1989), (1990, 1990), (1991, 1991), (1992, 1992), (1993, 1993), (1994, 1994), (1995, 1995), (1996, 1996), (1997, 1997), (1998, 1998), (1999, 1999), (2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019)], default=2019, verbose_name='มาตรฐานหลักสูตรตามปี')),
                ('pdf_docs', models.FileField(upload_to='assessment_details/')),
            ],
        ),
        migrations.CreateModel(
            name='AUN',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('criteria1', models.IntegerField()),
                ('criteria2', models.IntegerField()),
                ('criteria3', models.IntegerField()),
                ('criteria4', models.IntegerField()),
                ('criteria5', models.IntegerField()),
                ('criteria6', models.IntegerField()),
                ('criteria7', models.IntegerField()),
                ('criteria8', models.IntegerField()),
                ('criteria9', models.IntegerField()),
                ('criteria10', models.IntegerField()),
                ('criteria11', models.IntegerField()),
                ('total_score', models.IntegerField()),
                ('assessment_id', models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, to='study_program.AssessmentResult')),
            ],
        ),
        migrations.CreateModel(
            name='AvailableTime',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('appointment_date', models.DateField(default=datetime.datetime(2019, 2, 26, 12, 28, 5, 576661))),
                ('appointment_time', models.TimeField(default=datetime.datetime(2019, 2, 26, 12, 28, 5, 576661))),
                ('user', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Committee',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=200)),
                ('year', models.IntegerField(choices=[(1980, 1980), (1981, 1981), (1982, 1982), (1983, 1983), (1984, 1984), (1985, 1985), (1986, 1986), (1987, 1987), (1988, 1988), (1989, 1989), (1990, 1990), (1991, 1991), (1992, 1992), (1993, 1993), (1994, 1994), (1995, 1995), (1996, 1996), (1997, 1997), (1998, 1998), (1999, 1999), (2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019)], default=2019, verbose_name='year')),
                ('assessment_level', models.TextField(choices=[('Junior', 'Junior'), ('Senior', 'Senior'), ('Novice', 'Novice'), ('Apprentice-C', 'Apprentice-C')], max_length=400)),
                ('profession', models.CharField(max_length=200)),
                ('assessment_programs', models.ManyToManyField(blank=True, to='study_program.AssessmentResult')),
            ],
        ),
        migrations.CreateModel(
            name='Krai',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('professor_id', models.CharField(blank=True, max_length=200)),
                ('academic_title', models.CharField(max_length=200)),
                ('name_surname', models.CharField(max_length=200)),
                ('date_of_birth', models.DateField()),
                ('bsc', models.CharField(max_length=200)),
                ('bsc_grad_institute', models.CharField(max_length=200)),
                ('bsc_year', models.IntegerField(choices=[(1980, 1980), (1981, 1981), (1982, 1982), (1983, 1983), (1984, 1984), (1985, 1985), (1986, 1986), (1987, 1987), (1988, 1988), (1989, 1989), (1990, 1990), (1991, 1991), (1992, 1992), (1993, 1993), (1994, 1994), (1995, 1995), (1996, 1996), (1997, 1997), (1998, 1998), (1999, 1999), (2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019)], default=2019, verbose_name='year')),
                ('msc', models.CharField(max_length=200)),
                ('msc_grad_institute', models.CharField(max_length=200)),
                ('msc_year', models.IntegerField(choices=[(1980, 1980), (1981, 1981), (1982, 1982), (1983, 1983), (1984, 1984), (1985, 1985), (1986, 1986), (1987, 1987), (1988, 1988), (1989, 1989), (1990, 1990), (1991, 1991), (1992, 1992), (1993, 1993), (1994, 1994), (1995, 1995), (1996, 1996), (1997, 1997), (1998, 1998), (1999, 1999), (2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019)], default=2019, verbose_name='year')),
                ('phd', models.CharField(max_length=200)),
                ('phd_grad_institute', models.CharField(max_length=200)),
                ('phd_year', models.IntegerField(choices=[(1980, 1980), (1981, 1981), (1982, 1982), (1983, 1983), (1984, 1984), (1985, 1985), (1986, 1986), (1987, 1987), (1988, 1988), (1989, 1989), (1990, 1990), (1991, 1991), (1992, 1992), (1993, 1993), (1994, 1994), (1995, 1995), (1996, 1996), (1997, 1997), (1998, 1998), (1999, 1999), (2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019)], default=2019, verbose_name='year')),
                ('phone', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=200)),
                ('university', models.CharField(max_length=200)),
                ('additional_degree', models.CharField(blank=True, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='StudyProgram',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('code', models.CharField(blank=True, max_length=200)),
                ('name', models.CharField(max_length=200)),
                ('program_status', models.CharField(choices=[('ACTIVE', 'ACTIVE'), ('GOING TO CLOSE', 'GOING TO CLOSE'), ('NOT ACTIVE', 'NOT ACTIVE')], max_length=200)),
                ('degree_and_major', models.CharField(max_length=400)),
                ('collaboration_with_other_institues', models.CharField(choices=[('Program issued specifically by KMITL', 'Program issued specifically by KMITL'), ('Program supported by other institutes', 'Program supported by other institutes'), ('Collaborated program with other institutes', 'Collaborated program with other institutes')], max_length=400)),
                ('pdf_docs', models.FileField(upload_to='study_program_details/')),
                ('responsible_professors', models.ManyToManyField(blank=True, to='study_program.Professor')),
            ],
        ),
        migrations.AddField(
            model_name='professor',
            name='responsible_program',
            field=models.ManyToManyField(blank=True, to='study_program.StudyProgram'),
        ),
        migrations.AddField(
            model_name='committee',
            name='professor_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='study_program.Professor'),
        ),
        migrations.AddField(
            model_name='availabletime',
            name='appointed_committee',
            field=models.ManyToManyField(blank=True, to='study_program.Committee'),
        ),
        migrations.AddField(
            model_name='availabletime',
            name='appointed_program',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, to='study_program.StudyProgram'),
        ),
        migrations.AddField(
            model_name='assessmentresult',
            name='committee_id',
            field=models.ManyToManyField(blank=True, to='study_program.Committee'),
        ),
        migrations.AddField(
            model_name='assessmentresult',
            name='program_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='study_program.StudyProgram'),
        ),
    ]
