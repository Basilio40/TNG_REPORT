from django import forms


class ImportarDadosForm(forms.Form):
    faturamento = forms.FileField()


class ImportarSimulacaoForm(forms.Form):
    Simulações = forms.FileField()


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
