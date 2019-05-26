from study_program.models import AssessmentResult, Professor, StudyProgram, Committee
import xlrd

workbook = xlrd.open_workbook('C:/Users/58090032/Desktop/-/importDataScript/data/Revisedv2 Database_ [Assessors Matching & Assesment Scheduling_ An Application for IQA System].xlsx')
worksheet = workbook.sheet_by_name('Committee-AssessmentResult (เชื')

#shell()
#exec(open('C:/iqa_website_test/IQA-Website-for-KMITL-master/myvenv/Scripts/iqa_web/study_program/importDataScript/createCommitteeAssessment.py',encoding="utf8").read())

for i in range(2, worksheet.nrows):
    committee_code = worksheet.row(i)[0].value
    assessment_code = worksheet.row(i)[1].value

    
    a = Committee.objects.get(code=committee_code)
    b = AssessmentResult.objects.get(code = assessment_code)
    a.assessment_programs.add(b)

    print("aee ok")