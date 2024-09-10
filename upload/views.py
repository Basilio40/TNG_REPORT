from io import BytesIO
from django.conf import settings
import pandas as pd
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from .forms import ImportarDadosForm,ImportarSimulacaoForm
from django.http import FileResponse, JsonResponse,HttpResponse
from .models import Cliente, Conta, Fatura,Simulacao,DadosFatura,DadosMedicao,DadosEconomia
from django.db.models import Sum, Count
from xhtml2pdf import pisa
from django.template import Context
from django.template.loader import get_template
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import tempfile
# import weasyprint
# from weasyprint import HTML
from django.template.loader import render_to_string
import datetime
import pdfkit
import os
import time
from . import views
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os


class ImportarDadosView(View):
    template_name = 'importar_dados.html'

    def get(self, request):
        clientes = Cliente.objects.all()
        conta = Conta.objects.all()
        form = ImportarDadosForm()
        return render(request, self.template_name, {
            'form': form,
            'clientes': clientes,
            'conta':conta
        })

    def post(self, request):
        form = ImportarDadosForm(request.POST, request.FILES)

        if form.is_valid():
            arquivo = request.FILES['arquivo']
            df = pd.read_excel(arquivo)

            for _, row in df.iterrows():
                self.criar_cliente_e_endereco(row)

            return redirect('importar_dados')

        return render(request, self.template_name, {'form': form})

    def criar_cliente_e_endereco(self, row):
        # Use get_or_create para evitar a necessidade de verificar a existência antes de criar
        cliente, criado = Cliente.objects.get_or_create(
            nome=row['nome'],
            defaults={
                'nome': row['nome'],
            }
        )
        Conta.objects.create(
                cliente=cliente,
                descricao=row['descricao'],
                unidade=row['unidade'],
                quantidade_kw=row['quantidade_kw'],
                unid_c_tributos=row['unid_c_tributos'],
                valor_unit=row['valor_unit'],
                pis_cofins=row['pis_cofins'],
                base_icms=row['base_icms'],
                aliquota_icms=row['aliquota_icms'],
                valor_icms=row['valor_icms'],
                tarifa_unitaria=row['tarifa_unitaria'],
            )
        
class ImportarSimulacaoView(View):
    template_name = 'importacoes.html'

    def get(self, request):
        clientes = Cliente.objects.all()
        simulacao = Simulacao.objects.all()
        form1 = ImportarSimulacaoForm()
        return render(request, self.template_name, {
            'form1': form1,
            'clientes': clientes,
            'simulacao':simulacao
        })

    def post(self, request):
        form = ImportarDadosForm(request.POST, request.FILES)

        if form.is_valid():
            arquivo = request.FILES['arquivo']
            df = pd.read_excel(arquivo)

            for _, row in df.iterrows():
                self.criar_cliente_e_endereco(row)

            return redirect('importacoes')

        return render(request, self.template_name, {'form': form})

    def criar_cliente_e_endereco(self, row):
        # Use get_or_create para evitar a necessidade de verificar a existência antes de criar
        cliente, criado = Cliente.objects.get_or_create(
            nome=row['nome'],
            defaults={
                'nome': row['nome'],
            }
        )
        Simulacao.objects.create(
                cliente=cliente,
                itens_fat=row['descricao'],
                unidade=row['unidade'],
                quantidade_kw=row['quantidade_kw'],
                unit_c_trib=row['unit_c_trib'],
                aliquota_icms=row['aliquota_icms'],
                aliquota_pis=row['aliquota_pis'],
            )


def capa(request):
    return render(request,'capa.html')

def relatorio(request):
    return render(request,'relatorio.html')

def historico(request):
    return render(request,'historico.html')

def abertura(request):
    cliente = Cliente.objects.last()
    return render(request,'abertura_relat.html',{'cliente':cliente})

