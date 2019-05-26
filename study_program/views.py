from django import forms
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from django.http import HttpResponseRedirect, HttpResponse
import csv
from .models import StudyProgram, Professor, AssessmentResult, Committee, AUN, AvailableTime, Issue, Comment
from .forms import StudyProgramForm, ProfessorForm, AssessmentResultForm, CommitteeForm, AunForm, AvailableTimeForm, IssueForm, CommentForm

import numpy as np
import pandas as pd

import datetime, calendar
import math

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#import message on success or failure
from django.contrib import messages
# -------------------------------- main_menu -------------------------------- #


@login_required(login_url="/login")
def main_menu(request):
    return render(request, 'main_page/main_menu_page.html')

@login_required(login_url="/login")
def assessment_menu(request):
    return render(request, 'main_page/assessment_menu_page.html')

@login_required(login_url="/login")
def iqa_menu(request):
    return render(request, 'main_page/iqa_menu_page.html')

@login_required(login_url="/login")
def faculty_menu(request):
    return render(request, 'main_page/faculty_menu_page.html')

#@user_passes_test(lambda u: u.is_superuser, login_url='all_committee')
@login_required(login_url="login")
def committee_menu(request):
    return render(request, "main_page/committee_menu_page.html")


# --------------------------------------------------------------------------- #




# -------------------------------- iqa_menu -------------------------------- #

@login_required(login_url="/login")
def all_notification(request):
    sp = StudyProgram.objects.all().order_by('id').reverse()

    notify_not_enough_rp = []
    number_of_responsible_professor = 3

    for study_program in sp:
        #print(study_program.responsible_professors.count())
        if(study_program.responsible_professors.count() < number_of_responsible_professor):
            notify_not_enough_rp.append(study_program)
    
    ########################################################################
    page = request.GET.get('page')
    paginator = Paginator(notify_not_enough_rp, 10)

    try:
        notify_not_enough_rp = paginator.page(page)
    except PageNotAnInteger:
        notify_not_enough_rp = paginator.page(1)
    except EmptyPage:
        notify_not_enough_rp = paginator.page(paginator.num_pages)
    ########################################################################
    
    
    context = {'notify_not_enough_rp':notify_not_enough_rp}
    return render(request, 'iqa_menu/notice/notice.html', context)

def pearson_based_collaborative(df):

    #Pearson similarity
    pearson_sim = df.corr(method='pearson')
    #print(pearson_sim)
    
    #Predict unrated rating part
    for i in range(1,len(df.columns)):
        temp_sim_list = []
        
        for k in range(len(pearson_sim.index)):
            if pearson_sim.iloc[k,i-1] >= 0.3 and (i-1 != k):
                temp_sim_list.append(pearson_sim.columns[k])
        
        for j in range(len(df.index)):
            numerator = 0
            denominator = 0
            if df.isnull().iloc[j,i]:
                for m in range(len(temp_sim_list)):
                    numerator = numerator + (df.iloc[j,df.columns.get_loc(temp_sim_list[m])] * pearson_sim.iloc[pearson_sim.index.get_loc(temp_sim_list[m]),i-1])
                    denominator = denominator + pearson_sim.iloc[pearson_sim.index.get_loc(temp_sim_list[m]),i-1]
                if denominator == 0:
                    continue
                else:
                    df.iloc[j,i] = numerator/denominator
                
        #Reccommend
    return df
                
                
            
            
def viewAllRecommendedCommittee(df): 
    recommendation_committee_list = []
    recommendation_committee_list_score = []
    recommendation_committee_list_percentage = []
    
    professors_name = []
    for col in df.columns:
        professors_name.append(col)

    #print(professors_name)
    for i in range(len(df.index)):
        max1 = -999
        max2 = -999
        name1 = ""
        name2 = ""
        for j in range(1, len(df.columns)):
            if(df.iloc[i,j] > max1):
                max2 = max1
                name2 = name1
                max1 = df.iloc[i,j]
                name1 = professors_name[j]
            elif(df.iloc[i,j] > max2):
                max2 = df.iloc[i,j]
                name2 = professors_name[j]
        
        recommendation_committee_list.append([df.iloc[i,0],name1, name2])
        recommendation_committee_list_score.append([df.iloc[i,0], max1, max2]) 
        recommendation_committee_list_percentage.append([df.iloc[i,0],name1 + str(round((max1 * 100),2)) +  "%" , name2 + str(round((max2 * 100),2)) + "%"])
        
    #print(recommendation_committee_list)
    #print(recommendation_committee_list_score)
    #print("########################### PERCENTAGE!!!!################################3")
    #print(recommendation_committee_list_percentage)
    return recommendation_committee_list_percentage

