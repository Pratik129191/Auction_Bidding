# Generated by Django 4.1.1 on 2022-12-12 03:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("system", "0005_remove_auction_product_product_auction"),
    ]

    operations = [
        migrations.AddField(
            model_name="bid",
            name="auction",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="system.auction",
            ),
        ),
        migrations.AddField(
            model_name="bid",
            name="product",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="system.product",
            ),
        ),
    ]