class Graf1View(View):
    template_name = 'graf_hist.html'

    def get(self, request):
        clientes = Cliente.objects.all()
        conta = Conta.objects.all()
        fatura =Fatura.objects.first()
        dados_fatura = DadosFatura.objects.all()
        return render(request, self.template_name, {
            'clientes': clientes,
            'conta':conta,
            'fatura':fatura,
            'dados_fatura':dados_fatura,
            
        })

class Graf2View(View):
    template_name = 'graf_custo.html'

    def get(self, request):
        clientes = Cliente.objects.all()
        contas = Conta.objects.all()
        return render(request,'graf_custo.html')

def faturamento(request):
    clientes = Cliente.objects.all()
    conta = Conta.objects.all()
    return render(request, 'faturamento.html', {
            'clientes': clientes,
            'conta':conta
        })
    
    
def input_dados_fat(request):
    clientes = Cliente.objects.all()
    if request.method == "GET":
        return render(request, 'input_dados_fat.html',{'clientes':clientes})
    elif request.method == "POST":
        cliente_nome = request.POST.get('cliente')
        cliente = Cliente.objects.get(nome=cliente_nome)
        inicio = request.POST.get('inicio')
        fim = request.POST.get('fim')
        valor = request.POST.get('valor')
        fator = request.POST.get('fator')
        consumo = request.POST.get('consumo')
        custo = request.POST.get('valor')
        concessionaria = request.POST.get('concessionaria')
        
        dados_fat = DadosFatura(cliente=cliente,
                                inicio_leitura=inicio,
                                fim_leitura=fim,
                                valor=valor,
                                fator_carga=fator,
                                consumo=consumo,
                                custo_medio=custo,
                                concessionaria=concessionaria,
                                )
        
        dados_fat.save()
        return redirect('input_fat')
    return render(request, 'input_dados_fat.html',{'clientes':clientes})

def faturamento_mensal(request):
    clientes = Cliente.objects.all().aggregate(Count('nome'))['nome__count']
    nome_cliente = Cliente.objects.filter(nome__startswith="B")
    nomes = [cliente.nome for cliente in nome_cliente]
    quantidade_kw_total = Conta.objects.all().aggregate(Sum('quantidade_kw'))['quantidade_kw__sum']
    valor_unit_total = Conta.objects.all().aggregate(Sum('valor_unit'))['valor_unit__sum']
    total_demanda = Conta.objects.filter(descricao__icontains='DEMANDA').aggregate(total=Sum('valor_unit'))
    demanda = total_demanda['total'] if total_demanda['total'] is not None else 0
    total_consumo = Conta.objects.filter(descricao__icontains='CONSUMO').aggregate(total=Sum('valor_unit'))
    consumo = total_consumo['total'] if total_consumo['total'] is not None else 0
    data = {
        # 'contas_clientes': [cliente.id for cliente in contas_clientes],  # Exemplo: retornando IDs dos clientes
        'clientes':clientes,
        'dado2':[demanda,consumo]
        }
    return JsonResponse(data)

def custo_mensal(request):
    valor_unit_total = Conta.objects.all().aggregate(Sum('valor_unit'))['valor_unit__sum']
    total_demanda = Conta.objects.filter(descricao__icontains='DEMANDA').aggregate(total=Sum('valor_unit'))
    demanda = total_demanda['total'] if total_demanda['total'] is not None else 0
    total_consumo = Conta.objects.filter(descricao__icontains='CONSUMO').aggregate(total=Sum('valor_unit'))
    consumo = total_consumo['total'] if total_consumo['total'] is not None else 0
    custo = {
        'dado2':[consumo,demanda]
        }
    return JsonResponse(custo)

def historico_fatura(request):
    faturas = Fatura.objects.all()
    fatura_mes=[fatura.valor_fatura for fatura in faturas]
    mes_fatura =[fatura.mes for fatura in faturas]
    ano_fatura = Fatura.objects.last()
    historico = {
        'mes':["Janeiro","Fevereiro","Março",  "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"],
        'valor':[fatura.valor_fatura for fatura in faturas],
        'ano':2024,
        }
    
    return JsonResponse(historico)

