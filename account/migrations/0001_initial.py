# Generated by Django 4.1.2 on 2022-10-28 13:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccountRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='TransactionRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(choices=[('deposit', 'DEPOSIT'), ('withdrawal', 'WITHDRAWAL'), ('transfer', 'TRANSFER')], max_length=10)),
                ('amount', models.IntegerField(default=0, verbose_name='amount')),
                ('created', models.DateField(auto_now_add=True)),
                ('source', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='money_out_transactions', to='account.accountrecord')),
                ('target', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='money_in_transactions', to='account.accountrecord')),
            ],
        ),
        migrations.CreateModel(
            name='AuditRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('old_balance', models.IntegerField(default=0)),
                ('new_balance', models.IntegerField(default=0)),
                ('created', models.DateField(auto_now_add=True)),
                ('account_record', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='account.accountrecord')),
            ],
        ),
    ]
