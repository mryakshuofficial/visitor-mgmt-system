from django import forms

class ChangePasswordForm(forms.Form):
    gr_no = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)