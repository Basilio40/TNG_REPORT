# Generated by Django 5.0.7 on 2024-08-02 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0004_alter_conta_cliente_alter_conta_descricao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conta',
            name='aliquota_icms',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='conta',
            name='base_icms',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='conta',
            name='pis_cofins',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='conta',
            name='quantidade_kw',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='conta',
            name='tarifa_unitaria',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='conta',
            name='unid_c_tributos',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='conta',
            name='unidade',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='conta',
            name='valor_icms',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='conta',
            name='valor_unit',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