def viewAllNewRecomendedCommittee(variable1):
    result = [['หลักสูตรวิศวกรรมศาสตรบัณฑิต สาขาวิชาวิศวกรรมการบินและนักบินพาณิชย์', 'VASUDO58.4%', 'BOONSU30.0%'], ['หลักสูตรวิทยาศาสตรมหาบัณฑิต สาขาวิชาเกษตรศาสตร์', 'BOONSU45.0%', 'WORNCH45.0%'], ['หลักสูตรวิทยาศาสตรมหาบัณฑิต สาขาวิชาเทคโนโลยีชีวภาพทางการเกษตร', 'PINMKW60.0%', 'BOONSU50.0%'], ['หลักสูตรวิทยาศาสตรมหาบัณฑิต สาขาวิชาวิทยาศาสตร์การประมง', 'JIRASI43.4%', 'KASESI23.4%'], ['หลักสูตรวิทยาศาสตรมหาบัณฑิต สาขาวิชาพัฒนาการเกษตรและการจัดการทรัพยากร', 'URASBU48.4%', 'VEERPE23.4%'], ['หลักสูตรวิทยาศาสตรมหาบัณฑิต สาขาวิชาพืชสวน', 'PINMKW60.0%', 'BOONSU50.0%'], ['หลักสูตรวิทยาศาสตรมหาบัณฑิต สาขาวิชาสัตวศาสตร์', 'PINMKW60.0%', 'PAKOWA33.4%'], ['หลักสูตรปรัชญาดุษฎีบัณฑิต สาขาวิชาเกษตรศาสตร์', 'BOONSU45.0%', 'WORNCH45.0%'], ['หลักสูตรวิศวกรรมศาสตรบัณฑิต สาขาวิชาวิศวกรรมระบบการผลิต', 'CHAINU43.4%', 'TEERTI6.7%'], ['หลักสูตรวิศวกรรมศาสตรมหาบัณฑิต สาขาวิชาวิศวกรรมระบบการผลิตขั้นสูง', 'CHAINU43.4%', 'TEERTI6.7%'], ['หลักสูตรปรัชญาดุษฎีบัณฑิต สาขาวิชาวิศวกรรมระบบการผลิตขั้นสูง(หลักสูตรนานาชาติ)', 'CHAINU48.4%', 'TEERTI11.7%'], ['หลักสูตรปรัชญาดุษฎีบัณฑิต สาขาวิชาวิทยาศาสตร์การอาหาร', 'PINMKW55.0%', 'PARITU23.4%'], ['หลักสูตรวิทยาศาสตรบัณฑิต สาขาวิชาวิทยาศาสตร์และเทคโนโลยีการอาหาร', 'THIPLI33.4%', 'CHAINU23.4%'], ['หลักสูตรวิทยาศาสตรบัณฑิต สาขาวิชาเทคโนโลยีการหมักในอุตสาหกรรมอาหาร', 'BOONSU50.0%', 'WORNCH50.0%'], ['หลักสูตรวิทยาศาสตรบัณฑิต สาขาวิชาวิศวกรรมแปรรูปอาหาร', 'TERMPE33.4%', 'WANDPE31.7%'], ['หลักสูตรวิทยาศาสตรมหาบัณฑิต สาขาวิชาการจัดการความปลอดภัยอาหาร', 'BOONSU50.0%', 'WORNCH50.0%'], ['หลักสูตรวิทยาศาสตรมหาบัณฑิต สาขาวิชาเทคโนโลยีการบริการอาหารและการจัดการ', 'THIPLI33.4%', 'CHAINU23.4%'], ['หลักสูตรวิทยาศาสตรมหาบัณฑิต สาขาวิชาวิทยาศาสตร์อาหาร', 'PINMKW55.0%', 'PARITU23.4%'], ['หลักสูตรครุศาสตร์อุตสาหกรรมดุษฎีบัณฑิต สาขาวิชาการบริหารการศึกษา', 'WANDPE26.7%', 'TERMPE26.7%'], ['หลักสูตรครุศาสตร์อุตสาหกรรมดุษฎีบัณฑิต สาขาวิชาครุศาสตร์อุตสาหกรรม', 'PONRNE33.4%', 'PRAPUP33.4%'], ['หลักสูตรครุศาสตร์อุตสาหกรรมบัณฑิต สาขาวิชาการออกแบบสภาพแวดลอมภายใน', 'OACHPA33.4%', 'PRAPUP23.4%'], ['หลักสูตรครุศาสตร์อุตสาหกรรมบัณฑิต สาขาวิชาครุศาสตร์การออกแบบ', 'JANTPH311.7%', 'PORAAS23.4%'], ['หลักสูตรครุศาสตร์อุตสาหกรรมบัณฑิต สาขาวิชาครุศาสตร์เกษตร', 'DUANPR26.7%', 'KASESI23.4%'], ['หลักสูตรครุศาสตร์อุตสาหกรรมบัณฑิต สาขาวิชาครุศาสตร์วิศวกรรม', 'BOONSU40.0%', 'WORNCH40.0%'], ['หลักสูตรครุศาสตร์อุตสาหกรรมบัณฑิต สาขาวิชาสถาปัตยกรรม', 'OACHPA33.4%', 'PRAPUP33.4%'], ['หลักสูตรครุศาสตร์อุตสาหกรรมมหาบัณฑิต สาขาวิชาการบริหารการศึกษา', 'WANDPE26.7%', 'TERMPE26.7%'], ['หลักสูตรครุศาสตร์อุตสาหกรรมมหาบัณฑิต สาขาวิชาครุศาสตร์อุตสาหกรรม', 'PONRNE33.4%', 'PRAPUP33.4%'], ['หลักสูตรครุศาสตร์อุตสาหกรรมมหาบัณฑิต สาขาวิชาเทคโนโลยีการออกแบบผลิตภัณฑ์อุตสาหกรรม', 'JANTPH311.7%', 'PORAAS23.4%'], ['หลักสูตรครุศาสตร์อุตสาหกรรมมหาบัณฑิต สาขาวิชาวิศวกรรมไฟฟ้าสื่อสาร', 'BOONSU40.0%', 'WORNCH40.0%'], ['หลักสูตรครุศาสตร์อุตสาหกรรมมหาบัณฑิต สาขาวิชาอิเล็กทรอนิกส์', 'BOONSU40.0%', 'WORNCH40.0%'], ['หลักสูตรเทคโนโลยีบัณฑิต สาขาวิชาเทคโนโลยีชีวภาพทางการเกษตร(ต่อเนื่อง)', 'PAKOWA33.4%', 'WIBOPO33.4%'], ['หลักสูตรเทคโนโลยีบัณฑิต สาขาเทคโนโลยีอิเล็กทรอนิกส์(ต่อเนื่อง)', 'VEERPE48.4%', 'WIBOPO38.4%'], ['หลักสูตรปรัชญาดุษฎีบัณฑิต สาขาวิชาการศึกษาเกษตร', 'THIPLI38.4%', 'WANDPE33.4%'], ['หลักสูตรปรัชญาดุษฎีบัณฑิต สาขาวิชาการศึกษาวิทยาศาตร์เกษตร', 'THIPLI38.4%', 'WANDPE33.4%'], ['หลักสูตรปรัชญาดุษฎีบัณฑิต สาขาวิชาคอมพิวเตอร์ศึกษา', 'BOONSU55.0%', 'WORNCH55.0%'], ['หลักสูตรปรัชญาดุษฎีบัณฑิต สาขาวิชาวิศวกรรมไฟฟ้าศึกษา', 'VEERPE58.4%', 'SORAGL43.4%'], ['หลักสูตรวิทยาศาสตรมหาบัณฑิต สาขาวิชาการศึกษาเกษตร', 'DUANPR26.7%', 'KASESI23.4%'], ['หลักสูตรวิทยาศาสตรมหาบัณฑิต สาขาวิชาการศึกษาวิทยาศาสตร์', 'BOONSU45.0%', 'WORNCH45.0%'], ['หลักสูตรวิทยาศาสตรมหาบัณฑิต สาขาวิชาคอมพิวเตอร์ศึกษา', 'BOONSU55.0%', 'WORNCH55.0%'], ['หลักสูตรศิลปศาสตรบัณฑิต สาขาวิชาภาษาญี่ปุ่น', 'PONRNE33.4%', 'PARITU28.4%'], ['หลักสูตรศิลปศาสตรบัณฑิต สาขาวิชาภาษาอังกฤษ', 'PARITU33.4%', 'TIYAKA23.4%'], ['หลักสูตรศิลปศาสตรมหาบัณฑิต สาขาวิชาภาษาศาสตร์ประยุกต์-ภาษาอังกฤษเพื่อวัตถุประสงค์ทางวิชาชีพ', 'PONRNE33.4%', 'JIRASI33.4%'], ['หลักสูตรสถาปัตยกรรมศาสตรบัณฑิต สาขาวิชาสถาปัตยกรรมหลัก', 'PAKOWA40.0%', 'WANDPE26.7%'], ['หลักสูตรสถาปัตยกรรมศาสตรบัณฑิต สาขาวิชาสถาปัตยกรรมภายใน', 'PRAPUP38.4%', 'SARIVI33.4%'], ['หลักสูตรภูมิสถาปัตยกรรมศาสตรบัณฑิต', 'PAKOWA40.0%', 'WANDPE26.7%'], ['หลักสูตรสถาปัตยกรรมศาสตรบัณฑิต สาขาวิชาศิลปอุตสาหกรรม', 'URASBU33.4%', 'KANKKH23.4%'], ['หลักสูตรศิลปกรรมศาสตรบัณฑิต สาขาวิชาภาพยนตร์และดิจิทัล มีเดีย', 'SARIVI33.4%', 'PRAPUP23.4%'], ['หลักสูตรศิลปกรรมศาสตรบัณฑิต สาขาวิชานิเทศศิลป์', 'SARIVI33.4%', 'PRAPUP23.4%'], ['หลักสูตรศิลปกรรมศาสตรบัณฑิต สาขาวิชาการถ่ายภาพ', 'SARIVI33.4%', 'PRAPUP23.4%'], ['หลักสูตรศิลปกรรมศาสตรบัณฑิต สาขาวิชาการออกแบบสนเทศสามมิติ', 'SARIVI33.4%', 'PRAPUP23.4%'], ['หลักสูตรศิลปกรรมศาสตรบัณฑิต สาขาวิชาจิตรกรรม', 'OACHPA53.4%', 'VASUD33.4%'], ['หลักสูตรศิลปกรรมศาสตรบัณฑิต สาขาวิชาประติมากรรม', 'OACHPA53.4%', 'VASUD33.4%'], ['หลักสูตรศิลปกรรมศาสตรบัณฑิต สาขาวิชาภาพพิมพ์', 'OACHPA53.4%', 'VASUD33.4%'], ['หลักสูตรสถาปัตยกรรมศาสตรมหาบัณฑิต สาขาวิชาสถาปัตยกรรมเขตร้อน', 'PAKOWA40.0%', 'WANDPE26.7%'], ['หลักสูตรสถาปัตยกรรมศาสตรมหาบัณฑิต สาขาวิชาเทคโนโลยีสถาปัตยกรรม', 'PAKOWA40.0%', 'WANDPE26.7%'], ['หลักสูตรสถาปัตยกรรมศาสตรมหาบัณฑิต สาขาวิชาสถาปัตยภายใน', 'PRAPUP38.4%', 'SARIVI33.4%'], ['หลักสูตรสถาปัตยกรรมศาสตรมหาบัณฑิต สาขาวิชาการออกแบบอุตสาหกรรม', 'URASBU33.4%', 'KANKKH23.4%'], ['หลักสูตรศิลปกรรมศาสตรมหาบัณฑิต สาขาวิชาทัศนศิลป์', 'OACHPA53.4%', 'VASUD33.4%'], ['หลักสูตรการวางแผนภาคและเมืองมหาบัณฑิต สาขาวิชาการวางแผนชุมชนเมืองและสภาพแวดล้อม', 'PAKOWA40.0%', 'WANDPE26.7%'], ['หลักสูตรสถาปัตยกรรมศาสตรดุษฎีบัณฑิต สาขาวิชาสหวิทยาการการวิจัยเพื่อการออกแบบ', 'PAKOWA40.0%', 'WANDPE26.7%'], ['หลักสูตรวิทยาศาสตรมหาบัณฑิต สาขาวิชาเทคโนโลยีสารสนเทศ', 'JAKASU26.7%', 'CHAIPR26.7%'], ['หลักสูตรวิทยาศาสตรบัณฑิต สาขาวิชาวิทยาการข้อมูลและการวิเคราะห์เชิงธุรกิจ', 'AUCHRE26.7%', 'AUCHSR26.7%'], ['หลักสูตรปรัชญาดุษฎีบัณฑิต สาขาวิชาเทคโนโลยสารสนเทศ', 'PINMKW45.0%', 'SAKCTA26.7%'], ['หลักสูตรวิทยาศาสตรบัณฑิต สาขาวิชาเทคโนโลยีสารสนเทศทางธุรกิจ(หลักสูตรนานาชาติ)', 'THITCH36.7%', 'AUCHRE26.7%'], ['หลักสูตรวิทยาศาสตรบัณฑิต สาขาวิชาเทคโนโลยีสารสนเทศ', 'VARARU16.7%', '-99900%'], ['หลักสูตรบริหารธุรกิจบัณฑิต(หลักสูตรนานาชาติ)', 'JIRASI33.4%', 'BOONSU30.0%'], ['หลักสูตรบริหารธุรกิจบัณฑิต', 'BOONSU30.0%', 'WORNCH30.0%'], ['หลักสูตรบริหารธุรกิจมหาบัณฑิต', 'PINMKW40.0%', 'WANDPE26.7%'], ['หลักสูตรบริหารธุรกิจมหาบัณฑิต สาขาวิชาบริหารธุรกิจอุตสาหกรรม', 'PARITU28.4%', 'WANDPE26.7%'], ['หลักสูตรปรัชญาดุษฎีบัณฑิต สาขาวิชาบริหารธุรกิจอุตสาหกรรม', 'PARITU28.4%', 'WANDPE26.7%'], ['หลักสูตรวิทยาศาสตรบัณฑิต สาขาเศรษฐศาสตร์ธุรกิจและการจัดการ', 'BOONSU40.0%', 'WORNCH40.0%'], ['หลักสูตรวิศวกรรมศาสตรบัณฑิต สาขาวิชาวิศวกรรมซอฟต์แวร์(หลักสูตรนานาชาติ)', 'PAKOWA70.0%', 'WIBOPO53.4%'], ['หลักสูตรวิทยาศาสตรบัณฑิต สาขาวิชาการจัดการวิศวกรรมและเทคโนโลยี(หลักสูตรนานาชาติ)', 'PAKOWA50.0%', 'WIBOPO38.4%'], ['หลักสูตรวิศวกรรมศาสตรมหาบัณฑิต สาขาวิชาวิศวกรรมยานยนต์(หลักสูตรนานาชาติ)', 'PAKOWA60.0%', 'WIBOPO53.4%'], ['หลักสูตรวิศวกรรมศาสตรมหาบัณฑิต สาขาคำนวนในระบบวิศวกรรม(หลักสูตรนานาชาติ)', 'PAKOWA60.0%', 'WIBOPO48.4%'], ['หลักสูตรวิทยาศาสตรมหาบัณฑิต สาขาวิชาการจัดการโลจิสติกส์และซัพพลายเชน(หลักสูตรนานาชาติ)', 'PAKOWA40.0%', 'WIBOPO38.4%'], ['หลักสูตรปรัชญาดุษฎีบัณฑิต สาขาวิชาการจัดการโลจิสติกส์และซัพพลายเชน(หลักสูตรนานาชาติ)', 'PAKOWA40.0%', 'WIBOPO38.4%'], ['หลักสูตรวิศวกรรมศาสตรบัณฑิต สาขาวิชาวิศวกรรมโทรคมนาคม', 'SARIVI43.4%', 'PRAPUP43.4%'], ['หลักสูตรวิศวกรรมศาสตรบัณฑิต สาขาวิชาวิศวกรรมไฟฟ้า', 'PONRNE33.4%', 'RATRSI16.7%'], ['หลักสูตรวิศวกรรมศาสตรมหาบัณฑิต สาขาวิชาวิศวกรรมไฟฟ้า', 'PONRNE33.4%', 'RATRSI16.7%'], ['หลักสูตรวิศวกรรมศาสตรบัณฑิต สาขาวิชาวิศวกรรมพลังงานไฟฟ้า', 'PONRNE33.4%', 'RATRSI16.7%'], ['หลักสูตรวิศวกรรมศาสตรบัณฑิต สาขาวิชาวิศวกรรมอิเล็กทรอนิกส์', 'SORAGL58.4%', 'BOONSU30.0%'], ['หลักสูตรวิศวกรรมศาสตรมหาบัณฑิต สาขาวิชาวิศวกรรมอิเล็กทรอนิกส์', 'SORAGL58.4%', 'BOONSU30.0%'], ['หลักสูตรวิศวกรรมศาสตรมหาบัณฑิต สาขาวิชาวิศวกรรมไมโครอิเล็กทรอนิกส์', 'SORAGL58.4%', 'BOONSU30.0%'], ['หลักสูตรวิศวกรรมศาสตรบัณฑิต สาขาวิชาวิศวกรรมชีวการแพทย์', 'KASESI43.4%', 'PINMKW40.0%'], ['หลักสูตรวิศวกรรมศาสตรมหาบัณฑิต สาขาวิชาวิศวกรรมชีวการแพทย์', 'KASESI43.4%', 'PINMKW40.0%'], ['หลักสูตรวิศวกรรมศาสตรดุษฎีบัณฑิต สาขาวิชาวิศวกรรมชีวการแพทย์', 'KASESI43.4%', 'PONRNE33.4%'], ['หลักสูตรวิศวกรรมศาสตรบัณฑิต สาขาวิชาวิศวกรรมคอมพิวเตอร์', 'WANDPE46.7%', 'TERMPE46.7%'], ['หลักสูตรวิศวกรรมศาสตรมหาบัณฑิต สาขาวิชาวิศวกรรมคอมพิวเตอร์', 'WANDPE56.7%', 'TERMPE56.7%'], ['หลักสูตรวิศวกรรมศาสตรบัณฑิต สาขาวิชาวิศวกรรมดนตรีและสื่อผสม', 'PORAAS23.4%', 'PATCMU16.7%'], ['หลักสูตรวิศวกรรมศาสตรบัณฑิต สาขาวิชาวิศวกรรมสารสนเทศ', 'WANDPE56.7%', 'TERMPE56.7%'], ['หลักสูตรวิศวกรรมศาสตรมหาบัณฑิต สาขาวิชาวิศวกรรมสารสนเทศ', 'WANDPE56.7%', 'TERMPE56.7%'], ['หลักสูตรวิศวกรรมศาสตรบัณฑิต สาขาวิชาวิศวกรรมคอมพิวเตอร์(ต่อเนื่อง)', 'WANDPE56.7%', 'TERMPE53.4%'], ['หลักสูตรวิศวกรรมศาสตรบัณฑิต สาขาวิชาวิศวกรรมระบบควบคุม', 'VEERPE63.4%', 'THIPLI23.4%'], ['หลักสูตรวิศวกรรมศาสตรมหาบัณฑิต สาขาวิชาวิศวกรรมระบบควบคุม', 'VEERPE63.4%', 'THIPLI23.4%'], ['หลักสูตรวิศวกรรมศาสตรบัณฑิต สาขาวิชาวิศวกรรมแมคคาทรอนิกส์', 'PARITU23.4%', 'SORAKU11.7%'], ['หลักสูตรวิศวกรรมศาสตรบัณฑิต สาขาวิชาวิศวกรรมการวัดคุม', 'PORAAS23.4%', 'DUANPR16.7%'], ['หลักสูตรวิศวกรรมศาสตรมหาบัณฑิต สาขาวิชาวิศวกรรมการวัดคุม', 'PORAAS23.4%', 'DUANPR16.7%'], ['หลักสูตรวิศวกรรมศาสตรบณฑิต สาขาวิชาวิศวกรรมอัตโนมัติ', 'VEERPE63.4%', 'URASBU33.4%'], ['หลักสูตรวิศวกรรมศาสตรมหาบัณฑิต สาขาวิชาวิศวกรรมอัตโนมัติ', 'VEERPE63.4%', 'URASBU33.4%'], ['หลักสูตรวิศวกรรมศาสตรบัณฑิต สาขาวิชาวิศวกรรมเครื่องกล', 'SARIVI43.4%', 'PRAPUP33.4%'], ['หลักสูตรวิศวกรรมศาสตรบัณฑิต สาขาวิชาวิศวกรรมขนส่งทางราง', 'SARIVI43.4%', 'PRAPUP33.4%'], ['หลักสูตรวิศวกรรมศาสตรมหาบัณฑิต สาขาวิศวกรรมเครื่องกล', 'WANDPE48.4%', 'TERMPE48.4%'], ['หลักสูตรวิศวกรรมศาสตรดุษฏีบัณฑิต สาขาวิชาวิศวกรรมเครื่องกล', 'WANDPE48.4%', 'TERMPE48.4%'], ['หลักสูตรวิศวกรรมศาสตรบัณฑิต สาขาวิชาวิศวกรรมโยธา', 'PRAPUP43.4%', 'SARIVI43.4%'], ['หลักสูตรวิศวกรรมศาสตรมหาบัณฑิต สาขาวิชาวิศวกรรมโยธา', 'PRAPUP43.4%', 'SARIVI43.4%'], ['หลักสูตรวิศวกรรมศาสตรดุษฎีบัณฑิต สาขาวิชาวิศวกรรมโยธา', 'PRAPUP43.4%', 'SARIVI43.4%'], ['หลักสูตรวิศวกรรมศาสตรมหาบัณฑิต สาขาวิชาวิศวกรรมสิ่งแวดล้อมและพลังงานเพื่อความยั่งยืน', 'PAKOWA60.0%', 'OACHPA23.4%'], ['หลักสูตรวิศวกรรมศาสตรมหาบัณฑิต สาขาวิชาวิศวกรรมก่อสร้างการจัดการและสิ่งแวดล้อม', 'PAKOWA60.0%', '-99900%'], ['หลักสูตรวิศวกรรมศาสตรบัณฑิต สาขาวิชาวิศวกรรมโยธา(ต่อเนื่อง)', 'PAKOWA60.0%', 'BOONSU40.0%'], ['หลักสูตรวิศวกรรมศาสตรบัณฑิต สาขาวิชาวิศวกรรมโยธา(หลักสูตรนานาชาติ)', 'PAKOWA60.0%', 'BOONSU40.0%'], ['หลักสูตรวิศวกรรมศาสตรบัณฑิต สาขาวิชาวิศวกรรมเกษตร', 'AUMPJU58.4%', 'TIYAKA23.4%'], ['หลักสูตรวิศวกรรมศาสตรมหาบัณฑิต สาขาวิชาวิศวกรรมเกษตร', 'AUMPJU58.4%', 'TIYAKA23.4%'], ['หลักสูตรวิศวกรรมศาสตรดุษฎีบัณฑิต สาขาวิชาวิศวกรรมเกษตร', 'AUMPJU58.4%', 'TIYAKA23.4%'], ['หลักสูตรวิศวกรรมศาสตรบัณฑิต สาขาวิชาวิศวกรรมระบบอุตสาหกรรมการเกษตร(ต่อเนื่อง)', 'AUMPJU58.4%', 'TIYAKA23.4%'], ['หลักสูตรวิศวกรรมศาสตรบัณฑิต สาขาวิชาวิศวกรรมเคมี', 'WIBOPO53.4%', 'PAKOWA53.4%'], ['หลักสูตรวิศวกรรมศาสตรบัณฑิต สาขาวิชาวิศวกรรมปิโตรเคมี', 'WIBOPO53.4%', 'PAKOWA53.4%'], ['หลักสูตรวิศวกรรมศาสตรมหาบัณฑิต สาขาวิชาวิศวกรรมเคมี', 'WANDPE48.4%', 'TERMPE48.4%'], ['หลักสูตรวิศวกรรมศาสตรดุษฎีบัณฑิต สาขาวิชาวิศวกรรมเคมี', 'WANDPE48.4%', 'TERMPE48.4%'], ['หลักสูตรวิศวกรรมศาสตรบัณฑิต สาขาวิชาวิศวกรรมเคมี(หลักสูตรนานาชาติ)', 'WIBOPO53.4%', 'SORAGL53.4%'], ['หลักสูตรวิศวกรรมศาสตรบัณฑิต สาขาวิชาวิศวกรรมอาหาร', 'JIRASI43.4%', 'URASBU33.4%'], ['หลักสูตรวิศวกรรมศาสตรมหาบัณฑิต สาขาวิชาวิศวกรรมอาหาร', 'JIRASI43.4%', 'URASBU33.4%'], ['หลักสูตรวิศวกรรมศาสตรดุษฎีบัณฑิต สาขาวิชาวิศวกรรมอาหาร', 'JIRASI43.4%', 'URASBU33.4%'], ['หลักสูตรวิศวกรรมศาสตรบัณฑิต สาขาวิชาวิศวกรรมอุตสาหการ', 'AUMPJU58.4%', 'TIYAKA23.4%'], ['หลักสูตรวิศวกรรมศาสตรบัณฑิต สาขาวิชาวิศวกรรมออกแบบการผลิตและวัสดุ', 'AUMPJU58.4%', 'TIYAKA23.4%'], ['หลักสูตรวิศวกรรมศาสตรมหาบัณฑิต สาขาวิชาวิศวกรรมอุตสาหการ', 'KASESI43.4%', 'APISKE6.7%'], ['หลักสูตรวิศวกรรมศาสตรดุษฎีบัณฑิต สาขาวิชาวิศวกรรมอุตสาหการ', 'KASESI43.4%', 'APISKE6.7%'], ['หลักสูตรวิศวกรรมศาสตรดุษฎีบัณฑิต สาขาวิชาวิศวกรรมไฟฟ้า', 'CHAINU43.4%', 'TEERTI6.7%'], ['หลักสูตรวิศวกรรมศาสตรมหาบัณฑิต สาขาวิชาวิศวกรรมป้องกันประเทศ', 'PAKOWA60.0%', 'BOONSU40.0%'], ['หลักสูตรวิทยาศาสตรบัณฑิต สาขาวิชาเคมีอุตสาหกรรม', 'PINMKW40.0%', 'KANKKH38.4%'], ['หลักสูตรวิทยาศาสตรบัณฑิต สาขาวิชาวิทยาการคอมพิวเตอร์', 'BOONSU60.0%', 'WORNCH60.0%'], ['หลักสูตรวิทยาศาสตรบัณฑิต สาขาวิชาคณิตศาสตร์ประยุกต์', 'WORNCH50.0%', 'BOONSU45.0%'], ['หลักสูตรวิทยาศาสตรบัณฑิต สาขาวิชาเคมีสิ่งแวดล้อม', 'PINMKW45.0%', 'KANKKH38.4%'], ['หลักสูตรวิทยาศาสตรบัณฑิต สาขาวิชาจุลชีววิทยาอุตสาหกรรม', 'THIPLI33.4%', 'PAIBPA21.7%'], ['หลักสูตรวิทยาศาสตรบัณฑิต สาขาวิชาจุลชีววิทยาอุตสาหกรรม(หลักสูตรนานาชาติ)', 'THIPLI33.4%', 'PAIBPA21.7%'], ['หลักสูตรวิทยาศาสตรบัณฑิต สาขาวิชาเทคโนโลยีชีวภาพ', 'VASUD33.4%', 'SORAKU16.7%'], ['หลักสูตรวิทยาศาสตรบัณฑิต สาขาวิชาฟิสิกส์ประยุกต์', 'VASUD33.4%', 'SORAKU16.7%'], ['หลักสูตรวิทยาศาสตรบัณฑิต สาขาวิชาสถิติประยุกต์', 'PONRNE53.4%', 'PAKOWA40.0%'], ['หลักสูตรวิทยาศาสตรมหาบัณฑิต สาขาวิชาเคมีสิ่งแวดล้อม', 'PINMKW45.0%', 'WORAWO26.7%'], ['หลักสูตรวิทยาศาสตรมหาบัณฑิต สาขาวิชาเทคโนโลยีพอลิเมอร์', 'BUSAPI31.7%', 'KASESI28.4%'], ['หลักสูตรวิทยาศาสตรมหาบัณฑิต สาขาวิชาคณิตศาสตร์ประยุกต์', 'WORNCH50.0%', 'BOONSU45.0%'], ['หลักสูตรวิทยาศาสตรมหาบัณฑิต สาขาวิชาเคมีประยุกต์', 'PINMKW40.0%', 'KASESI23.4%'], ['หลักสูตรวิทยาศาสตรมหาบัณฑิต สาขาวิชาเทคโนโลยีชีวภาพ', 'KANKKH38.4%', '-99900%'], ['หลักสูตรวิทยาศาสตรมหาบัณฑิต สาขาวิชาปิโตรเคมีและเคมีไฮโดรคาร์บอน', 'BUSAPI31.7%', 'KASESI23.4%'], ['หลักสูตรวิทยาศาสตรมหาบัณฑิต สาขาวิชาฟิสิกส์ประยุกต์', 'WORAWO26.7%', 'SORAKU16.7%'], ['หลักสูตรวิทยาศาสตรมหาบัณฑิต สาขาวิชาวิทยาการคอมพิวเตอร์', 'PAKOWA50.0%', 'APISKE16.7%'], ['หลักสูตรวิทยาศาสตรมหาบัณฑิต สาขาวิชาสถิติและการวิเคราะห์ธุรกิจ', 'PONRNE53.4%', 'PAKOWA40.0%'], ['หลักสูตรปรัชญาดุษฎีบัณฑิต สาขาวิชาคณิตศาสตร์ประยุกต์', 'WORNCH50.0%', 'BOONSU45.0%'], ['หลักสูตรปรัชญาดุษฎีบัณฑิต สาขาวิชาเคมีประยุกต์', 'PINMKW40.0%', 'KASESI23.4%'], ['หลักสูตรปรัชญาดุษฎีบัณฑิต สาขาวิชาเทคโนโลยีชีวภาพ', 'KANKKH28.4%', 'VARAKI26.7%'], ['หลักสูตรปรัชญาดุษฎีบัณฑิต สาขาวิชาฟิสิกส์ประยุกต์', 'WORAWO26.7%', 'SORAKU16.7%'], ['หลักสูตรปรัชญาดุษฎีบัณฑิต สาขาวิชาวิทยาการคอมพิวเตอร์', 'PAKOWA50.0%', 'APISKE16.7%']]

    return result

