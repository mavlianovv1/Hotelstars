from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

W = {"class": "field__input"}

class RegisterForm(UserCreationForm):
    email      = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={**W, "placeholder": "you@email.com"}),
        label="Email",
    )
    first_name = forms.CharField(
        max_length=100, required=False,
        widget=forms.TextInput(attrs={**W, "placeholder": "Имя"}),
        label="Имя",
    )
    last_name  = forms.CharField(
        max_length=100, required=False,
        widget=forms.TextInput(attrs={**W, "placeholder": "Фамилия"}),
        label="Фамилия",
    )

    class Meta:
        model  = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({**W, "placeholder": "Имя пользователя"})
        self.fields["username"].label = "Логин"
        self.fields["password1"].widget.attrs.update({**W, "placeholder": "Пароль"})
        self.fields["password1"].label = "Пароль"
        self.fields["password2"].widget.attrs.update({**W, "placeholder": "Повторите пароль"})
        self.fields["password2"].label = "Подтверждение пароля"
