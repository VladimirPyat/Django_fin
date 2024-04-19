from django import forms
from django.contrib.auth.password_validation import CommonPasswordValidator

class RegisterForm(forms.Form):
    login_ = forms.CharField(max_length=50, label='Логин',
                           widget=forms.TextInput(attrs={'required': 'True'}))
    password = forms.CharField(max_length=50, label='Пароль', widget=forms.PasswordInput(attrs={'required': 'True'}))
    confirm_password = forms.CharField(max_length=50, label='Подтверждение пароля',
                                       widget=forms.PasswordInput(attrs={'required': 'True'}))
    email = forms.EmailField(label='email')


    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Пароли не совпадают. Попробуйте еще раз.")

        return cleaned_data