def demanda_mensal(request):
    faturas = Fatura.objects.all()
    
    demanda_mes = {
        'mes':["Janeiro","Fevereiro","Março",  "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"],
        'valor':[fatura.valor_demanda_max for fatura in faturas],
        'ano':2024
        }
    return JsonResponse(demanda_mes)

def input_medicao(request):
    clientes = Cliente.objects.all()
    if request.method == "GET":
        return render(request, 'input_medicao.html',{'clientes':clientes})
    
    elif request.method == "POST":
        cliente_nome = request.POST.get('cliente')
        cliente = Cliente.objects.get(nome=cliente_nome)
        volume_total = request.POST.get('volume_total')
        total_s_icms = request.POST.get('total_s_icms')
        consumo_mwh = request.POST.get('consumo_mwh')
        consumo_perda = request.POST.get('consumo_perda')
        percentual = request.POST.get('percentual')
        proinfa = request.POST.get('proinfa')
        consumo_perda_p = request.POST.get('consumo_perda_p')
        codigo = request.POST.get('codigo')
        concessionaria = request.POST.get('concessionaria')
        qtd_contrat = request.POST.get('qtd_contrat')
        flex_min = request.POST.get('flex_min')
        flex_max = request.POST.get('flex_max')
        contrato_longo = request.POST.get('contrato_longo')
        preco = request.POST.get('preco')
        total_sem_icms = request.POST.get('total_sem_icms')
        preco_r = request.POST.get('preco_r')
        encargos = request.POST.get('encargos')
        valor_nf = request.POST.get('valor_nf')
        
        dados_med = DadosMedicao(cliente=cliente,
                                volume_total = volume_total,
                                total_s_icms = total_s_icms,
                                consumo_mwh = consumo_mwh,
                                consumo_perda = consumo_perda,
                                percentual = percentual,
                                proinfa = proinfa,
                                consumo_perda_p = consumo_perda_p,
                                codigo = codigo,
                                concessionaria = concessionaria,
                                qtd_contrat = qtd_contrat,
                                flex_min = flex_min,
                                flex_max = flex_max,
                                contrato_longo = contrato_longo,
                                preco = preco,
                                total_sem_icms = total_sem_icms,
                                preco_r = preco_r,
                                encargos = encargos,
                                valor_nf = valor_nf,
                                )
        
        dados_med.save()
        return redirect('input_med')
    
    return render(request,'input_medicao.html',{'clientes':clientes})

def medicao_fat(request):
    clientes = Cliente.objects.last()
    medicao = DadosMedicao.objects.all()
    dados = {
        'clientes':clientes,
        'medicao':medicao
    }
    return render(request,'medicao_fat.html',dados)

def simulacao(request):
    cliente = Cliente.objects.last()
    simulacoes = Simulacao.objects.all()
    # Calcular os valores para cada simulação
    for simulacao in simulacoes:
        try:
            simulacao.calculo()  # Chama o método de cálculo para cada simulação
        except Exception as e:
            print(f"Erro ao calcular simulação ID {simulacao.id}: {e}")
        
        
    quantidade_kw_total = Simulacao.objects.all().aggregate(Sum('quantidade_kw'))['quantidade_kw__sum']
    quantidade_kw_total = round(quantidade_kw_total, 2)
    unit_c_trib_total = Simulacao.objects.all().aggregate(Sum('unit_c_trib'))['unit_c_trib__sum']
    valor_total = (quantidade_kw_total + unit_c_trib_total) / 3.2
    
    dados = {
        'simulacoes': simulacoes,
        'cliente': cliente,
        'valor_total':valor_total,
        'unit_c_trib_total':unit_c_trib_total,
    }
    return render(request, 'simulacao.html', dados)

