from django import forms
CHOICES=[('1','1'),
        ('2','2'),
        ('3','3'),
        ('4','4'),]
class AnswerForm(forms.Form):
    answer = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    # class Meta:
    #     
    #     answer = forms.ChoiceField(choices=CHOICES, , label="hi")