def combine_recommendation():
    #Read data
    test_data = pd.read_excel('study_program/rating_matrix_committee.xlsx')

    recommended_committee_df = pearson_based_collaborative(test_data)
    #print(recommended_committee_df)       
    
    recommendation_committee_pearson_list = viewAllRecommendedCommittee(recommended_committee_df)
    recommendation_committee_knn_list = viewAllNewRecomendedCommittee(1)

    # might be slow
    total_recommendation_committee_dict = {}
    aee_list = []
    for new_committee in recommendation_committee_knn_list:
        for committee in recommendation_committee_pearson_list:
            # happy case, where length of program are equal
            if(new_committee[0] == committee[0]):
                program = []
                program.append(committee[0])
                #temp1 = {}
                try:
                    c = Professor.objects.get(professor_id=str(committee[1])[:6])
                    name1 = str(committee[1])[6::] + " : " +  c.name_surname
                except:
                    name1 = committee[1]

                try:
                    c = Professor.objects.get(professor_id=str(committee[2])[:6])
                    name2 = str(committee[2])[6::] + " : " + c.name_surname
                except:
                    name2 = committee[2]

                #temp1.update({'existing committee':[name1,name2]})


                #temp2 = {}
                try:
                    c = Professor.objects.get(professor_id=str(new_committee[1])[:6])
                    # print("KUAYYY   ")
                    #name1 = c.professor_id.name_surname
                    name3 = str(new_committee[1])[6::] + " : " + c.name_surname 
                    # print("NOOOOo")
                except:
                    name3 = new_committee[1]

                try:
                    c = Professor.objects.get(professor_id=str(new_committee[2])[:6])
                    name4 = str(new_committee[2])[6::] + " : " + c.name_surname 
                except:
                    name4 = new_committee[2]

                #temp2.update({'new committee': [name1, name2]})

                #program.append([temp1, temp2])
                #total_recommendation_committee_dict.update({program[0]:program[1]})
                aee_list.append([committee[0], name1, name2, name3, name4])
                #print(committee[0], committee[1], committee[2], new_committee[1], new_committee[2])

                break

    return aee_list