def dados_economia(request):
    dados_econ = DadosEconomia.objects.get(id=1)
    cativo_total = DadosEconomia.objects.all()
    cativo_fat = DadosEconomia.objects.all()
    enel_trad = DadosEconomia.objects.all()
    cativo_total = [cat_t.cativo_total for cat_t in cativo_total]
    cativo_fat=[cat_f.cativo_fat for cat_f in cativo_fat]
    enel_trad = [enel_t.enel_tranding for enel_t in enel_trad]
    perc_econ = dados_econ.livre / (dados_econ.livre + dados_econ.economia) 
    perc_total = dados_econ.economia / (dados_econ.livre + dados_econ.economia) 
    dados = {
        'cativo_total':cativo_total,
        'fat_t':[cativo_fat,enel_trad],
        'econ':[cativo_total,dados_econ.livre,dados_econ.economia],
        'percent':[perc_econ,perc_total],
    }
    return JsonResponse(dados)

def economia(request):
    return render(request,'graf_economia.html')

def input_economia(request):
    clientes = Cliente.objects.all()
    if request.method == "GET":
        return render(request, 'input_economia.html',{'clientes':clientes})
    elif request.method == "POST":
        cliente_nome = request.POST.get('cliente')
        cliente = Cliente.objects.get(nome=cliente_nome)
        enel_trad = request.POST.get('enel_trad')
        cativo_total = request.POST.get('cat_total')
        cativo_fat = request.POST.get('cat_fat')
        
        dados_econ = DadosEconomia(cliente=cliente,
                                enel_tranding=enel_trad,
                                cativo_total=cativo_total,
                                cativo_fat=cativo_fat,
                                )
        
        dados_econ.save()
        return redirect('input_econ')
    return render(request, 'input_economia.html',{'clientes':clientes})

def gerar_relatorio(request):
    return render(request, 'gerar_relatorio.html')

def final(request):
    return render(request,'final.html')


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    
    options = settings.PDFKIT_CONFIG['options']
    pdf = pdfkit.from_string(html, False, options=options)
    
    return pdf

def gerar_pdf(request):
    file_name = 'relatorio.pdf'
    pdf_path = os.path.join(settings.BASE_DIR,'templates' ,'static', 'pdf', file_name)
    
    _html = render_to_string('relatorio.html')
    options = {
        "enable-local-file-access": "",
        "orientation": "Landscape"}  # Define a orientação como paisagem
    pdfkit.from_string(_html, pdf_path, options=options)
    response = FileResponse(open(pdf_path, 'rb'), filename=file_name, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{file_name}"'
    
    return response


def capturar_imagem(request):
    # Configurações do Selenium
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Executa o Chrome em modo headless (sem interface gráfica)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Caminho para o ChromeDriver
    service = Service('TNG_REPORT/chromedriver')# Substitua pelo caminho do seu ChromeDriver
    options = Options()
    driver = webdriver.Chrome(options=options)

    # Lista de URLs que você deseja capturar
    urls = [
        'http://localhost:8000/capa',  
        'http://localhost:8000/abertura',
        'http://localhost:8000/historico',
        'http://localhost:8000/graf_hist',
        'http://localhost:8000/graf_custo',
        'http://localhost:8000/medicao_fat',
        'http://localhost:8000/faturamento',
        'http://localhost:8000/simulacao',
        'http://localhost:8000/graf_economia',
        'http://localhost:8000/final',
    ]

    # Dicionário para armazenar os caminhos das imagens
    screenshot_paths = {}

    for url in urls:
        # Acessa a URL
        driver.get(url)
        
        time.sleep(3)

        # Define o nome do arquivo de captura baseado na URL
        url_name = url.split('/')[-1]  # Pega a última parte da URL
        screenshot_path = f'media/capturas/{url_name}_screenshot.png'  # Define o caminho da imagem

        # Captura a imagem
        driver.save_screenshot(screenshot_path)

        # Armazena o caminho da imagem no dicionário
        screenshot_paths[url] = screenshot_path

    # Fecha o driver
    driver.quit()
    
    

    # Retorna as imagens como resposta (opcional)
    response_content = ""
    for url, path in screenshot_paths.items():
        response_content += f"Captura da URL {url}: {path}\n"

    return HttpResponse(response_content, content_type='text/plain')