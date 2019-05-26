from django import forms
from .models import StudyProgram, Professor, AssessmentResult, Committee, AUN, Issue, Comment
from .models import AvailableTime

class StudyProgramForm(forms.ModelForm):
    class Meta:
        model = StudyProgram
        fields = [
            'code', 'name', 'program_status', 'degree_and_major', 'collaboration_with_other_institues',
            'pdf_docs', 'pdf_docs_link', 'responsible_professors'
        ]
        

class ProfessorForm(forms.ModelForm):
    class Meta:
        model = Professor
        fields = [
            'professor_id','academic_title', 'name_surname', 'date_of_birth', 'bsc', 'bsc_grad_institute', 'bsc_year',
            'msc', 'msc_grad_institute', 'msc_year', 'phd', 'phd_grad_institute', 'phd_year', 'phone',
            'email', 'university', 'additional_degree', 'responsible_program'
        ]
       
        widgets = {'date_of_birth': forms.TextInput(attrs={'placeholder':'i.e. 2549-06-25'})} # might be a root of form problemssss


class AssessmentResultForm(forms.ModelForm):
    class Meta:
        model = AssessmentResult
        fields = [
            'code','committee_id', 'program_id', 'year', 'curriculum_status', 'curriculum_status_year', 'curriculum_standard',
            'pdf_docs', 'pdf_docs_link'
        ]
         

class CommitteeForm(forms.ModelForm):
    class Meta:
        model = Committee
        fields = [
            'code', 'professor_id','year', 'assessment_level', 'profession', 'assessment_programs'
        ]


class AunForm(forms.ModelForm):
    class Meta:
        model = AUN
        fields = [
            'assessment_id', 'criteria1', 'criteria2', 'criteria3', 'criteria4', 'criteria5', 'criteria6', 
            'criteria7', 'criteria8', 'criteria9', 'criteria10', 'criteria11', 'total_score',

        ]


class AvailableTimeForm(forms.ModelForm):
    class Meta:
         model = AvailableTime
         fields = ['appointment_date','available_in_morning','available_in_afternoon','appointed_committee','appointed_program','user']
         widgets = {'user': forms.HiddenInput(), 'appointment': forms.TextInput(attrs={'placeholder':'i.e. 2549-06-25'})}
        

class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = [
            'receiver', 'sender', 'sending_time', 'topic', 'content'
        ]
        widgets = {'sender':forms.HiddenInput(), 'receiver':forms.HiddenInput(), 'sending_time':forms.HiddenInput(),
                    'content':forms.Textarea(attrs={'rows':4, 'cols':15}) }
        #sending time shold disable

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'comment_for', 'content', 'sender'
        ]
        widgets = {'comment_for':forms.HiddenInput(), 'sender':forms.HiddenInput(),
                   'content':forms.Textarea(attrs={'rows':4, 'cols':15}) }