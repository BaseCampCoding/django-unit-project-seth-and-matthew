from django import forms
CHOICES=[('1','1'),
         ('2','2'),
         ('3','3'),
         ('4','4'),]
class Answer(forms.ModelForm):
    answer = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)