#    print("total_recommendation_committee_list:")
#    print(total_recommendation_committee_dict)       

@login_required(login_url="/login")
def committee_recommendation(request, page_number = 1):
    aee_list = combine_recommendation()
    temp_list = []
    faculty_search = request.GET.get('faculty_name')
    if(faculty_search != None):
        #print(faculty_search)
        for item in aee_list:
            #print(item.name)
            if faculty_search in item[0]:
                temp_list.append(item)
                
        aee_list = temp_list
    #done

    current_page = page_number
    if(current_page == 1):
        previous_page = 1
    else:
        previous_page = current_page - 1

    if(math.ceil(len(aee_list) / 10) < current_page + 1):
        next_page = current_page
    else:
        next_page = current_page + 1
    
    aee_list = aee_list[0 + current_page * 10 - 10: (current_page + 1) * 10 - 9]
    total_recommendation_committee_dict = {}
    for item in aee_list:
        temp1 = {"existing committee":[item[1], item[2]]}
        temp2 = {'new committee':[item[3], item[4]]}
        total_recommendation_committee_dict.update({item[0]:[temp1,temp2]})
    context = {'committee_recommendation_dict':total_recommendation_committee_dict, 'current_page':current_page, 'next_page':next_page, 'previous_page':previous_page}        
    


    return render(request, 'iqa_menu/committee_recommendation/committee_recommendation.html', context)


# ASSESSMENT CALENDAR
@login_required(login_url="/login")
def assessment_calendar(request, month = datetime.datetime.today().month, year = datetime.datetime.today().year):
    today = datetime.datetime.today()

    date_name = list(calendar.day_abbr)
    month_name = datetime.date(year, month, 1).strftime('%B')
    day_in_month = calendar.monthcalendar(year, month)
    print("DATEM: ", day_in_month)

    
    if(month == 12):
        next_month = 1
        next_year = year + 1
    else:
        next_month = month + 1
        next_year = year
        
    
    if(month == 1):
        prev_month = 12
        prev_year = year - 1
    else:
        prev_month = month - 1
        prev_year = year
        
    # get all dates that have appointments
    available_time_list = AvailableTime.objects.all()
    #available_time = available_time_list[0]
    
    
    if(month < 10):
        string_month = "0" + str(month)
    else:
        string_month = str(month)
    
    have_appointment_in_morning_list = []
    have_appointment_in_afternoon_list = []
    for available_time in available_time_list:
        appointed_date = str(available_time.appointment_date)
        appointment_year = appointed_date[0:4]
        appointment_month = appointed_date[5:7]
        appointment_day = appointed_date[8:10]
        
        if(string_month == appointment_month and str(year) == appointment_year):
            if(available_time.available_in_morning == "yes"):
                if appointment_day not in have_appointment_in_morning_list:
                    have_appointment_in_morning_list.append(int(appointment_day))

            if(available_time.available_in_afternoon == "yes"):
                if appointment_day not in have_appointment_in_afternoon_list:
                    have_appointment_in_afternoon_list.append(int(appointment_day))
        
    
    print(have_appointment_in_morning_list)
    print(have_appointment_in_afternoon_list)
    
    conflict_list = check_appointment_conflict()  
    
    # ECHO PRINTING: check if the conflict list is correct!
    # for item in conflict_list:
    #     print(item[0].code,":",item[1],":",item[2],":",end=" [")
    #     for faculty in item[3]:
    #         print(faculty.code, end=", ")
    #     print("]")
 

    conflict_date_list = []
    for item in conflict_list:
        conflict_date = str(item[1])
        conflict_year = conflict_date[0:4]
        conflict_month = conflict_date[5:7]
        conflict_day = conflict_date[8:10]
        if(string_month == conflict_month and str(year) == conflict_year):
            if conflict_day not in conflict_date_list:
                conflict_date_list.append(int(conflict_day))

    if(len(conflict_date_list) > 0):
        is_conflict = True
    else:
        is_conflict = False

    context = {'date_name':date_name,'day_in_month':day_in_month,'month':month , 'month_name':month_name, 'next_month':next_month,'prev_month':prev_month, 
                'year':year, 'next_year':next_year,'prev_year':prev_year, 'have_appointment_in_afternoon_list':have_appointment_in_afternoon_list,
                'have_appointment_in_morning_list':have_appointment_in_morning_list, 'conflict_date_list':conflict_date_list, 'is_conflict':is_conflict }

         
    return render(request, 'iqa_menu/assessment_calendar/assessment_calendar.html', context)



