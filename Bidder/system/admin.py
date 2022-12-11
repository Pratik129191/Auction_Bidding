import datetime

from django.contrib import admin
from django.db.models import Count, Value, BooleanField, ExpressionWrapper, Q
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode
from django.contrib import admin
from . import models


@admin.register(models.Auction)
class AuctionAdmin(admin.ModelAdmin):
    list_display = ['title', 'product_name', 'start_time', 'end_time', 'winner', 'is_active']
    readonly_fields = ['winner']
    search_fields = ['title']
    autocomplete_fields = ['product']

    def product_name(self, auction: models.Auction):
        url = (
            reverse('admin:system_product_changelist')
            + '?'
            + urlencode({
                'auction_id': str(auction.id)
            })
        )
        return format_html('<a href={}>{}</a>', url, auction.product)

    @admin.display(ordering='end_time')
    def is_active(self, auction: models.Auction):
        color = 'tomato'
        if auction.is_active:
            color = 'aqua'
        return format_html(
            '<button type="button" style="background-color: {}">{}</button>', color,
            auction.is_active
        )

    def get_queryset(self, request):
        return super(AuctionAdmin, self).get_queryset(request).annotate(
            is_active=ExpressionWrapper(
                Q(end_time__gt=datetime.datetime.now()),
                output_field=BooleanField()
            )
        )


@admin.register(models.AuctionBid)
class AuctionBidAdmin(admin.ModelAdmin):
    list_display = ['auction', 'user_name', 'offer', 'created', 'modified']

    def user_name(self, auction_bid: models.AuctionBid):
        url = (
            reverse('admin:system_auctionbid_changelist')
            + '?'
            + urlencode({
                'user_id': auction_bid.user.id
            })
        )
        return format_html('<a href={}>{}</a>', url, auction_bid.user)


@admin.register(models.Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ['user', 'status', 'created', 'modified']


class ProductImageInline(admin.TabularInline):
    model = models.ProductImage
    max_num = 3
    extra = 1
    readonly_fields = ['thumbnail']
    
    def thumbnail(self, product_image: models.ProductImage):
        if product_image.image.name != '':
            return format_html(f"<img src='{product_image.image.url}' class='thumbnail' />")
        return ''


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category']
    list_editable = ['price', 'category']
    list_per_page = 30
    search_fields = ['name']
    # inlines = [ProductImageInline]

    def images(self, product: models.Product):
        return product.images

    class Media:
        css = {
            'all': ['style.css']
        }


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']

    def products_count(self, category: models.Category):
        url = (
            reverse('admin:system_product_changelist')
            + '?'
            + urlencode({
                'category_id': str(category.id)
            })
        )
        return format_html(
            '<a href={}>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{}</a>',
            url, category.products_count
        )

    def get_queryset(self, request):
        return super(CategoryAdmin, self).get_queryset(request).annotate(
            products_count=Count('product')
        )
