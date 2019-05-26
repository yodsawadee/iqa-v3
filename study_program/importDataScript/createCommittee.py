#import psycopg2
import xlrd
from study_program.models import Professor
from study_program.models import StudyProgram
from study_program.models import Committee


workbook = xlrd.open_workbook('C:/Users/58090032/Desktop/-/importDataScript/data/Revisedv2 Database_ [Assessors Matching & Assesment Scheduling_ An Application for IQA System].xlsx')
worksheet = workbook.sheet_by_name('CommitteeList (รายชื่อกรรมการปร')

#shell()
#exec(open('C:/iqa_website_test/IQA-Website-for-KMITL-master/myvenv/Scripts/iqa_web/study_program/importDataScript/createCommittee.py',encoding="utf8").read())


for i in range(2, worksheet.nrows):
    code = worksheet.row(i)[0].value
    year = worksheet.row(i)[2].value
    assessment_level = worksheet.row(i)[3].value
    profession = worksheet.row(i)[4].value

    prof_id = worksheet.row(i)[1].value
    try:
        a = Professor.objects.get(professor_id=prof_id)
        professor_id_id = a.id
    except:
        professor_id_id = 1

    c = Committee.objects.create(code = code, year = year, assessment_level = assessment_level, profession = profession, professor_id_id = professor_id_id)
    print("aee ok")


