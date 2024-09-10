# Generated by Django 4.2.15 on 2024-09-04 10:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0012_dadosfatura'),
    ]

    operations = [
        migrations.CreateModel(
            name='DadosMedicao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('volume_total', models.CharField(blank=True, max_length=100, null=True)),
                ('total_s_icms', models.CharField(blank=True, max_length=100, null=True)),
                ('consumo_mwh', models.CharField(blank=True, max_length=100, null=True)),
                ('consumo_perda', models.CharField(blank=True, max_length=100, null=True)),
                ('percentual', models.CharField(blank=True, max_length=100, null=True)),
                ('proinfa', models.CharField(blank=True, max_length=100, null=True)),
                ('consumo_perda_p', models.CharField(blank=True, max_length=100, null=True)),
                ('codigo', models.CharField(blank=True, max_length=100, null=True)),
                ('concessionaria', models.CharField(blank=True, max_length=100, null=True)),
                ('qtd_contrat', models.CharField(blank=True, max_length=100, null=True)),
                ('flex_min', models.CharField(blank=True, max_length=100, null=True)),
                ('flex_max', models.CharField(blank=True, max_length=100, null=True)),
                ('contrato_longo', models.CharField(blank=True, max_length=100, null=True)),
                ('preco', models.CharField(blank=True, max_length=100, null=True)),
                ('total_sem_icms', models.CharField(blank=True, max_length=100, null=True)),
                ('preco_r', models.CharField(blank=True, max_length=100, null=True)),
                ('encargos', models.CharField(blank=True, max_length=100, null=True)),
                ('valor_nf', models.CharField(blank=True, max_length=100, null=True)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='datamed', to='upload.cliente')),
            ],
        ),
    ]
