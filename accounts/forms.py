from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm

User = get_user_model()


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(
            attrs={
                "placeholder": "seu@email.com",
                "autocomplete": "email",
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password"].widget.attrs.update(
            {
                "placeholder": "Sua senha secreta",
                "autocomplete": "current-password",
            }
        )
        self.fields["password"].label = "Senha"


class StudentRegistrationForm(forms.Form):
    nome_completo = forms.CharField(
        label="Nome completo",
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Seu nome",
                "autocomplete": "name",
            }
        ),
    )
    email = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(
            attrs={
                "placeholder": "seu@email.com",
                "autocomplete": "email",
            }
        ),
    )
    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Crie uma senha segura",
                "autocomplete": "new-password",
            }
        ),
    )

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Este e-mail já está cadastrado.")
        return email

    def _generate_username(self, email):
        base = email.split("@")[0]
        username = base
        suffix = 1
        while User.objects.filter(username=username).exists():
            username = f"{base}{suffix}"
            suffix += 1
        return username

    def save(self):
        data = self.cleaned_data
        username = self._generate_username(data["email"])
        user = User.objects.create_user(
            username=username,
            email=data["email"],
            password=data["password"],
            first_name=data["nome_completo"].strip(),
            role=User.Role.STUDENT,
        )
        return user
