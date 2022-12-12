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
    list_display = ['title', 'start_time', 'start_price', 'end_time', 'highest_bid', 'winner_name', 'is_active']
    readonly_fields = ['highest_bid']
    search_fields = ['title']
    # autocomplete_fields = ['product']

    def product_name(self, auction: models.Auction):
        pass

    def winner_name(self, auction: models.Auction):
        url = (
            reverse('admin:system_auction_changelist')
            + '?'
            + urlencode({
                'winner_id': str(auction.winner_id)
            })
        )
        return format_html(f"<a href={url}>{auction.winner}</a>")

    def product_name(self, auction: models.Auction):
        url = (
            reverse('admin:system_product_changelist')
            + '?'
            + urlencode({
                'id': str()
            })
        )
        return format_html('<a href={}>{}</a>', url, auction.product)

    def highest_bid(self, auction: models.Auction):
        x = auction.auctionbid_set.filter(auction_id=auction.id).values('offer').latest('offer')
        return format_html(f"<p>Rs.&nbsp;{x['offer']}</p>")

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
    list_display = ['auction', 'product_name', 'user_name', 'offer', 'created', 'modified']

    def product_name(self, auction: models.AuctionBid):
        url = (
            reverse('admin:system_bid_changelist')
            + '?'
            + urlencode({
                'product_id': str(auction.bid.product_id)
            })
        )
        return format_html(f"<a href={url}>{auction.bid.product}</a>")

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
    list_select_related = ['user']
    list_display = ['user', 'status', 'product', 'offer', 'auction_name', 'created', 'modified']
    search_fields = ['user__first_name__icontains', 'product__name']

    def auction_name(self, bid: models.Bid):
        url = (
            reverse('admin:system_bid_changelist')
            + '?'
            + urlencode({
                'auction_id': str(bid.auction_id)
            })
        )
        return format_html(f"<a href={url}>{bid.auction}</a>")

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
    list_display = ['name', 'auction_title', 'price', 'category']
    list_editable = ['price', 'category']
    list_per_page = 30
    search_fields = ['name']
    # inlines = [ProductImageInline]

    def auction_title(self, product: models.Product):
        url = (
            reverse('admin:system_product_changelist')
            + '?'
            + urlencode({
                'auction_id': str(product.auction_id)
            })
        )
        return format_html(f"<a href={url}>{product.auction}</a>")
        # return product.auction_set.filter(product_id=product.id)

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