@login_required(login_url="/login")
def assessment_calendar_detail(request, day = 0, month = 0, year = 0):
    if(day < 10):
        day = '0' + str(day)
    else:
        day = str(day)
    
    if(month < 10):
        month = '0' + str(month)
    else:
        month = str(month)
    
    year = str(year)

    date = year + '-' + month + '-' + day

    print("SELECTED DATE: ",date)
    #SLEEPY WA, FIX this LATER
    morning_appointment_dict = {}
    afternoon_appointment_dict = {}

    at = AvailableTime.objects.all()
    for appointment in at:
        if(str(appointment.appointment_date) == date and appointment.available_in_morning == "yes"):
            c = appointment.appointed_committee.all()
            morning_appointment_dict.update({appointment:c})
    
    for appointment in at:  
        if(str(appointment.appointment_date) == date and appointment.available_in_afternoon == "yes"):
            c = appointment.appointed_committee.all()
            afternoon_appointment_dict.update({appointment:c})
          
    #print("OBJECT TIME: ",str(at[0].appointment_date))
    context = { 'date': date,'morning_appointment_dict':morning_appointment_dict, 'afternoon_appointment_dict':afternoon_appointment_dict}
    return render(request,  'iqa_menu/assessment_calendar/assessment_calendar_detail.html', context)

def check_appointment_conflict():
    #print("check appointment conflict")

    at = AvailableTime.objects.all()
    conflict_list = []
    for appointment in at:
        for c_appointment in at:
            if(appointment.appointment_date == c_appointment.appointment_date): # check if it is different date
                if(appointment.appointed_program != c_appointment.appointed_program): # confirm that it is different program
                    if(appointment.available_in_morning == c_appointment.available_in_morning and appointment.available_in_morning == "yes"): # case of morning assessment
                        # check if same professor
                        committees_a = appointment.appointed_committee
                        committees_a = committees_a.all()
                        
                        committees_b = c_appointment.appointed_committee
                        committees_b = committees_b.all()

                        result = check_committee_conflict(committees_a, committees_b)
                        for committee in result:
                            conflict_list.append([committee,appointment.appointment_date, appointment.appointed_program, "morning"])
                            conflict_list.append([committee,appointment.appointment_date, c_appointment.appointed_program, "morning"])

                    if(appointment.available_in_afternoon == c_appointment.available_in_afternoon and appointment.available_in_afternoon == "yes"):
                        # check if same professor
                        committees_a = appointment.appointed_committee
                        committees_a = committees_a.all()
                        
                        committees_b = c_appointment.appointed_committee
                        committees_b = committees_b.all()

                        result = check_committee_conflict(committees_a, committees_b)
                        for committee in result:
                            conflict_list.append([committee,appointment.appointment_date, appointment.appointed_program, "afternoon"])
                            conflict_list.append([committee,appointment.appointment_date, c_appointment.appointed_program, "afternoon"])
    
    conflict_list = eliminate_same_item(conflict_list)
    conflict_list = conflict_grouping(conflict_list)
    
    return conflict_list

def check_committee_conflict(committee_list_a, committee_list_b):
    #print("check professor conflict")
    conflict_list = []
    for committee in committee_list_a:
        if committee in committee_list_b:
            if committee not in conflict_list:
                conflict_list.append(committee)
    
    return conflict_list

def eliminate_same_item(conflict_list):
    new_conflict_list = [] # no redundant
    for item in conflict_list:
        #print(item[0].code,":",item[1],":",item[2].code,":",item[3])
        not_in = True
        for i in range(len(new_conflict_list)):
            if(item[0].code == new_conflict_list[i][0].code and
               item[1] == new_conflict_list[i][1] and
               item[2].code == new_conflict_list[i][2].code and
               item[3] == new_conflict_list[i][3]):
               not_in = False
               break

        if(not_in == True):
            new_conflict_list.append(item)

    return new_conflict_list

def conflict_grouping(conflict_list):
    new_conflict_list = []

    grouping_list = []
    for i in range(len(conflict_list)):
        group = []
        for j in range(len(conflict_list)):
            if(conflict_list[i][0].code == conflict_list[j][0].code and
               conflict_list[i][1] == conflict_list[j][1] and
               conflict_list[i][3] == conflict_list[j][3] and
               (conflict_list[j][2] not in group)):
               group.append(conflict_list[j][2])
        
        grouping_list.append([conflict_list[i][0],conflict_list[i][1],conflict_list[i][3], group])
    
    #return grouping_list
    for group in grouping_list:
        not_in = True
        for i in range(len(new_conflict_list)):
            if(new_conflict_list[i][0] == group[0] and
               new_conflict_list[i][1] == group[1] and
               new_conflict_list[i][2] == group[2]):
               not_in = False
               break

        if(not_in == True):
            new_conflict_list.append(group)

    return new_conflict_list



@login_required(login_url="/login")
def view_conflict_detail(request):
    conflict_date_list = check_appointment_conflict()

    conflict_date_dict = {}
    for item in conflict_date_list:
        # FORMAT STRING
        key = str(item[0].professor_id.name_surname) + " " + (str(item[1])) + " " + item[2]
        conflict_date_dict.update({key:item[3]})

    context = {'conflict_date_dict':conflict_date_dict }
    return render(request, 'iqa_menu/assessment_calendar/appointment_conflict.html', context)

# --------------------------------------------------------------------------- #



# -------------------------------- faculty_menu -------------------------------- #

@login_required(login_url="/login")
def all_faculty_program(request, page_number = 1):
    #Filters: 
    # 1 - faculties
    # 2 - degree
    # 3 - status
    # 4 - inter/thai
    # 5 - modify/new
    
    faculties_list = {
        'AAI':'วิทยาลัยอุตสาหกรรมการบินนานาชาติ', 
        'ADM':'คณะบริหารและจัดการ', 
        'AGI':'คณะอุตสาหกรรมเกษตร', 
        'AMI':'คณะเทคโนโลยีการเกษตร', 
        'ARC':'วิทยาลัยนวัตกรรมการผลิตขั้นสูง', 
        'CHP':'คณะสถาปัตยกรรมศาสตร์', 
        'EIR':'วิทยาเขตชุมพรเขตรอุดมศักดิ์', 
        'ENG':'คณะวิศวกรรมศาสตร์', 
        'ICX':'วิทยาลัยนานาขาติ', 
        'IDE':'คณะครุศาสตร์อุตสาหกรรมและเทคโนโลยี', 
        'ITX':'คณะเทคโนโลยีสารสนเทศ', 
        'LBA':'คณะศิลปศาสตร์', 
        'MED':'วิทยาลัยแพทยศาสตร์นานาชาติ', 
        'MSE':'วิทยาลัยสังคีต', 
        'NNT':'วิทยาลัยนาโนเทคโนโลยี', 
        'SCI':'คณะวิทยาศาสตร์', 
        }    

    degree_list = {
        'B':'ปริญญาตรี',
        'M':'ปริญญาโท',
        'D':'ปริญญาเอก',
    }

    study_program_list = StudyProgram.objects.all().order_by('id')

    # Get all program relating to that faculty
    temp_list = []
    for program in study_program_list:
        # !!!
        if(str(request.user.username).upper() == program.code[0:3]):
            temp_list.append(program)
    
    study_program_list = temp_list

    # check searching program
    program_list = []

    faculty_search = request.GET.get('faculty_name')
    if(faculty_search != None):
        #print(faculty_search)
        for item in study_program_list:
            #print(item.name)
            if faculty_search in item.name:
                program_list.append(item)
                
        study_program_list = program_list
    # done

    # PAGINATOR THINGSY
    page = request.GET.get('page')
    paginator = Paginator(study_program_list, 10)

    try:
        studyPrograms = paginator.page(page)
        print(type(studyPrograms))
    except PageNotAnInteger:
        print("Paginator: PageNotAnIntegerException")
        studyPrograms = paginator.page(1)
    except EmptyPage:
        print("Paginator: EmptyPageException")
        studyPrograms = paginator.page(paginator.num_pages)


    prev_page = page_number - 1
    if(page_number - 1 < 1):
        prev_page = 1 

    current_page = page_number

    next_page = page_number + 1
    
    total_program = StudyProgram.objects.count()
    #print(total_program)
    if(next_page > math.ceil(total_program/10)):
        next_page = current_page

    context = {'studyPrograms':studyPrograms, 'faculties_list':faculties_list, 'degree_list':degree_list,
               'next_page':next_page, 'current_page':current_page, 'prev_page':prev_page }


    return render(request, 'faculty_menu/faculty_study_program/all_faculty_study_program.html', context)


def faculty_program_detail(request, program_id):
    detail = get_object_or_404(StudyProgram, pk=program_id)

    professor_list = []
    for professor in detail.responsible_professors.all():
        professor_list.append(professor)

    assessment_list =[]
    assessments = AssessmentResult.objects
    for assessment in assessments.all():
        #print("asssessment",assessment.program_id)
        #print("name",detail.name)
        if(str(assessment.program_id) == detail.name):
            #print("KAO")
            assessment_list.append(assessment)

    context = {
        'program_detail': detail, 
        'professors':professor_list, 
        'assessment_list':assessment_list, 
        'program_id': program_id
        }

    return render(request, 'faculty_menu/faculty_study_program/faculty_program_detail.html', context )

#@login_required(login_url="/login")
#def committee_appointment(request):
#    return render(request, 'faculty_menu/committee_appointment/committee_appointment.html')


# --------------------------------------------------------------------------- #





# ---------------------------------------------- listItem & detail --------------------------------------------- #


