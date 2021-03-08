from django import forms
CHOICES=[('1',' 1'),
         ('2',' 2')]
class Answer(forms.ModelForm):
    answer = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)