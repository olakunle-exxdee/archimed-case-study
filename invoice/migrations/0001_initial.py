# Generated by Django 5.0.7 on 2024-08-07 21:37

import django.core.validators
import django.db.models.deletion
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Investment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('date', models.DateField(auto_now_add=True, help_text='The date the investment was made')),
                ('fee_percentage', models.DecimalField(decimal_places=2, max_digits=4, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
            ],
        ),
        migrations.CreateModel(
            name='Investor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bill_type', models.CharField(choices=[('MEMBERSHIP', 'Membership'), ('UPFRONT', 'Upfront Fees'), ('YEARLY', 'Yearly Fees')], max_length=10)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateField()),
                ('investment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bills', to='invoice.investment')),
                ('investor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bills', to='invoice.investor')),
            ],
        ),
        migrations.AddField(
            model_name='investment',
            name='investor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='investments', to='invoice.investor'),
        ),
        migrations.CreateModel(
            name='CapitalCall',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('date', models.DateField()),
                ('due_date', models.DateField()),
                ('iban', models.CharField(max_length=34)),
                ('status', models.CharField(choices=[('VALIDATED', 'Validated'), ('SENT', 'Sent'), ('PAID', 'Paid'), ('OVERDUE', 'Overdue')], default='VALIDATED', max_length=10)),
                ('bills', models.ManyToManyField(to='invoice.bill')),
                ('investor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='capital_calls', to='invoice.investor')),
            ],
        ),
    ]