# ALL PROGRAMS
@login_required(login_url='login')
def all_programs(request, page_number = 1, faculty = "-"):
    #Filters: 
    # 1 - faculties
    # 2 - degree
    # 3 - status
    # 4 - inter/thai
    # 5 - modify/new
    print("In all study proram")
    faculties_list = {
        'AAI':'วิทยาลัยอุตสาหกรรมการบินนานาชาติ', 
        'ADM':'คณะบริหารและจัดการ', 
        'AGI':'คณะอุตสาหกรรมเกษตร', 
        'AMI':'คณะเทคโนโลยีการเกษตร', 
        'ARC':'วิทยาลัยนวัตกรรมการผลิตขั้นสูง', 
        'CHP':'คณะสถาปัตยกรรมศาสตร์', 
        'EIR':'วิทยาเขตชุมพรเขตรอุดมศักดิ์', 
        'ENG':'คณะวิศวกรรมศาสตร์', 
        'ICX':'วิทยาลัยนานาขาติ', 
        'IDE':'คณะครุศาสตร์อุตสาหกรรมและเทคโนโลยี', 
        'ITX':'คณะเทคโนโลยีสารสนเทศ', 
        'LBA':'คณะศิลปศาสตร์', 
        'MED':'วิทยาลัยแพทยศาสตร์นานาชาติ', 
        'MSE':'วิทยาลัยสังคีต', 
        'NNT':'วิทยาลัยนาโนเทคโนโลยี', 
        'SCI':'คณะวิทยาศาสตร์', 
        }    

    degree_list = {
        'B':'ปริญญาตรี',
        'M':'ปริญญาโท',
        'D':'ปริญญาเอก',
    }
    # degree_list = {'b':'Bachelor', 'm':'Master', 'd':'Doctor'}

    # # status_list = {}

    from_item = (page_number * 10) - 10
    to_item = page_number * 10

    # page_number_list = [1,1,2,3,4] ##########

 

    ########################################################################
    studyProgram_list = StudyProgram.objects.all().order_by('id')
    page = request.GET.get('page')
    
    # filtering faculties
    if(faculty != "-"):
        faculty = faculty[0:3]
        faculty = faculty.upper()
    
        temp_study_list = []
        for item in studyProgram_list:
            if(item.code[0:3] == faculty):
                temp_study_list.append(item)
        
        studyProgram_list = temp_study_list
    # done

    # filtering degree
    degree = "-"
    if(degree != "-"):
        temp_study_list = []
        for item in studyProgram_list:
            if(item.code[10] == degree):
                temp_study_list.append(item) 
        studyProgram_list = temp_study_list
    # done

    # check searching program
    program_list = []

    faculty_search = request.GET.get('faculty_name')
    if(faculty_search != None):
        #print(faculty_search)
        for item in studyProgram_list:
            #print(item.name)
            if faculty_search in item.name:
                program_list.append(item)
                
        studyProgram_list = program_list
    # done


    paginator = Paginator(studyProgram_list, 10)

    try:
        studyPrograms = paginator.page(page)
    except PageNotAnInteger:
        studyPrograms = paginator.page(1)
    except EmptyPage:
        studyPrograms = paginator.page(paginator.num_pages)

    # return render(request, 'study_program/all_program.html', { 'studyPrograms': studyPrograms })
    ########################################################################

    
    for item in StudyProgram.objects.all():
        program_list.append(item)
        
    # get 10 items/ page
    program_list = program_list[from_item:to_item]

    # adjust page button
    prev_page = page_number - 1
    if(page_number - 1 < 1):
        prev_page = 1 

    current_page = page_number

    next_page = page_number + 1
    
    total_program= StudyProgram.objects.count()
    print(total_program)
    if(next_page > math.ceil(total_program/10)):
        next_page = current_page

    
    return render(request, 'study_program/all_program.html', {
        'studyPrograms': studyPrograms,
        'faculties':faculties_list,
        'degree': degree_list,
        # 'programs': program_list, 
        'current_page': current_page, 
        'prev_page': prev_page, 
        'next_page': next_page
        })

    # if(found == True):
    #     prev_page = 1
    #     current_page = 1
    #     next_page = 1
    #     prev_two_page = 1
    #     next_two_page = 1

    #     return render(request, 'study_program/all_program.html', {
    #         'studyPrograms': studyPrograms,
    #         'faculties':faculties_list,
    #         'degree': degree_list,
    #         # 'programs': program_list, 
    #         'current_page': current_page, 
    #         'prev_page': prev_page, 
    #         'next_page': next_page
    #         }) 

    # else:
    #     for item in StudyProgram.objects.all():
    #         program_list.append(item)
        
    #     # get 10 items/ page
    #     program_list = program_list[from_item:to_item]

    #     # adjust page button
    #     prev_page = page_number - 1
    #     if(page_number - 1 < 1):
    #         prev_page = 1 

    #     current_page = page_number

    #     next_page = page_number + 1
        
    #     total_program= StudyProgram.objects.count()
    #     print(total_program)
    #     if(next_page > math.ceil(total_program/10)):
    #         next_page = current_page

        
    #     return render(request, 'study_program/all_program.html', {
    #         'studyPrograms': studyPrograms,
    #         'faculties':faculties_list,
    #         'degree': degree_list,
    #         # 'programs': program_list, 
    #         'current_page': current_page, 
    #         'prev_page': prev_page, 
    #         'next_page': next_page
    #         })


# PROGRAM DETAIL
@login_required(login_url="login")
def program_detail(request, program_id):
    detail = get_object_or_404(StudyProgram, pk=program_id)

    professor_list = []
    for professor in detail.responsible_professors.all():
        professor_list.append(professor)

    assessment_list =[]
    assessments = AssessmentResult.objects
    for assessment in assessments.all():
        #print("asssessment",assessment.program_id)
        #print("name",detail.name)
        if(str(assessment.program_id) == detail.name):
            #print("KAO")
            assessment_list.append(assessment)
    
    print(detail.pdf_docs_link)
    return render(request, 'study_program/program_detail.html', {
        'program_detail': detail, 
        'professors':professor_list, 
        'assessment_list':assessment_list, 
        'program_id': program_id})


# ALL PROFESSOR
@login_required(login_url="login")
def all_professors(request, page_number=1):

    from_item = (page_number * 10) - 10
    to_item = page_number * 10

    p = Professor.objects # get object
    assessments = p.all() # get all objects
    total_assessment = p.count() # get length of object

    ########################################################################
    professor_list = Professor.objects.all().order_by('id')
    page = request.GET.get('page')

    # check searching program
    temp_list = []

    faculty_search = request.GET.get('faculty_name')
    if(faculty_search != None):
        #print(faculty_search)
        for item in professor_list:
            #print(item.name)
            if faculty_search in item.name_surname:
                temp_list.append(item)
                
        professor_list = temp_list
    # done
    
    #print(page)
    paginator = Paginator(professor_list, 10)

    try:
        professors = paginator.page(page)
    except PageNotAnInteger:
        professors = paginator.page(1)
    except EmptyPage:
        professors = paginator.page(paginator.num_pages)

    # return render(request, 'study_program/all_program.html', { 'professors': professors })
    ########################################################################
    
    assessment_list = []

    for assessment in assessments:
        assessment_list.append(assessment)
    
    # get 10 items/ page
    assessment_list = assessment_list[from_item:to_item]

    # adjust page button
    prev_page = page_number - 1
    if(page_number - 1 < 1):
        prev_page = 1  

    current_page = page_number

    next_page = page_number + 1
    if(next_page > math.ceil(total_assessment/10)):
        next_page = current_page

    return render(request, 'professor/all_professor.html', {
        'professors': professors,
        # 'professors': assessment_list, 
        'current_page': current_page, 
        'prev_page': prev_page, 
        'next_page':next_page
        })


# PROFESSOR DETAIL
@login_required(login_url="login")
def professor_detail(request, professor_id):
    profile = get_object_or_404(Professor, pk=professor_id)

    responsible_program = []
    for program in profile.responsible_program.all():
        responsible_program.append(program)

    committee_list = []
    c = Committee.objects
    committees = c.all()
    for committee in committees:
        #print("c:",committee.professor_id)
        #print("p:", profile.name_surname)
        if(str(committee.professor_id) == profile.name_surname):
            #print("KAO IF")
            committee_list.append(committee)
    '''
    for comittee_per_year in profile.committee_profile.all():
        committee_list.append(comittee_per_year)
    '''
   
    return render(request, 'professor/professor_profile.html', {
        'professor_profile': profile, 
        'responsible_program':responsible_program, 
        'committee_list':committee_list, 
        'professor_id':professor_id})


# ALL ASSESSMENTS
@login_required(login_url="login")
def all_assessments(request, page_number=1, faculty = "-"):
    faculties_list = {
        'AAI':'วิทยาลัยอุตสาหกรรมการบินนานาชาติ', 
        'ADM':'คณะบริหารและจัดการ', 
        'AGI':'คณะอุตสาหกรรมเกษตร', 
        'AMI':'คณะเทคโนโลยีการเกษตร', 
        'ARC':'วิทยาลัยนวัตกรรมการผลิตขั้นสูง', 
        'CHP':'คณะสถาปัตยกรรมศาสตร์', 
        'EIR':'วิทยาเขตชุมพรเขตรอุดมศักดิ์', 
        'ENG':'คณะวิศวกรรมศาสตร์', 
        'ICX':'วิทยาลัยนานาขาติ', 
        'IDE':'คณะครุศาสตร์อุตสาหกรรมและเทคโนโลยี', 
        'ITX':'คณะเทคโนโลยีสารสนเทศ', 
        'LBA':'คณะศิลปศาสตร์', 
        'MED':'วิทยาลัยแพทยศาสตร์นานาชาติ', 
        'MSE':'วิทยาลัยสังคีต', 
        'NNT':'วิทยาลัยนาโนเทคโนโลยี', 
        'SCI':'คณะวิทยาศาสตร์', 
        }  

    from_item = (page_number * 10) - 10
    to_item = page_number * 10

    ar = AssessmentResult.objects # get object
    assessments = ar.all() # get all objects
    total_assessment = ar.count() # get length of object

    ########################################################################
    assessment_list = AssessmentResult.objects.all().order_by('year').reverse()

    # filtering faculties
    if(faculty != "-"):
        faculty = faculty[0:3]
        faculty = faculty.upper()
    
        temp_study_list = []
        for item in assessment_list:
            if(item.code[0:3] == faculty):
                temp_study_list.append(item)
        
        assessment_list = temp_study_list
    # done

    # check searching program
    temp_list = []

    faculty_search = request.GET.get('faculty_name')
    if(faculty_search != None):
        #print(faculty_search)
        for item in assessment_list:
            #print(item.name)
            already_in = 0
            try:
                if faculty_search in item.program_id.name:
                    temp_list.append(item)
                    already_in = 1
                if faculty_search in str(item.year):
                    if(already_in == 0):
                        temp_list.append(item)
            except:
                continue
                
        assessment_list = temp_list
    # done

    page = request.GET.get('page')
    #print(page)
    paginator = Paginator(assessment_list, 10)

    try:
        assessments = paginator.page(page)
    except PageNotAnInteger:
        assessments = paginator.page(1)
    except EmptyPage:
        assessments = paginator.page(paginator.num_pages)

    # return render(request, 'study_program/all_program.html', { 'assessments': assessments })
    ########################################################################
    
    assessment_list = []

    for assessment in assessments:
        assessment_list.append(assessment)
    
    # get 10 items/ page
    assessment_list = assessment_list[from_item:to_item]

    # adjust page button
    prev_page = page_number - 1
    if(page_number - 1 < 1):
        prev_page = 1  

    current_page = page_number

    next_page = page_number + 1
    if(next_page > math.ceil(total_assessment/10)):
        next_page = current_page

   
    return render(request, 'assessment/all_assessment.html', {
        'assessments': assessments,
        # 'assessments': assessment_list, 
        'faculties':faculties_list,
        'current_page': current_page, 
        'prev_page': prev_page, 
        'next_page':next_page})


