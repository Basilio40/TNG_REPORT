from django.db import models

# Create your models here.
class Cliente(models.Model):
    nome = models.CharField(max_length=255,blank=True,null=True)
    modalidade=models.CharField(max_length=50,blank=True,null=True)
    distribuidora = models.CharField(max_length=100,blank=True,null=True)
    grupo = models.CharField(max_length=200,blank=True,null=True)
    

    def __str__(self):
        return self.nome

class Conta(models.Model):
    cliente = models.ForeignKey(
        Cliente, on_delete=models.CASCADE, related_name='contas',blank=True,null=True)
    descricao = models.CharField(max_length=100,blank=True,null=True)
    unidade = models.CharField(max_length=255,blank=True,null=True)
    quantidade_kw = models.FloatField(blank=True,null=True)
    unid_c_tributos = models.FloatField(blank=True,null=True)
    valor_unit = models.FloatField(blank=True,null=True)
    pis_cofins = models.FloatField(blank=True,null=True)
    base_icms = models.FloatField(blank=True,null=True)
    aliquota_icms = models.FloatField(blank=True,null=True)
    valor_icms = models.FloatField(blank=True,null=True)
    tarifa_unitaria = models.FloatField(blank=True,null=True)

    def __str__(self):
        return f"{self.descricao}"

class Fatura(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='faturas')
    mes = models.CharField(max_length=20)
    ano=models.IntegerField(blank=True,null=True)
    valor_fatura = models.DecimalField(max_digits=15, decimal_places=4,blank=True,null=True)
    valor_demanda_max = models.DecimalField(max_digits=15, decimal_places=4,blank=True,null=True)

    def __str__(self):
        return f"{self.mes}/{self.ano}"

class Simulacao(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='simulacao')
    itens_fat = models.CharField(max_length=100,blank=True,null=True)
    unidade = models.CharField(max_length=255,blank=True,null=True)
    quantidade_kw = models.FloatField(blank=True,null=True)
    unit_c_trib = models.FloatField(blank=True,null=True)
    aliquota_icms = models.FloatField(blank=True,null=True)
    aliquota_pis = models.FloatField(blank=True,null=True)
    def calculo(self,*args, **kwargs):
        if self.quantidade_kw is None or self.unit_c_trib is None:
            raise ValueError("Quantidade e unidade de custo devem ser definidos.")
        self.valor = self.quantidade_kw * self.unit_c_trib
        self.pis_cofins = self.valor*self.aliquota_pis/100
        self.base_icms = self.valor
        self.icms = self.base_icms*self.aliquota_icms
        self.valor_s_trib = self.valor - self.pis_cofins - self.icms
        self.tarifa_unit =  self.valor_s_trib / self.quantidade_kw

class DadosFatura(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='datafat')
    inicio_leitura = models.CharField(max_length=100,blank=True,null=True)
    fim_leitura = models.CharField(max_length=100,blank=True,null=True)
    valor = models.FloatField(blank=True,null=True)
    fator_carga = models.CharField(max_length=100,blank=True,null=True)
    consumo = models.CharField(max_length=100,blank=True,null=True)
    custo_medio = models.CharField(max_length=100,blank=True,null=True)
    concessionaria = models.CharField(max_length=100,blank=True,null=True)
    
class DadosMedicao(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='datamed')
    volume_total = models.CharField(max_length=100,blank=True,null=True)
    total_s_icms = models.CharField(max_length=100,blank=True,null=True)
    consumo_mwh = models.CharField(max_length=100,blank=True,null=True)
    consumo_perda = models.CharField(max_length=100,blank=True,null=True)
    percentual = models.CharField(max_length=100,blank=True,null=True)
    proinfa = models.CharField(max_length=100,blank=True,null=True)
    consumo_perda_p = models.CharField(max_length=100,blank=True,null=True)
    codigo = models.CharField(max_length=100,blank=True,null=True)
    concessionaria = models.CharField(max_length=100,blank=True,null=True)
    qtd_contrat = models.CharField(max_length=100,blank=True,null=True)
    flex_min = models.CharField(max_length=100,blank=True,null=True)
    flex_max = models.CharField(max_length=100,blank=True,null=True)
    contrato_longo = models.CharField(max_length=100,blank=True,null=True)
    preco = models.CharField(max_length=100,blank=True,null=True)
    total_sem_icms = models.CharField(max_length=100,blank=True,null=True)
    preco_r = models.CharField(max_length=100,blank=True,null=True)
    encargos = models.CharField(max_length=100,blank=True,null=True)
    valor_nf = models.CharField(max_length=100,blank=True,null=True)
    
class DadosEconomia(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='dataecon')
    enel_tranding = models.FloatField(blank=True,null=True)
    cativo_total = models.FloatField(blank=True,null=True)
    cativo_fat = models.FloatField(blank=True,null=True)
    @property
    def livre(self):
        return self.cativo_fat + self.enel_tranding if self.enel_tranding else self.cativo_fat
    @property
    def economia(self):
        return self.cativo_total - self.livre if self.cativo_total else None
        

    