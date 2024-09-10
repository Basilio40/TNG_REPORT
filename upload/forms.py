from django import forms

class ImportarDadosForm(forms.Form):
    faturamento = forms.FileField()
    
class ImportarSimulacaoForm(forms.Form):
    Simulações = forms.FileField()