# ASSESSMENT RESULT
@login_required(login_url="login")
def assessment_result(request, assessment_id):
    detail = get_object_or_404(AssessmentResult, pk=assessment_id)

    commitee_list = []
    for committee in detail.committee_id.all():
        commitee_list.append(committee)

    #assessment_result.aun_id
    #print("AEE")
    aun_result = get_object_or_404(AUN, assessment_id=assessment_id)
    #print(aun_result)
    return render(request, 'assessment/assessment_result.html', {'assessment_result': detail, 'commitee_list':commitee_list, 'assessment_id': assessment_id,'aun_result':aun_result})


# ALL COMMITTEES
@login_required(login_url="login")
def all_committees(request, page_number=1):
        
    from_item = (page_number * 10) - 10
    to_item = page_number * 10

    c = Committee.objects # get object
    committees = c.all() # get all objects
    total_committee = c.count() # get length of object

    ########################################################################
    committee_list = Committee.objects.all().order_by('year').reverse()

    # check searching program
    temp_list = []

    faculty_search = request.GET.get('faculty_name')
    if(faculty_search != None and faculty_search != ""):   
        #print(faculty_search)
        for item in committee_list:
            #print(item.name)
            already_in = 0
            try:
                if faculty_search in str(item.year):
                    temp_list.append(item)
                    already_in = 1
                if faculty_search in item.professor_id.name_surname:
                    if already_in == 0:
                        temp_list.append(item) 
            except:
                continue
                
        committee_list = temp_list
    # done


    page = request.GET.get('page')
    #print(page)
    paginator = Paginator(committee_list, 10)

    try:
        committees = paginator.page(page)
    except PageNotAnInteger:
        committees = paginator.page(1)
    except EmptyPage:
        committees = paginator.page(paginator.num_pages)

    # return render(request, 'study_program/all_program.html', { 'committees': committees })
    ########################################################################

    committee_list = []

    for committee in committees:
        committee_list.append(committee)
    
    # get 10 items/ page
    committee_list = committee_list[from_item:to_item]

    # adjust page button
    prev_page = page_number - 1
    if(page_number - 1 < 1):
        prev_page = 1  

    current_page = page_number

    next_page = page_number + 1
    if(next_page > math.ceil(total_committee/10)):
        next_page = current_page

   
    return render(request, 'committee/all_committee.html', {
        'committees': committees,
        'committee_list': committee_list, 
        'current_page': current_page, 
        'prev_page': prev_page, 
        'next_page':next_page})
  

# COMMITTEE PROFILE
@login_required(login_url="login")
def committee_profile(request, committee_id):
    detail = get_object_or_404(Committee, pk=committee_id)

    assessment_list = []
    for assessment in detail.assessment_programs.all():
        assessment_list.append(assessment)
    
    id_kub = detail.professor_id.id
    print(id_kub)
    return render(request, 'committee/committee_detail.html', {'committee_detail': detail, 'professor_profile':id_kub, 'assessment_list': assessment_list, 'committee_id':committee_id})

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#




#---------------------------------------- CREATE -------------------------------------------------------------------------------------------------------------------------------------------#


# create study program
@user_passes_test(lambda u: u.is_superuser, login_url='all_program')
@login_required(login_url="login")
def create_study_program(request):
    form = StudyProgramForm(request.POST or None, files = request.FILES or None)
    if form.is_valid():
        #print("kao if")
        form.save()
        #print("save leaw")
        form = StudyProgramForm()
        messages.success(request, "Create form success!!")
        return redirect('all_program')

    context = { 'form': form }
    return render(request, "study_program/create_study_program.html", context)

# create faculty study program
@login_required(login_url="login")
def create_faculty_program(request):
    form = StudyProgramForm(request.POST or None, files = request.FILES or None)
    if form.is_valid():
        #print("kao if")
        form.save()
        #print("save leaw")
        form = StudyProgramForm()
        messages.success(request, 'Create form success!!')
        return redirect('all_faculty_program')

    context = { 'form': form }
    return render(request, "faculty_menu/faculty_study_program/faculty_create_study_program.html", context)

# create professor
@user_passes_test(lambda u: u.is_superuser, login_url='all_program')
@login_required(login_url="login")
def create_professor(request):
    form = ProfessorForm(request.POST or None, files = request.FILES or None)
    if form.is_valid():
        form.save()
        form = ProfessorForm()
        return redirect('all_professor')

    context = { 'form': form }
    return render(request, "professor/create_professor.html", context)


@user_passes_test(lambda u: u.is_superuser, login_url='all_program')
@login_required(login_url="login")
def create_professor_fromStudyProgram(request, program_id):
    form = ProfessorForm(request.POST or None, files = request.FILES or None)
    if form.is_valid():
        form.save()
        form = ProfessorForm()
        return redirect('program_detail', program_id = program_id)

    context = { 'form': form }
    return render(request, "professor/create_professor.html", context)


# create committee
@user_passes_test(lambda u: u.is_superuser, login_url='all_committee')
@login_required(login_url="login")
def create_committee(request):
    form = CommitteeForm(request.POST or None, files = request.FILES or None)
    if form.is_valid():
        form.save()
        form = CommitteeForm()
        return redirect('all_committee')

    context = { 'form': form }
    return render(request, "committee/create_committee.html", context)


# create assessment result
@user_passes_test(lambda u: u.is_superuser, login_url='all_assessment')
@login_required(login_url="login")
def create_assessment_result(request):
    form = AssessmentResultForm(request.POST or None, files = request.FILES or None)
    if form.is_valid():
        form.save()
        form = AssessmentResultForm()
        return redirect('create_aun')

    context = { 'form': form }
    return render(request, "assessment/create_assessment_result.html", context)

# create AUN result
@user_passes_test(lambda u: u.is_superuser, login_url='all_assessment')
@login_required(login_url="login")
def create_aun_result(request):
    form = AunForm(request.POST or None, files = request.FILES or None)
    if form.is_valid():
        form.save()
        form = AunForm()
        return redirect('all_assessment')

    context = { 'form': form }
    return render(request, "assessment/create_aun.html", context)

#-----------------------------------------------------------------------------------------------#



#---------------------------------------- EDIT --------------------------------------------------#

@user_passes_test(lambda u: u.is_superuser, login_url='all_program')
@login_required(login_url="login")
def edit_study_program(request, program_id):
    study_program = get_object_or_404(StudyProgram, pk=program_id)
    if request.method == "POST":
        #form = StudyProgramForm(request.POST, request.FILES, instance=study_program)
        form = StudyProgramForm(data = request.POST, files = request.FILES, instance=study_program)
        if form.is_valid():
            form.save()
            #ini_obj = form.save(commit=False)
            #ini_obj.save()
            return redirect('program_detail', program_id = program_id)

    else:
        form = StudyProgramForm(instance=study_program)

    context = {
        'form':form
    }
    return render(request, "study_program/edit_study_program.html", context)


@user_passes_test(lambda u: u.is_superuser, login_url='all_program')
@login_required(login_url="login")
def edit_professor_profile(request, professor_id):
    professor = get_object_or_404(Professor, pk=professor_id)
    if request.method == "POST":
        form = ProfessorForm(request.POST, instance=professor)
        if form.is_valid():
            form.save()
            return redirect('professor_profile', professor_id = professor_id)

    else:
        form = ProfessorForm(instance=professor)

    context = {
        'form':form
    }
    return render(request, "professor/edit_professor_profile.html", context)


@user_passes_test(lambda u: u.is_superuser, login_url='all_assessment')
@login_required(login_url="login")
def edit_assessment_result(request, assessment_id):
    assessment = get_object_or_404(AssessmentResult, pk=assessment_id)
    if request.method == "POST":
        form = AssessmentResultForm(request.POST, instance=assessment)
        if form.is_valid():
            form.save()
            return redirect('assessment_result', assessment_id = assessment_id)

    else:
        form = AssessmentResultForm(instance=assessment)

    context = {
        'form':form
    }
    return render(request, "assessment/edit_assessment_result.html", context)


@user_passes_test(lambda u: u.is_superuser, login_url='all_committee')
@login_required(login_url="login")
def edit_committee_profile(request, committee_id):
    committee = get_object_or_404(Committee, pk=committee_id)
    if request.method == "POST":
        form = CommitteeForm(request.POST, instance=committee)
        if form.is_valid():
            form.save()
            return redirect('committee_profile', committee_id = committee_id)

    else:
        form = CommitteeForm(instance=committee)

    context = {
        'form':form
    }
    return render(request, "committee/edit_committee_profile.html", context)

#-----------------------------------------------------------------------------------------------------#



#------------------------------- Committeee Appointment ----------------------------------------------#

#@user_passes_test(lambda u: u.is_superuser, login_url='all_committee')
@login_required(login_url="login")
def committee_appointment(request):

    at = AvailableTime.objects # get object
    atObject = at.all().order_by('id').reverse() # get all objects
    total_AvailableTime = at.count() # get length of object

    available_list = []

    for available_time in atObject:
        print(available_time.user)
        if(available_time.user == request.user.username):
            available_list.append(available_time)
    
    print("AVAILABLE TIME:",available_list)
    page = request.GET.get('page')
    #print(page)
    paginator = Paginator(available_list, 10)

    try:
        available_time_for_user = paginator.page(page)
        print(type(available_time_for_user))
    except PageNotAnInteger:
        print("KAO NOTiNT")
        available_time_for_user = paginator.page(1)
    except EmptyPage:
        print("KAO EMPTY PAGE")
        available_time_for_user = paginator.page(paginator.num_pages)

    context = {'available_time_for_user': available_time_for_user }
    return render(request, 'faculty_menu/committee_appointment/committee_appointment.html', context)



