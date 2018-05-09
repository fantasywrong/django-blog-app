from django import forms

def min_len_3_validator(value):
    if len(value) < 3:
        raise forms.ValidationError('3글자 이상 입력해 주세요.')

class PostForm(forms.Form):
    title = forms.CharField(validators = [min_len_3_validator]) # 여러개 사용 가능.
    text = forms.CharField(widget=forms.Textarea)
