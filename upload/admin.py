from django.contrib import admin
from .models import Cliente,Fatura
from .models import Conta
from .models import Simulacao,DadosFatura,DadosMedicao,DadosEconomia

admin.site.register(Cliente)
admin.site.register(Conta)
admin.site.register(Fatura)
admin.site.register(Simulacao)
admin.site.register(DadosFatura)
admin.site.register(DadosMedicao)
admin.site.register(DadosEconomia)


# Register your models here.