#@user_passes_test(lambda u: u.is_superuser, login_url='all_committee')
@login_required(login_url="login")
def create_committee_appointment(request):
    if request.user.is_authenticated:
        user = request.user.username


    form = AvailableTimeForm(request.POST or None, files = request.FILES or None)
    print(form['user'].data)
    print(form['appointment_date'].data)

    
    if form.is_valid():
        print("FORM IS VALID")
        try:
            # no date, user, and program are the same
            ae = AvailableTime.objects.get(appointment_date=form['appointment_date'].data, user=form['user'].data, appointed_program=form['appointed_program'].data)
            print("--- get ---")
            print(ae.appointment_date)
            print(ae.user)
            #print(ae.appointed_program)
            print("-----------")
            if(str(ae.appointment_date) != str(form['appointment_date'].data)):
                print("create new object: date is not the same")
                form.save()
                form = AvailableTimeForm()
                return redirect('committee_appointment')
                
        except AvailableTime.DoesNotExist:
            print("create new object: totally new object")
            form.save()
            form = AvailableTimeForm()
            return redirect('committee_appointment')
        
        except AvailableTime.MultipleObjectsReturned:
            print("already exist!!!")
            return redirect('committee_appointment')
        else:
            # check if this case really in???
            print("kao HMMM!?!?!")
            return redirect('committee_appointment')
    else:
        print("form INVALID")
    
    form = AvailableTimeForm(initial={'appointment_date':str(datetime.datetime.now())[0:10],'user':user})
    context = {'form': form }
    print("EWWW")

    return render(request, 'faculty_menu/committee_appointment/create_appointment_time.html', context)


#@user_passes_test(lambda u: u.is_superuser, login_url='all_committee')

@login_required(login_url="login")
def edit_committee_appointment(request, available_time_id):
    available_time = get_object_or_404(AvailableTime, pk=available_time_id)
    print(available_time)
    if request.method == "POST":
        form = AvailableTimeForm(request.POST, instance=available_time)
        if form.is_valid():
            form.save()
            return redirect('committee_appointment')

    else:
        form = AvailableTimeForm(instance=available_time)

    context = {
        'form':form
    }
    return render(request, 'faculty_menu/committee_appointment/edit_appointment_time.html', context)


#------------------------------------------------------------------------------------------------------------#
def export_studyprogram_csv(request):
    response = HttpResponse(content_type='text/xlsx')
    response['Content-Disposition'] = 'attachment; filename="studyprogram.csv"'
    response.write(u'\ufeff'.encode('utf8'))

    writer = csv.writer(response)
    writer.writerow(['Program', 'Program Status', 'Degree & Major', 'Program Collaborations with Other Insitues', 'docs', 'pdf_docs_link'])
    
    studyPrograms = StudyProgram.objects.all().values_list('name', 'program_status', 'degree_and_major', 'collaboration_with_other_institues', 'pdf_docs','pdf_docs_link')
    for studyProgram in studyPrograms:
        writer.writerow(studyProgram)

    return response

    # response = HttpResponse(content_type='text/xlsx')
    # response['Content-Disposition'] = 'attachment; filename="records.xlsx"'
    # response.write(u'\ufeff'.encode('utf8'))
    # writer = csv.writer(response) 
    # writer.writerow([''])          
    # writer.writerow(['บริษัท สยาม รีเทล ดีเวลล็อปเม้นท์ จำกัด'])
    # show_date = "รายงานสรุปการเก็บเงินประจำวัน ตั้งแต่วันที่ "+str(date_start)+" ถึง "+str(date_end)
    # writer.writerow([show_date])
    # writer.writerow([''])
    # writer.writerow(['Lease Number','Shop Name','Customer Name',
    # 'วันที่เริ่มต้นสัญญา','วันที่สิ้นสุดสัญญา','ประเภทของสัญญา',
    # 'ยอดรวมทั้งสิ้น','ยอดจดยอด','เก็บเงินสด','EDC ศูนย์ฯ','EDC ร้านค้า','Voucher','Remark'])
    # writer.writerow([''])


def export_professor_csv(request):
    response = HttpResponse(content_type='text/xlsx')
    response['Content-Disposition'] = 'attachment; filename="professor.csv"'
    response.write(u'\ufeff'.encode('utf8'))

    writer = csv.writer(response)
    writer.writerow(['academic_title', 'name_surname', 'date_of_birth', \
        'bsc', 'bsc_grad_institute', 'bsc_year', 'msc', 'msc_grad_institute', 'msc_year', 'phd', 'phd_grad_institute', 'phd_year', \
            'phone', 'email', 'university', 'additional_degree'])
    
    professors = Professor.objects.all().values_list('academic_title', 'name_surname', 'date_of_birth', \
        'bsc', 'bsc_grad_institute', 'bsc_year', 'msc', 'msc_grad_institute', 'msc_year', 'phd', 'phd_grad_institute', 'phd_year', \
            'phone', 'email', 'university', 'additional_degree')
    for professor in professors:
        writer.writerow(professor)

    return response


def export_assessment_csv(request):
    response = HttpResponse(content_type='text/xlsx')
    response['Content-Disposition'] = 'attachment; filename="assessments.csv";'
    response.write(u'\ufeff'.encode('utf8'))

    writer = csv.writer(response)
    writer.writerow(['assessment_id', 'assessment_code','faculty_name', 'assessment_year', 'pdf_docs', 'pdf_docs_link', 'committee names'])
    
    all_as = AssessmentResult.objects.all()


    for a in all_as:
        try:
            committee_name_list = []
            for item in a.committee_id.all():
                committee_name_list.append(item.professor_id.name_surname)
            response_list = [a.id, a.code, a.program_id.name, str(a.year), a.pdf_docs, a.pdf_docs_link]
            response_list = response_list + committee_name_list
            writer.writerow(response_list)
        except:
            writer.writerow([a.id, a.code, a.program_id, a.year, a.pdf_docs, a.pdf_docs_link])




    return response


def export_aun_csv(request):
    response = HttpResponse(content_type='text/xlsx')
    response['Content-Disposition'] = 'attachment; filename="aun.csv"'
    response.write(u'\ufeff'.encode('utf8'))

    writer = csv.writer(response)
    writer.writerow(['AUN Code', 'Criteria 1', 'Criteria 2','Criteria 3','Criteria 4','Criteria 5','Criteria 6','Criteria 7','Criteria 8','Criteria 9','Criteria 10','Criteria 11','Criteria Total',])
    
    AUNs = AUN.objects.all()
    for aun in AUNs:
        response_list = [aun.assessment_id.code, aun.criteria1, aun.criteria2, aun.criteria3, aun.criteria4, aun.criteria5, aun.criteria6, aun.criteria7, aun.criteria8, aun.criteria9, aun.criteria10, aun.criteria11, aun.total_score]
        writer.writerow(response_list)

    return response

def export_committee_csv(request):
    response = HttpResponse(content_type='text/xlsx')
    response['Content-Disposition'] = 'attachment; filename="committee.csv"'
    response.write(u'\ufeff'.encode('utf8'))

    writer = csv.writer(response)
    writer.writerow(['committee_code', 'committee_name', 'year', 'assessment_level', 'profession', 'assessment_programs'])
    
    committees = Committee.objects.all()
    for c in committees:
        response_list = [ c.code, c.professor_id.name_surname, str(c.year), c.assessment_level, c.profession ] 
        try:
            assessed_program_list = []
            for item in c.assessment_programs.all():
                assessed_program_list.append(item.program_id.name)

            response_list = response_list + assessed_program_list   
            writer.writerow(response_list) 
        except:
            writer.writerow(response_list)
        

    return response


def export_committee_recommendation_csv(request):
    response = HttpResponse(content_type='text/xlsx')
    response['Content-Disposition'] = 'attachment; filename="committee_recommendation.csv"'
    response.write(u'\ufeff'.encode('utf8'))

    writer = csv.writer(response)
    writer.writerow(['หลักสูตร', 'กรรมการเก่า1', 'กรรมการเก่า2', 'กรรมการใหม่1', 'กรรมการใหม่2'])

    aee_list = combine_recommendation()    
    for item in aee_list:
        response_list = [item[0],item[1],item[2],item[3],item[4]]
        writer.writerow(response_list)
    return response



#--------------------------------------------- Inbox System ------------------------------------------------#

def inbox(request):
    if(request.user.is_authenticated):
        user = request.user.username
    
    if(user == 'admin'): ### AUTHENTICATION ###
        user = 'admin'
    
    iss = Issue.objects.all().order_by('id').reverse()

    issue_list = []

    for item in iss:
        issue_list.append(item)
    
    ########################################################################
    page = request.GET.get('page')
    paginator = Paginator(issue_list, 10)

    try:
        issue_list = paginator.page(page)
    except PageNotAnInteger:
        issue_list = paginator.page(1)
    except EmptyPage:
        issue_list = paginator.page(paginator.num_pages)
    ########################################################################

    context = {'issue_list':issue_list, 'user':user }
    return render(request, 'inbox/inbox_main_page.html', context)


def issue_detail(request, issue_id):
    if(request.user.is_authenticated):
        user = request.user.username

    detail = get_object_or_404(Issue, pk=issue_id)

    comment_list = []
    #print(detail.id)
    for comment in Comment.objects.all():
        if(comment.comment_for == str(detail.id)):
            comment_list.append(comment)

    context = {'detail':detail, 'comments':comment_list, 'issue_id':issue_id, 'user':user}
    return render(request, 'inbox/issue_detail.html',context)

def create_issue(request):
    if(request.user.is_authenticated):
        user = request.user.username

    form = IssueForm(request.POST or None, files = request.FILES or None)
    if form.is_valid():
        form.save()
        form = IssueForm()
        return redirect('inbox')
    
    form = IssueForm(initial={'sender':user, 'receiver':'admin'})
    context = { 'form': form }
    return render(request, "inbox/create_issue.html", context)


def create_comment(request, issue_id):
    if(request.user.is_authenticated):
        user = request.user.username

    form = CommentForm(request.POST or None, files = request.FILES or None)
    if form.is_valid():
        form.save()
        form = CommentForm()
        return redirect('issue_detail', issue_id=issue_id)
    
    issue = get_object_or_404(Issue, pk=issue_id)
    form = CommentForm(initial={'comment_for':str(issue.id), 'sender':user})

    context = {'form': form, 'issue':issue}
    return render(request, "inbox/create_comment.html", context)


def edit_issue(request, issue_id):
    issue = get_object_or_404(Issue, pk=issue_id)
    #print(issue)
    if request.method == "POST":
        form = IssueForm(request.POST, instance=issue)
        if form.is_valid():
            form.save()
            return redirect('inbox')

    else:
        form = IssueForm(instance=issue)

    context = {
        'form':form
    }
    return render(request, 'inbox/edit_issue.html', context)


def edit_comment(request, issue_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    #print(issue)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('issue_detail', issue_id=issue_id)

    else:
        form = CommentForm(instance=comment)

    context = {'form':form}
    return render(request, 'inbox/edit_comment.html', context)

#-------------------------------------------------------------------------------------------------------------#

